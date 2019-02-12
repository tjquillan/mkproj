import sys

from pathlib import Path
from typing import Dict

import networkx

from . import LockingDict, spinner
from .bases import BaseTask, TaskFailedException


def depends(*deps):
    def depends() -> set:
        return set(deps)

    def wrapper(cls):
        setattr(cls, depends.__name__, staticmethod(depends))
        return cls

    return wrapper


def build_graph(langs: list):
    graph = networkx.DiGraph()
    nodes = list(n.task_id() for n in BaseTask.__subclasses__() if n.lang_id() in langs)
    graph.add_nodes_from(nodes, success=False, error=False)
    edges = list(
        (n.task_id(), dep)
        for n in BaseTask.__subclasses__()
        if n.lang_id() in langs
        for dep in n.depends()
        if not set()
    )
    graph.add_edges_from(edges)

    return graph


def run_nodes(graph: networkx.DiGraph, nodes, tasks: Dict[str, BaseTask]):
    rerun_nodes = []

    for node in nodes:
        if (
            not graph.nodes[node]["error"] and not len(list(graph.successors(node))) > 0
        ):  # noqa: E501
            try:
                tasks[node].run()
                graph.nodes[node]["success"] = True
                edges = list((dep, node) for dep in graph.predecessors(node))
                graph.remove_edges_from(edges)
            except TaskFailedException:
                graph.nodes[node]["error"] = True
                for dep in graph.predecessors(node):
                    graph.nodes[dep]["error"] = True
        elif not graph.nodes[node]["error"]:
            rerun_nodes.append(node)

    if rerun_nodes:
        run_nodes(graph, rerun_nodes, tasks)


from .cli.options import State  # isort:skip # noqa: E402


def create_project(project_name: str, state: State):
    project_path = Path("{0}/{1}".format(Path.cwd(), project_name))

    if project_path.exists():
        spinner.print_error("Project already exists. Aborting...")
        sys.exit(1)

    data = LockingDict({"project-name": project_name, "project-path": project_path})
    tasks = dict((n.task_id(), n(data)) for n in BaseTask.__subclasses__())

    langs = ["generic"]
    if state.lang is not None:
        langs.append(state.lang)

    graph = build_graph(langs)

    spinner.start()
    run_nodes(graph, graph.nodes, tasks)
    spinner.ok()
