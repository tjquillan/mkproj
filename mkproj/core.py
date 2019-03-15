import sys

from collections.abc import MutableMapping
from pathlib import Path
from typing import Any, Dict, List, Tuple

import networkx

from pluginbase import PluginBase, PluginSource

from . import LockingDict, config, environment, spinner
from .bases import BaseTask, TaskFailedException


def depends(*tasks):
    def depends() -> set:
        return set(tasks)

    def wrapper(cls):
        setattr(cls, depends.__name__, staticmethod(depends))
        return cls

    return wrapper


def overrides(*tasks):
    def overrides() -> set:
        return set(tasks)

    def wrapper(cls):
        setattr(cls, overrides.__name__, staticmethod(overrides))
        return cls

    return wrapper


class TaskIndex(MutableMapping):
    def __init__(
        self,
        project_name: str,
        project_path: Path,
        langs: List[str],
        mixins: List[str],
        *args,
        **kwargs,
    ):
        self._langs: List[str] = langs
        self._mixins: List[str] = mixins

        self._data: LockingDict = LockingDict(
            {"project-name": project_name, "project-path": project_path}
        )

        self._tasks: Dict[str, Dict[str, Any]] = dict(*args, **kwargs)
        self._index()

    def _index(self):
        skip_tasks: List[str] = list(config.get_config("tasks", "skip"))
        # fmt: off
        self._tasks = {
            n.task_id(): {
                "class": n(self._data),
                "overridden": False,
                "overrider": None,
            }
            for n in BaseTask.__subclasses__()
            if n.task_id() not in skip_tasks  # Check if the task should be skipped
            and n.lang_id() in self._langs  # Check if the task is in the langs specified
            and (n.mixin_id() in self._mixins  # Check if the task is in the mixins specified
                 or n.mixin_id() is None)  # or if it is not a mixin
        }
        # fmt: on

        for task in self._tasks:
            override_tasks: Dict[str, List[str]] = {}
            for override_task in self._tasks[task]["class"].overrides():
                try:
                    override_tasks[override_task].append(
                        self._tasks[task]["class"].task_id()
                    )
                    spinner.print_error(
                        "Tasks: {} both attempt to override task: '{}'".format(
                            override_tasks[override_task], override_task
                        )
                    )
                    sys.exit(1)
                except KeyError:
                    override_tasks[override_task] = [
                        self._tasks[task]["class"].task_id()
                    ]
                    self._override(override_task, task)

    def _override(self, overridden: str, overrider: str):
        self._tasks[overridden]["overridden"] = True
        self._tasks[overridden]["overrider"] = overrider

    def __setitem__(self, key: str, value):
        self._tasks[key] = value

    def __getitem__(self, key: str):
        return self._tasks[key]

    def __delitem__(self, key: str):
        del self._tasks[key]

    def __iter__(self):
        return iter(self._tasks)

    def __len__(self):
        return len(self._tasks)

    def __repr__(self):
        return self._tasks.__repr__()


class TaskGraph:
    def __init__(self, tasks: TaskIndex):
        self._graph: networkx.DiGraph = networkx.DiGraph()

        self._tasks: TaskIndex = tasks

        self._build_graph()

    @property
    def tasks(self) -> TaskIndex:
        return self._tasks

    def _build_graph(self):
        # Assemble the initial nodes and edges
        nodes: List[str] = self._tasks.keys()
        edges: List[Tuple[str, str]] = [
            (
                task,
                self._tasks[dep]["overrider"]
                if self._tasks[dep]["overridden"]
                else dep,
            )
            for task in nodes
            if not self._tasks[task]["overridden"]
            for dep in self._tasks[task]["class"].depends()
            if not set()
        ]

        self._graph.add_nodes_from(nodes, success=False, error=False)
        self._graph.add_edges_from(edges)

    def _run_nodes(self, nodes: networkx.classes.reportviews.NodeView):
        rerun_nodes: list = []

        for node in nodes:
            if not self._tasks[node]["overridden"]:
                if (
                    not self._graph.nodes[node]["error"]
                    and not len(list(self._graph.successors(node))) > 0
                ):
                    try:
                        self._tasks[node]["class"].run()
                        self._graph.nodes[node]["success"] = True
                        edges: list = [
                            (dep, node) for dep in self._graph.predecessors(node)
                        ]
                        self._graph.remove_edges_from(edges)
                    except TaskFailedException:
                        self._graph.nodes[node]["error"] = True
                        for dep in self._graph.predecessors(node):
                            self._graph.nodes[dep]["error"] = True
                elif not self._graph.nodes[node]["error"]:
                    rerun_nodes.append(node)

        if rerun_nodes:
            self._run_nodes(rerun_nodes)

    def run_nodes(self):
        self._run_nodes(self._graph.nodes)


from .cli.options import State  # isort:skip # noqa: E402


def create_project(project_name: str, state: State):
    project_path: Path = Path("{0}/{1}".format(Path.cwd(), project_name))

    if project_path.exists():
        spinner.print_error("Project already exists. Aborting...")
        sys.exit(1)

    langs: list = ["generic"]
    if state.lang is not None:
        langs.append(state.lang)

    mixins: list = list(config.get_config(state.lang, "mixins")) + state.mixins

    # Load external tasks
    plugin_base: PluginBase = PluginBase(package="mkproj.plugins")
    plugin_source: PluginSource = plugin_base.make_plugin_source(
        searchpath=["{}/tasks".format(environment.APP_DIRS.user_data_dir)]
    )
    for plugin in plugin_source.list_plugins():
        plugin_source.load_plugin(plugin)

    tasks: TaskIndex = TaskIndex(project_name, project_path, langs, mixins)
    graph: TaskGraph = TaskGraph(tasks)

    spinner.start()
    graph.run_nodes()
    spinner.ok()
