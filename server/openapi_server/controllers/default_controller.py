import connexion
import six

from openapi_server.models.concept_code import ConceptCode  # noqa: E501
from openapi_server.models.concept_detail import ConceptDetail  # noqa: E501
from openapi_server.models.concept_term import ConceptTerm  # noqa: E501
from openapi_server.models.qqst import QQST  # noqa: E501
from openapi_server.models.sab_code_term import SabCodeTerm  # noqa: E501
from openapi_server.models.sab_definition import SabDefinition  # noqa: E501
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm  # noqa: E501
from openapi_server.models.semantic_stn import SemanticStn  # noqa: E501
from openapi_server.models.sty_tui_stn import StyTuiStn  # noqa: E501
from openapi_server.models.termtype_code import TermtypeCode  # noqa: E501
from openapi_server.models.termtype_term import TermtypeTerm  # noqa: E501
from openapi_server import util
from openapi_server.controllers.neo4j_manager import Neo4jManager

neo4jManager = Neo4jManager()


def codes_code_id_codes_get(code_id: str) -> [ConceptCode]:  # noqa: E501
    """Returns a list of {Concept, Code} dictionaries associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[ConceptCode]
    """
    return neo4jManager.codes_code_id_codes_get(code_id)


def codes_code_id_concepts_get(code_id: str) -> [ConceptDetail]:  # noqa: E501
    """Returns a list of {Concept, Prefterm} dictionaries associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[ConceptDetail]
    """
    return neo4jManager.codes_code_id_concepts_get(code_id)


def codes_code_id_description_get(code_id: str) -> [SabCodeTerm]:  # noqa: E501
    """Returns a list of {SAB, Code, Term} dictionaries associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[SabCodeTerm]
    """
    return neo4jManager.codes_code_id_description_get(code_id)


def codes_code_id_terms_get(code_id: str) -> [TermtypeTerm]:  # noqa: E501
    """Returns a list of {TermType, Term} dictionaries associated with the code_id

     # noqa: E501

    :param code_id: The code identifier
    :type code_id: str

    :rtype: List[TermtypeTerm]
    """
    return neo4jManager.codes_code_id_terms_get(code_id)


def concepts_concept_id_codes_get(concept_id: str) -> [str]:  # noqa: E501
    """Returns a distinct list of codes associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[str]
    """
    return neo4jManager.concepts_concept_id_codes_get(concept_id)


def concepts_concept_id_concepts_get(concept_id: str) -> [SabRelationshipConceptPrefterm]:  # noqa: E501
    """Returns a list of {Sab, Relationship, Concept, Prefterm} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabRelationshipConceptPrefterm]
    """
    return neo4jManager.concepts_concept_id_concepts_get(concept_id)


def concepts_concept_id_definitions_get(concept_id: str) -> [SabDefinition]:  # noqa: E501
    """Returns a list of {Sab, Definition} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[SabDefinition]
    """
    return neo4jManager.concepts_concept_id_definitions_get(concept_id)


def concepts_concept_id_semantics_get(concept_id: str) -> [StyTuiStn]:  # noqa: E501
    """Returns a list of {Sty, Tui, Stn} dictionaries associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[StyTuiStn]
    """
    return neo4jManager.concepts_concept_id_semantics_get(concept_id)


def concepts_concept_id_terms_get(concept_id: str) -> [str]:  # noqa: E501
    """Returns a list of Terms associated with the concept_id

     # noqa: E501

    :param concept_id: The concept identifier
    :type concept_id: str

    :rtype: List[str]
    """
    return neo4jManager.concepts_concept_id_terms_get(concept_id)


def semantics_semantic_id_semantics_get(semantic_id: str) -> [QQST]:  # noqa: E501
    """Returns a list of {queryTUI, querySTN ,semantic, TUI_STN} dictionaries associated with the concept_id

     # noqa: E501

    :param semantic_id: The semantic identifier
    :type semantic_id: str

    :rtype: List[QQST]
    """
    return neo4jManager.semantics_semantic_id_semantics_get(semantic_id)


def terms_term_id_codes_get(term_id: str) -> [TermtypeCode]:  # noqa: E501
    """Returns a list of {TermType, Code} dictionaries associated with the term_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[TermtypeCode]
    """
    return neo4jManager.terms_term_id_codes_get(term_id)


def terms_term_id_concepts_get(term_id: str) -> [str]:  # noqa: E501
    """Returns a list of Terms associated with the concept_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[str]
    """
    return neo4jManager.terms_term_id_concepts_get(term_id)


def terms_term_id_concepts_terms_get(term_id: str) -> [ConceptTerm]:  # noqa: E501
    """Returns a list of {Concept, Term} dictionaries associated with the term_id

     # noqa: E501

    :param term_id: The term identifier
    :type term_id: str

    :rtype: List[ConceptTerm]
    """
    return neo4jManager.terms_term_id_concepts_terms_get(term_id)


def tui_tui_id_semantics_get(tui_id: str) -> [SemanticStn]:  # noqa: E501
    """Returns a list of {semantic, STN} dictionaries associated with the tui_id

     # noqa: E501

    :param tui_id: The TUI identifier
    :type tui_id: str

    :rtype: List[SemanticStn]
    """
    return neo4jManager.tui_tui_id_semantics_get(tui_id)