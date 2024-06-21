from abc import ABC, abstractmethod
from typing import Dict, List, Union

class ISpkIdSearch(ABC):
    
    @abstractmethod
    def get_data(self) -> Dict[str, Union[str, List[Dict[str, str]]]]:
        raise NotImplementedError('Should implement method: get_data')