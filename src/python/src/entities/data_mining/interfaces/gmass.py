from abc import ABC, abstractmethod

class IGmass(ABC):
    
    report:str
        
    @abstractmethod
    def gmass(self) -> dict[str, float]:
        raise Exception('Should implement property: gmass')