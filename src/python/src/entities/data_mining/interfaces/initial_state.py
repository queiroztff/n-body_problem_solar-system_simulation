from abc import ABC, abstractmethod

class IInitialState(ABC):
    
    report: str
    
    @abstractmethod
    def initial_state(self) -> dict[str, str]:
        raise Exception('Should implement property: initial_state')
    
        