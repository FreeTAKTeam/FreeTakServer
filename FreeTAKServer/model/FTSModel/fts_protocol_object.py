from abc import ABC, abstractmethod

class FTSProtocolObject(ABC):
    def __init__(self, structure ):
		for item, key in structure:
			setattr(self, key, item)