from sqlalchemy.ext.asyncio import AsyncSession

# --- CORRECTED ---
# This now imports the correctly named session factory.
from app.db.session import SessionLocal
from app.crud.crud_concept import concept as crud_concept
from app.schemas.concept import ConceptCreate

async def init_db() -> None:
    """Initializes the database with some basic concepts if they don't exist."""
    async with SessionLocal() as db:
        concepts = [
            ("Basic Arithmetic", "Fundamental operations like addition, subtraction, etc."),
            ("Fractions and Decimals", "Representing parts of a whole."),
            ("Basic Algebra", "Using variables to represent numbers."),
            ("Linear Equations", "Equations of a straight line."),
            ("Quadratic Equations", "Equations with a second-degree term."),
        ]
        
        for name, desc in concepts:
            existing_concept = await crud_concept.get_by_name(db, name=name)
            if not existing_concept:
                concept_in = ConceptCreate(name=name, description=desc)
                await crud_concept.create(db, obj_in=concept_in)