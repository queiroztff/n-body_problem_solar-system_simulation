from abc import ABC, abstractmethod

class IBodyFeatures(ABC):

    @abstractmethod
    def get_report(self) -> str:
        raise NotImplementedError('Should implement method: get_data')