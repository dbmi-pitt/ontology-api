import neo4j
import configparser

from openapi_server.models.concept_code import ConceptCode
from openapi_server.models.concept_detail import ConceptDetail
from openapi_server.models.qqst import QQST
from openapi_server.models.sab_code_term import SabCodeTerm
from openapi_server.models.sab_definition import SabDefinition
from openapi_server.models.sab_relationship_concept_prefterm import SabRelationshipConceptPrefterm
from openapi_server.models.semantic_stn import SemanticStn
from openapi_server.models.sty_tui_stn import StyTuiStn
from openapi_server.models.termtype_code import TermtypeCode
from openapi_server.models.termtype_term import TermtypeTerm
from openapi_server.models.concept_term import ConceptTerm


class Neo4jManager(object):

    def __init__(self):
        config = configparser.ConfigParser()
        # [neo4j]
        # Server = bolt://localhost: 7687
        # Username = neo4j
        # Password = password
        config.read('openapi_server/resources/app.properties')
        neo4j_config = config['neo4j']
        server = neo4j_config.get('Server')
        username = neo4j_config.get('Username')
        password = neo4j_config.get('Password')
        self.driver = neo4j.GraphDatabase.driver(server, auth=(username, password))

    # https://neo4j.com/docs/api/python-driver/current/api.html
    def close(self):
        self.driver.close()

    def codes_code_id_codes_get(self, code_id: str) -> [ConceptCode]:
        conceptCodes: [ConceptCode] = []
        query = 'WITH [$code_id] AS query MATCH (a:Code)<-[:CODE]-(b:Concept)-[:CODE]->(c:Code)' \
                ' WHERE a.CodeID IN query' \
                ' RETURN DISTINCT a.CodeID AS Code1, b.CUI as Concept, c.CodeID AS Code2' \
                ' ORDER BY Code1, Concept ASC, Code2'
        with self.driver.session() as session:
            recds = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    conceptCode: ConceptCode = ConceptCode(record.get('Concept'), record.get('Code2'))
                    conceptCodes.append(conceptCode)
                except KeyError:
                    pass
        return conceptCodes

    def codes_code_id_concepts_get(self, code_id: str) -> [ConceptDetail]:
        conceptDetails: [ConceptDetail] = []
        query = 'WITH [$code_id] AS query MATCH (a:Code)<-[:CODE]-(b:Concept)-[:PREF_TERM]->(c:Term)' \
                ' WHERE a.CodeID IN query' \
                ' RETURN DISTINCT a.CodeID AS Code, b.CUI AS Concept, c.name as Prefterm' \
                ' ORDER BY Code ASC, Concept'
        with self.driver.session() as session:
            recds = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    conceptDetail: ConceptDetail = ConceptDetail(record.get('Concept'), record.get('Prefterm'))
                    conceptDetails.append(conceptDetail)
                except KeyError:
                    pass
        return conceptDetails

    def codes_code_id_description_get(self, code_id: str) -> [SabCodeTerm]:
        sabCodeTerms: [SabCodeTerm] = []
        query = 'WITH [$code_id] as query MATCH (c:Code)<--(e:Concept)' \
                ' WHERE c.CodeID = query WITH c,e MATCH p = ((e:Concept)<-[:isa|CHD|subclass_of|part_of*0..5]-(l:Concept))' \
                ' WHERE ALL (y IN relationships(p)' \
                ' WHERE y.SAB = c.SAB) WITH c,l MATCH (n:Code)<--(l:Concept)-[:PREF_TERM]->(v:Term)' \
                ' WHERE n.SAB = c.SAB' \
                ' RETURN DISTINCT n.SAB AS SAB, n.CODE as code, v.name as term' \
                ' ORDER BY SAB, code, size(term)'
        with self.driver.session() as session:
            recds = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    sabCodeTerm: SabCodeTerm = SabCodeTerm(record.get('SAB'), record.get('code'), record.get('term'))
                    sabCodeTerms.append(sabCodeTerm)
                except KeyError:
                    pass
        return sabCodeTerms

    def codes_code_id_terms_get(self, code_id) -> [TermtypeTerm]:
        termtypeTerms: [TermtypeTerm] = []
        query = 'WITH [$code_id] AS query MATCH (a:Code)-[b]->(c:Term)' \
                ' WHERE a.CodeID IN query' \
                ' RETURN DISTINCT a.CodeID AS Code, Type(b) AS TermType, c.name AS Term' \
                ' ORDER BY Code, TermType, Term'
        with self.driver.session() as session:
            recds = session.run(query, code_id=code_id)
            for record in recds:
                try:
                    termtypeTerm: TermtypeTerm = TermtypeTerm(record.get('TermType'), record.get('Term'))
                    termtypeTerms.append(termtypeTerm)
                except KeyError:
                    pass
        return termtypeTerms

    # https://neo4j.com/docs/api/python-driver/current/api.html#explicit-transactions
    def concepts_concept_id_codes_get(self, concept_id: str) -> [str]:
        codes: [str] = []
        query = 'WITH [$concept_id] AS query MATCH (a:Concept)-[:CODE]->(b:Code)' \
                ' WHERE a.CUI IN query' \
                ' RETURN DISTINCT a.CUI AS Concept, b.CodeID AS Code' \
                ' ORDER BY Concept, Code ASC'
        with self.driver.session() as session:
            recds = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    code = record.get('Code')
                    codes.append(code)
                except KeyError:
                    pass
        return codes

    def concepts_concept_id_concepts_get(self, concept_id: str) -> [SabRelationshipConceptPrefterm]:
        sabRelationshipConceptPrefterms: [SabRelationshipConceptPrefterm] = []
        query = 'WITH [$concept_id] AS query MATCH (a:Term)<-[:PREF_TERM]-(b:Concept)-[c]-(d:Concept)-[:PREF_TERM]->(e:Term)' \
                ' WHERE b.CUI IN query' \
                ' RETURN DISTINCT a.name AS Prefterm1, b.CUI AS Concept1, c.SAB AS SAB, type(c) AS Relationship,' \
                ' d.CUI AS Concept2, e.name AS Prefterm2' \
                ' ORDER BY Concept1, Relationship, Concept2 ASC, Prefterm1, Prefterm2'
        with self.driver.session() as session:
            recds = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    sabRelationshipConceptPrefterm: SabRelationshipConceptPrefterm =\
                        SabRelationshipConceptPrefterm(record.get('SAB'), record.get('Relationship'),
                                                       record.get('Concept2'), record.get('Prefterm2'))
                    sabRelationshipConceptPrefterms.append(sabRelationshipConceptPrefterm)
                except KeyError:
                    pass
        return sabRelationshipConceptPrefterms

    def concepts_concept_id_definitions_get(self, concept_id: str) -> [SabDefinition]:
        sabDefinitions: [SabDefinition] = []
        query = 'WITH [$concept_id] AS query MATCH (a:Concept)-[:DEF]->(b:Definition)' \
                ' WHERE a.CUI in query' \
                ' RETURN DISTINCT a.CUI AS Concept, b.SAB AS SAB, b.DEF AS Definition' \
                ' ORDER BY Concept, SAB'
        with self.driver.session() as session:
            recds = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    sabDefinition: SabDefinition = SabDefinition(record.get('SAB'), record.get('Definition'))
                    sabDefinitions.append(sabDefinition)
                except KeyError:
                    pass
        return sabDefinitions

    def concepts_concept_id_terms_get(self, concept_id: str) -> [str]:
        concepts: [str] = []
        query = 'WITH [$concept_id] AS query MATCH (a:Term)<-[:PREF_TERM]-(b:Concept)-[:CODE]->(c:Code)-[d]->(e:Term)' \
                ' WHERE b.CUI IN query AND b.CUI = d.CUI WITH b,COLLECT(e.name)+[a.name] AS x WITH * UNWIND(x) AS Term' \
                ' RETURN DISTINCT b.CUI AS Concept, Term' \
                ' ORDER BY Term ASC'
        with self.driver.session() as session:
            recds = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    concept: str = record.get('Term')
                    concepts.append(concept)
                except KeyError:
                    pass
        return concepts

    def concepts_concept_id_semantics_get(self, concept_id) -> [StyTuiStn]:
        styTuiStns: [StyTuiStn] = []
        query = 'WITH [$concept_id] AS query MATCH (a:Concept)-[:STY]->(b:Semantic)' \
                ' WHERE a.CUI IN query' \
                ' RETURN DISTINCT a.CUI AS concept, b.name AS STY, b.TUI AS TUI, b.STN as STN'
        with self.driver.session() as session:
            recds = session.run(query, concept_id=concept_id)
            for record in recds:
                try:
                    styTuiStn: StyTuiStn = StyTuiStn(record.get('STY'), record.get('TUI'), record.get('STN'))
                    styTuiStns.append(styTuiStn)
                except KeyError:
                    pass
        return styTuiStns

    def semantics_semantic_id_semantics_get(self, semantic_id: str) -> [QQST]:
        qqsts: [QQST] = []
        query = 'WITH [$semantic_id] AS query MATCH (a:Semantic)-[:ISA_STY]->(b:Semantic)' \
                ' WHERE a.name IN query OR query = []' \
                ' RETURN DISTINCT a.name AS querySemantic, a.TUI as queryTUI, a.STN as querySTN, b.name AS semantic,' \
                ' b.TUI AS TUI, b.STN as STN'
        with self.driver.session() as session:
            recds = session.run(query, semantic_id=semantic_id)
            for record in recds:
                try:
                    qqst: QQST = QQST(record.get('queryTUI'), record.get('querySTN'), record.get('semantic'), record.get('TUI'), record.get('STN'))
                    qqsts.append(qqst)
                except KeyError:
                    pass
        return qqsts

    def tui_tui_id_semantics_get(self, tui_id: str) -> [SemanticStn]:
        semanticStns: [SemanticStn] = []
        query = 'WITH [$tui_id] AS query MATCH (a:Semantic)' \
                ' WHERE a.TUI IN query OR query = []' \
                ' RETURN DISTINCT a.name AS semantic, a.TUI AS TUI, a.STN AS STN1'
        with self.driver.session() as session:
            recds = session.run(query, tui_id=tui_id)
            for record in recds:
                try:
                    semanticStn: SemanticStn = SemanticStn(record.get('semantic'), record.get('STN1'))
                    semanticStns.append(semanticStn)
                except KeyError:
                    pass
        return semanticStns

    def terms_term_id_codes_get(self, term_id: str) -> [TermtypeCode]:
        termtypeCodes: [TermtypeCode] = []
        query = 'WITH [$term_id] AS query MATCH (a:Term)<-[b]-(c:Code)' \
                ' WHERE a.name IN query' \
                ' RETURN DISTINCT a.name AS Term, Type(b) AS TermType, c.CodeID AS Code' \
                ' ORDER BY Term, TermType, Code'
        with self.driver.session() as session:
            recds = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    termtypeCode: TermtypeCode = TermtypeCode(record.get('TermType'), record.get('Code'))
                    termtypeCodes.append(termtypeCode)
                except KeyError:
                    pass
        return termtypeCodes

    def terms_term_id_concepts_get(self, term_id: str) -> [str]:
        concepts: [str] = []
        query = 'WITH [$term_id] AS query OPTIONAL MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
                ' WHERE a.name IN query AND b.CUI = d.CUI OPTIONAL MATCH (a:Term)<--(d:Concept) WHERE a.name IN query' \
                ' RETURN DISTINCT a.name AS Term, d.CUI AS Concept' \
                ' ORDER BY Concept ASC'
        with self.driver.session() as session:
            recds = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    concept: str = record.get('Concept')
                    concepts.append(concept)
                except KeyError:
                    pass
        return concepts

    def terms_term_id_concepts_terms_get(self, term_id: str) -> [ConceptTerm]:
        conceptTerms: [ConceptTerm] = []
        query = 'WITH [$term_id] AS query OPTIONAL MATCH (a:Term)<-[b]-(c:Code)<-[:CODE]-(d:Concept)' \
                ' WHERE a.name IN query AND b.CUI = d.CUI OPTIONAL MATCH (a:Term)<--(d:Concept)' \
                ' WHERE a.name IN query WITH a,collect(d.CUI) AS next MATCH (f:Term)<-[:PREF_TERM]-(g:Concept)-[:CODE]->(h:Code)-[i]->(j:Term)' \
                ' WHERE g.CUI IN next AND g.CUI = i.CUI WITH a, g,COLLECT(j.name)+[f.name] AS x WITH * UNWIND(x) AS Term2' \
                ' RETURN DISTINCT a.name AS Term1, g.CUI AS Concept, Term2' \
                ' ORDER BY Term1, Term2'
        with self.driver.session() as session:
            recds = session.run(query, term_id=term_id)
            for record in recds:
                try:
                    conceptTerm: ConceptTerm = ConceptTerm(record.get('Concept'), record.get('Term2'))
                    conceptTerms.append(conceptTerm)
                except KeyError:
                    pass
        return conceptTerms