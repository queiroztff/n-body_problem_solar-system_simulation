from abc import ABC, abstractmethod

class IMass(ABC):
    
    report: str
    
    @abstractmethod
    def mass(self) -> dict[str, float]:
        raise Exception('Should implement property: mass')

