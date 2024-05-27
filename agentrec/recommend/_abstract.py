from abc import ABC, abstractmethod
from agents._abstract import _AbstractPopulation
import configparser
from joblib import Parallel, delayed

config = configparser.ConfigParser()
config.read('settings.ini')


class _AbstactRecommendationAlgorithm(ABC):
    def __init__(self, population: _AbstractPopulation) -> None:
        self._population = population
        cpu_count = int(config['backend']['CPUCount'])
        self._parallel_backend = Parallel(n_jobs=cpu_count,
                                          backend='threading',
                                          return_as='list',
                                          prefer='threads')

    @abstractmethod
    def make_recommendation(self, user_number: int) -> int | None:
        raise NotImplementedError

    @abstractmethod
    def train(self):
        raise NotImplementedError

    def get_recommendations(self) -> list:
        return self._parallel_backend(delayed(self.make_recommendation)(i)
                                      for i in range(self._population.size))
