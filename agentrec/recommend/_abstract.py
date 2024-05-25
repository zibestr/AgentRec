from abc import ABC, abstractmethod
from agents._abstract import _AbstractPopulation
import numpy as np


class _AbstactRecommendationAlgorithm(ABC):
    def __init__(self, population: _AbstractPopulation) -> None:
        self._population = population

    @abstractmethod
    def make_recommendation(self, user_number: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def train(self):
        raise NotImplementedError

    def get_recommendations(self) -> list:
        result = []
        for i in range(self._population.size):
            result.append(self.make_recommendation(i))
        return result
