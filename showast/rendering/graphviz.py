"""
Rendering module for graphviz.
"""

import itertools
from functools import partial

try:
    reduce
except NameError:
    from functools import reduce

import graphviz
from IPython.display import SVG

from showast.asts import recurse_through_ast


def _bold(label):
    return "<<B>{}</B>>".format(label)


def _attach_to_parent(parent, graph, names, label, name=None, **style):
    node_name = next(names) if name is None else name
    node = graph.node(node_name, label=label, **style)
    if parent is not None:
        graph.edge(parent, node_name, sametail="t{}".format(parent))


def handle_ast(
    node,
    parent_node,
    graph,
    names,
    omit_docstrings,
    terminal_color,
    nonterminal_color,
    field_name=None,
):
    attach_to_parent = partial(
        _attach_to_parent,
        graph=graph,
        names=names,
    )
    node_name = next(names)

    _label = _bold(node.__class__.__name__)
    if field_name is not None:
        _label = "%s\n[%s]" % (node.__class__.__name__, field_name)

    attach_to_parent(
        parent=parent_node,
        label=_label,
        name=node_name,
        fontcolor=nonterminal_color,
    )
    recurse_through_ast(
        node,
        partial(
            handle_ast,
            parent_node=node_name,
            graph=graph,
            names=names,
            omit_docstrings=omit_docstrings,
            terminal_color=terminal_color,
            nonterminal_color=nonterminal_color,
        ),
        partial(
            handle_terminal,
            attach_to_parent=partial(
                attach_to_parent,
                parent=node_name,
                fontcolor=terminal_color,
            ),
        ),
        handle_fields,
        partial(
            handle_no_fields,
            parent_node=node_name,
            graph=graph,
            terminal_color=terminal_color,
            nonterminal_color=nonterminal_color,
        ),
        omit_docstrings,
    )


def handle_terminal(terminal, attach_to_parent):
    attach_to_parent(label=str(terminal))


def handle_fields(*__):
    pass


def handle_no_fields(__, parent_node, graph, terminal_color, nonterminal_color):
    parent_node_beginning = "{} ".format(parent_node)
    parent_node_num = int(parent_node)
    for i, node in enumerate(graph.body[parent_node_num:]):
        if node.strip().startswith(parent_node_beginning):
            break
    else:
        raise KeyError("Could not find parent in graph.")
    replacements = {
        nonterminal_color: terminal_color,
        "<<B>": "",
        "</B>>": "",
    }
    graph.body[i + parent_node_num] = reduce(
        lambda s, replacement: s.replace(*replacement),
        replacements.items(),
        node,
    )


def render(node, settings):
    """
    Given an AST node and settings, return a displayable object.
    """
    graph = graphviz.Graph(format="svg")
    names = (str(x) for x in itertools.count())

    handle_ast(
        node,
        parent_node=None,
        graph=graph,
        names=names,
        omit_docstrings=settings["omit_docstrings"],
        terminal_color=settings["terminal_color"],
        nonterminal_color=settings["nonterminal_color"],
    )

    graph.node_attr.update(
        dict(
            fontname=settings["font"],
            shape=settings["shape"],
            # height='0.25',  # TODO: how to incorporate with scale param?
            # fixedsize='true',
        )
    )

    return SVG(graph.pipe(format="svg"))
