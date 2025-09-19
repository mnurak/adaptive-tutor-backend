from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import select
from app.db.session import AsyncSessionLocal
from app.models.concept import Concept

async def init_db() -> None:
    """
    Initializes the database with predefined concepts and their relationships.
    This version uses a two-pass approach to be robust against initialization errors.
    """
    concepts_data = {
        "Basic Arithmetic": {"description": "Fundamental operations.", "prerequisites": []},
        "Fractions and Decimals": {"description": "Understanding parts of a whole.", "prerequisites": ["Basic Arithmetic"]},
        "Basic Algebra": {"description": "Using variables to represent numbers.", "prerequisites": ["Basic Arithmetic"]},
        "Linear Equations": {"description": "Solving equations of the form ax + b = c.", "prerequisites": ["Basic Algebra"]},
        "Quadratic Equations": {"description": "Solving second-degree equations.", "prerequisites": ["Linear Equations"]},
        "Calculus Intro": {"description": "The study of continuous change.", "prerequisites": ["Quadratic Equations"]},
        "Derivatives": {"description": "Finding rates of change.", "prerequisites": ["Calculus Intro"]},
    }

    async with AsyncSessionLocal() as db:
        # Pass 1: Ensure all Concept objects exist in the database.
        for name, data in concepts_data.items():
            result = await db.execute(select(Concept).filter(Concept.name == name))
            concept = result.scalars().first()
            if not concept:
                db.add(Concept(name=name, description=data["description"]))
        await db.commit()

        # Pass 2: Now that all concepts are committed, build the relationships.
        # Query all concepts again, this time eager-loading the relationship.
        stmt = select(Concept).options(selectinload(Concept.prerequisites))
        result = await db.execute(stmt)
        concepts_map = {c.name: c for c in result.scalars().all()}

        for name, data in concepts_data.items():
            current_concept = concepts_map[name]
            for prereq_name in data["prerequisites"]:
                prereq_concept = concepts_map[prereq_name]
                if prereq_concept not in current_concept.prerequisites:
                    current_concept.prerequisites.append(prereq_concept)
        
        await db.commit()