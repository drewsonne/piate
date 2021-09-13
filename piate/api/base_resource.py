from abc import abstractmethod
from typing import Dict


class BaseResource:
    @property
    @abstractmethod
    def PATH(self):
        ...

    def _post(self, path: str, param: Dict):
        pass
