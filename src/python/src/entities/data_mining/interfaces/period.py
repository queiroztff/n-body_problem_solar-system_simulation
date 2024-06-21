from abc import ABC, abstractmethod

class IPeriod(ABC):
    
    report: str

    @abstractmethod
    def period(self) -> dict[str, float]:
        raise Exception('Should implement property: period')