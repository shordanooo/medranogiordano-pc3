"""
Patron Composite: Construye el documento de propuesta legislativa
como un árbol de componentes (titulo, cuerpo, firmas, recursos).
"""
from abc import ABC, abstractmethod
from typing import List


class ProposalComponent(ABC):
    """Componente base del árbol Composite."""

    @abstractmethod
    def render(self) -> dict:
        pass

    @abstractmethod
    def get_word_count(self) -> int:
        pass


class ProposalLeaf(ProposalComponent):
    """Hoja: sección individual del documento."""

    def __init__(self, section_name: str, content: str):
        self.section_name = section_name
        self.content = content

    def render(self) -> dict:
        return {self.section_name: self.content}

    def get_word_count(self) -> int:
        return len(self.content.split())


class ProposalComposite(ProposalComponent):
    """Compuesto: agrupa secciones del documento legislativo."""

    def __init__(self, name: str):
        self.name = name
        self._children: List[ProposalComponent] = []

    def add(self, component: ProposalComponent):
        self._children.append(component)
        return self

    def remove(self, component: ProposalComponent):
        self._children.remove(component)

    def render(self) -> dict:
        result = {"section": self.name, "children": []}
        for child in self._children:
            result["children"].append(child.render())
        return result

    def get_word_count(self) -> int:
        return sum(child.get_word_count() for child in self._children)


class LegislativeDocument:
    """Builder del documento legislativo usando el patrón Composite."""

    def __init__(self, proposal_id: int, title: str):
        self.root = ProposalComposite("documento_legislativo")
        self.proposal_id = proposal_id

        header = ProposalLeaf("titulo", title)
        self.root.add(header)

    def add_section(self, name: str, content: str) -> "LegislativeDocument":
        self.root.add(ProposalLeaf(name, content))
        return self

    def add_signatures_section(self, count: int) -> "LegislativeDocument":
        self.root.add(ProposalLeaf("firmas_validas", str(count)))
        return self

    def build(self) -> dict:
        return {
            "proposal_id": self.proposal_id,
            "total_words": self.root.get_word_count(),
            "content": self.root.render(),
        }
