"""Minimal in-memory prototype of Helios Atlas.

The goal is to experiment con estructura de nodos, edges y generación de context packs
sin depender de almacenamiento externo.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple


@dataclass
class Summary:
    """Resúmenes jerárquicos por nodo."""

    macro: str
    meso: str
    micro: str
    invariants: List[str] = field(default_factory=list)


@dataclass
class Node:
    node_id: str
    node_type: str
    attributes: Dict[str, str]
    summary: Summary
    neighbors: Set[str] = field(default_factory=set)


class HeliosAtlas:
    def __init__(self) -> None:
        self._nodes: Dict[str, Node] = {}
        self._edges: Dict[Tuple[str, str], str] = {}

    # --- node management -------------------------------------------------
    def add_node(
        self,
        node_id: str,
        node_type: str,
        attributes: Optional[Dict[str, str]] = None,
        summary: Optional[Summary] = None,
    ) -> None:
        if node_id in self._nodes:
            raise ValueError(f"Node {node_id} already exists")
        self._nodes[node_id] = Node(
            node_id=node_id,
            node_type=node_type,
            attributes=attributes or {},
            summary=summary or Summary(macro="", meso="", micro=""),
        )

    def add_edge(self, source: str, target: str, edge_type: str) -> None:
        if source not in self._nodes or target not in self._nodes:
            raise KeyError("Both nodes must exist before adding an edge")
        key = (source, target)
        self._edges[key] = edge_type
        self._nodes[source].neighbors.add(target)

    # --- query helpers ---------------------------------------------------
    def get_node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def neighbors(self, node_id: str, edge_filter: Optional[str] = None) -> List[Node]:
        node = self._nodes[node_id]
        if edge_filter is None:
            return [self._nodes[n_id] for n_id in node.neighbors]
        return [
            self._nodes[target]
            for (source, target), e_type in self._edges.items()
            if source == node_id and e_type == edge_filter
        ]

    # --- context pack generation ----------------------------------------
    def generate_context_pack(
        self,
        focus_nodes: List[str],
        target_tokens: int,
        capsule_id: Optional[str] = None,
    ) -> Dict[str, object]:
        """Produce un context pack rudimentario basado en resúmenes.

        Este prototipo simplemente ajusta la granularidad según los tokens.
        En implementación real se aplicarían embeddings y ranking semántico.
        """

        pack: Dict[str, object] = {
            "request": {
                "focus_nodes": focus_nodes,
                "target_tokens": target_tokens,
                "capsule_id": capsule_id,
            },
            "contents": {
                "macro_outline": [],
                "meso_details": [],
                "micro_snippets": [],
                "related_tests": [],
                "invariants": set(),
            },
        }

        for node_id in focus_nodes:
            node = self._nodes[node_id]
            summaries = pack["contents"]
            summaries["macro_outline"].append({
                "node": node_id,
                "summary": node.summary.macro,
            })
            summaries["meso_details"].append({
                "node": node_id,
                "summary": node.summary.meso,
                "neighbors": list(self._nodes[n_id].node_type for n_id in node.neighbors),
            })
            summaries["micro_snippets"].append({
                "node": node_id,
                "summary": node.summary.micro,
            })
            summaries["invariants"].update(node.summary.invariants)

            # ejemplo simplista: recomendaciones de pruebas basadas en edges `validates`
            for (source, target), edge_type in self._edges.items():
                if edge_type == "validates" and target == node_id:
                    summaries["related_tests"].append(source)

        summaries["invariants"] = sorted(list(summaries["invariants"]))
        return pack


def demo() -> None:
    atlas = HeliosAtlas()
    atlas.add_node(
        "atom:email-format-validator",
        "atom",
        attributes={"language": "python"},
        summary=Summary(
            macro="Validador de email usado en autenticación",
            meso="Procesa strings RFC 5322 y retorna estructura {valid, error}",
            micro="def validate_email(email: str) -> dict",
            invariants=["deterministic", "null_safety"],
        ),
    )
    atlas.add_node(
        "test:property/email_unicode_fuzz",
        "test",
        summary=Summary(
            macro="Property-based fuzz para emails unicode",
            meso="Cubre variantes IDN y caracteres extremos",
            micro="pytest -k email_unicode_fuzz",
        ),
    )
    atlas.add_edge(
        "test:property/email_unicode_fuzz",
        "atom:email-format-validator",
        "validates",
    )

    pack = atlas.generate_context_pack(
        ["atom:email-format-validator"],
        target_tokens=2048,
        capsule_id="omega-demo",
    )
    for section, details in pack["contents"].items():
        print(f"[{section}] => {details}")


if __name__ == "__main__":
    demo()
