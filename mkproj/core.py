import sys

from pathlib import Path
from typing import Dict

import networkx

from . import LockingDict, config, spinner
from .bases import BaseTask, TaskFailedException


def depends(*deps):
    def depends() -> set:
        return set(deps)

    def wrapper(cls):
        setattr(cls, depends.__name__, staticmethod(depends))
        return cls

    return wrapper


class TaskIndex:
    def __init__(self, project_name: str, project_path: Path, langs: list):
        self._langs: list = langs

        self._data: LockingDict = LockingDict(
            {"project-name": project_name, "project-path": project_path}
        )
        self._tasks: Dict[str, BaseTask] = {}

        self._index()

    def __len__(self):
        return len(self._tasks)

    def __repr__(self):
        return self._tasks.__repr__()

    def _index(self):
        self._tasks = {
            n.task_id(): n(self._data)
            for n in BaseTask.__subclasses__()
            if n.lang_id() in self._langs
            and n.task_id() not in config.get_config("tasks", "skip")
        }

    def _task(self, task: str) -> BaseTask:
        return self._tasks[task]

    def lang_id(self, task: str) -> str:
        return self._task(task).lang_id()

    def task_ids(self) -> list:
        return list(self._tasks.keys())

    def task_id(self, task: str) -> str:
        return self._task(task).task_id()

    def depends(self, task: str) -> set:
        return self._task(task).depends()

    def config_defaults(self, task: str) -> Dict[str, dict]:
        return self._task(task).config_defaults()

    def run(self, task: str):
        self._task(task).run()


class TaskGraph:
    def __init__(self, tasks: TaskIndex):
        self._graph: networkx.DiGraph = networkx.DiGraph()

        self._tasks: TaskIndex = tasks

        self._build_graph()

    @property
    def tasks(self) -> TaskIndex:
        return self._tasks

    @tasks.setter
    def tasks(self, tasks: Dict[str, BaseTask]):
        self._tasks = tasks
        self._build_graph()

    def _build_graph(self):
        nodes: list = self._tasks.task_ids()
        self._graph.add_nodes_from(nodes, success=False, error=False)

        edges: list = [
            (task, dep)
            for task in nodes
            for dep in self._tasks.depends(task)
            if not set()
        ]
        self._graph.add_edges_from(edges)

    def _run_nodes(self, nodes: networkx.classes.reportviews.NodeView):
        rerun_nodes: list = []

        for node in nodes:
            if (
                not self._graph.nodes[node]["error"]
                and not len(list(self._graph.successors(node))) > 0
            ):
                try:
                    self._tasks.run(node)
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

    tasks: TaskIndex = TaskIndex(project_name, project_path, langs)
    graph: TaskGraph = TaskGraph(tasks)

    spinner.start()
    graph.run_nodes()
    spinner.ok()
