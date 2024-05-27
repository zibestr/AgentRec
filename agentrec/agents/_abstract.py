from abc import ABC, abstractmethod
from enum import Enum


class _AbstractAgent(ABC):
    class States(Enum):
        START = 0
        END = -1

    def __init__(self):
        self._state = self.States.START

    @abstractmethod
    def change_state(self,
                     recommendation: int | None,
                     metric_coef: int) -> None:
        raise NotImplementedError

    @property
    def state(self) -> int:
        return self._state


class _AbstractPopulation(ABC):
    agents: list[_AbstractAgent]

    @abstractmethod
    def iteration(self, recommendations, metric_coef: int) -> None:
        raise NotImplementedError
