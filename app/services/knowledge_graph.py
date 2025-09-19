from neo4j import AsyncSession as Neo4jAsyncSession
from app.schemas.concept import Neo4jConcept

class Neo4jKnowledgeGraphService:
    def __init__(self, session: Neo4jAsyncSession):
        self.session = session

    # ... (existing get_learning_context and recommend_next_concept methods remain the same)
    async def get_learning_context(self, concept_name: str) -> dict:
        query = """
        MATCH (c)
        WHERE (c:Topic OR c:Subtopic) AND toLower(c.name) CONTAINS toLower($concept_name)
        WITH c LIMIT 1
        OPTIONAL MATCH (p:Subtopic)-[:PREREQUISITE_FOR]->(c)
        RETURN c as concept, collect(p) as prerequisites
        """
        result = await self.session.run(query, concept_name=concept_name)
        record = await result.single()
        if not record or not record["concept"]:
            return None
        concept_node = record["concept"]
        prereq_nodes = record["prerequisites"]
        prerequisites = [Neo4jConcept.model_validate(node) for node in prereq_nodes]
        return {
            "current_concept": Neo4jConcept.model_validate(concept_node),
            "prerequisites": prerequisites,
        }

    async def recommend_next_concept(self, concept_name: str) -> list[Neo4jConcept]:
        query = """
        MATCH (c)
        WHERE (c:Topic OR c:Subtopic) AND toLower(c.name) CONTAINS toLower($concept_name)
        WITH c LIMIT 1
        MATCH (c)-[:PREREQUISITE_FOR]->(next_concept:Subtopic)
        RETURN next_concept
        """
        result = await self.session.run(query, concept_name=concept_name)
        records = await result.data()
        recommendations = [Neo4jConcept.model_validate(record['next_concept']) for record in records]
        return recommendations

    async def get_learning_path(self, concept_name: str) -> list[Neo4jConcept]:
        query = """
        MATCH (target)
        WHERE (target:Topic OR target:Subtopic) AND toLower(target.name) CONTAINS toLower($concept_name)
        WITH target LIMIT 1
        MATCH p = (start)-[:PREREQUISITE_FOR*1..]->(target)
        UNWIND nodes(p) as concept
        RETURN DISTINCT concept
        """
        result = await self.session.run(query, concept_name=concept_name)
        records = await result.data()
        learning_path = [Neo4jConcept.model_validate(record['concept']) for record in records]
        return learning_path

    # ------------------ NEW METHOD ------------------

    async def get_comprehensive_analysis(self, concept_name: str) -> dict:
        """
        Performs a full analysis of a concept, fetching data from multiple relationships.
        """
        query = """
        MATCH (c)
        WHERE (c:Topic OR c:Subtopic) AND toLower(c.name) CONTAINS toLower($concept_name)
        WITH c LIMIT 1
        OPTIONAL MATCH (p)-[:PREREQUISITE_FOR]->(c)
        OPTIONAL MATCH (c)-[:HAS_SUBTOPIC]->(sub)
        OPTIONAL MATCH (c)-[:USED_WITH]->(related)
        OPTIONAL MATCH (easier)-[:EASIER_THAN]->(c)
        
        RETURN c as concept,
               collect(DISTINCT p) as prerequisites,
               collect(DISTINCT sub) as subtopics,
               collect(DISTINCT related) as related_concepts,
               collect(DISTINCT easier) as easier_alternatives
        """
        result = await self.session.run(query, concept_name=concept_name)
        record = await result.single()

        if not record or not record["concept"]:
            return None

        def to_model_list(nodes):
            # FIXED: Add deduplication based on the unique 'id' property of the nodes
            seen_ids = set()
            unique_nodes = []
            for node in nodes:
                node_id = node.get("id")
                if node_id not in seen_ids:
                    unique_nodes.append(Neo4jConcept.model_validate(node))
                    seen_ids.add(node_id)
            return unique_nodes

        return {
            "target_concept": Neo4jConcept.model_validate(record["concept"]),
            "prerequisites": to_model_list(record["prerequisites"]),
            "subtopics": to_model_list(record["subtopics"]),
            "related_concepts": to_model_list(record["related_concepts"]),
            "easier_alternatives": to_model_list(record["easier_alternatives"]),
        }
        """
        Performs a full analysis of a concept, fetching data from multiple relationships.
        """
        # This single, efficient query uses OPTIONAL MATCH for each relationship type.
        query = """
        MATCH (c)
        WHERE (c:Topic OR c:Subtopic) AND toLower(c.name) CONTAINS toLower($concept_name)
        WITH c LIMIT 1
        // Gather all related nodes into collections
        OPTIONAL MATCH (p)-[:PREREQUISITE_FOR]->(c)
        OPTIONAL MATCH (c)-[:HAS_SUBTOPIC]->(sub)
        OPTIONAL MATCH (c)-[:USED_WITH]->(related)
        OPTIONAL MATCH (easier)-[:EASIER_THAN]->(c)
        
        RETURN c as concept,
               collect(DISTINCT p) as prerequisites,
               collect(DISTINCT sub) as subtopics,
               collect(DISTINCT related) as related_concepts,
               collect(DISTINCT easier) as easier_alternatives
        """
        result = await self.session.run(query, concept_name=concept_name)
        record = await result.single()

        if not record or not record["concept"]:
            return None

        # Helper to convert a list of nodes to a list of Pydantic models
        def to_model_list(nodes):
            return [Neo4jConcept.model_validate(node) for node in nodes]

        return {
            "target_concept": Neo4jConcept.model_validate(record["concept"]),
            "prerequisites": to_model_list(record["prerequisites"]),
            "subtopics": to_model_list(record["subtopics"]),
            "related_concepts": to_model_list(record["related_concepts"]),
            "easier_alternatives": to_model_list(record["easier_alternatives"]),
        }