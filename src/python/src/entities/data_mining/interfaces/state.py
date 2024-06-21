from abc import ABC, abstractmethod

class IState(ABC):
    
    report: str

    @abstractmethod
    def state(self) -> dict[str, str]:
        raise Exception('Should implement property: state')