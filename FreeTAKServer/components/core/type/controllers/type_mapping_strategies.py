from enum import Enum

class MappingStrategies(Enum):
    CACHING = "CachingMapping"
    MEMORY = "MemoryMapping"
    DATABASE = "DatabaseMapping"