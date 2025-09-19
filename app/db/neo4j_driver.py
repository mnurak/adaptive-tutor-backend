from neo4j import AsyncGraphDatabase, AsyncDriver
from app.core.config import settings

class Neo4jDriver:
    _driver: AsyncDriver | None = None

    def get_driver(self) -> AsyncDriver:
        """Returns the singleton AsyncDriver, creating it if necessary."""
        if self._driver is None:
            print("Initializing Neo4j driver...")
            try:
                self._driver = AsyncGraphDatabase.driver(
                    settings.NEO4J_URI,
                    auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD)
                )
                print("Neo4j driver initialized.")
            except Exception as e:
                print(f"Failed to initialize Neo4j driver: {e}")
                raise
        return self._driver

    async def close(self):
        """Closes the Neo4j driver connection."""
        if self._driver is not None and not self._driver.closed():
            print("Closing Neo4j driver...")
            await self._driver.close()
            self._driver = None
            print("Neo4j driver closed.")

# Create a global instance of the driver
neo4j_driver = Neo4jDriver()

# Dependency for FastAPI to inject a session
async def get_neo4j_session():
    driver = neo4j_driver.get_driver()
    async with driver.session() as session:
        yield session