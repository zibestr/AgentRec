from agents._abstract import _AbstractAgent
from enum import Enum
import numpy as np
from random import choices
import configparser
from time import time

config = configparser.ConfigParser()
config.read('settings.ini')


class UserAgent(_AbstractAgent):
    class States(Enum):
        NEUTRAL = 0
        POSITIVE = 1
        NEGATIVE = 2
        CHURN = -1

    def __init__(self):
        self._state = self.States.NEUTRAL
        self.ratings = self._generate_ratings()
        self._dissatisfaction = 0

        max_coord = (max(map(int, config['app']['CanvasSize'].split('x')))
                     - int(config['app']['AgentSize']) - 5)
        self.coords = np.random.uniform(
            low=0,
            high=max_coord,
            size=2
        )

    @property
    def color(self) -> str:
        match self._state:
            case self.States.NEUTRAL:
                return 'blue'
            case self.States.POSITIVE:
                return 'green'
            case self.States.NEGATIVE:
                return 'red'
            case self.States.CHURN:
                return 'gray'
        return 'black'

    @staticmethod
    def _generate_ratings() -> np.ndarray:
        ratings = np.random.randint(
            size=int(config['products']['ProductsCount']),
            low=int(config['products']['MinRate']),
            high=int(config['products']['MaxRate']) + 1,
            dtype=np.int16
        )

        undefined_count = np.random.randint(
            low=int(config['products']['MinUndefinedRateCount']),
            high=int(config['products']['MaxUndefinedRateCount']) + 1
        )
        undefined_inds = np.arange(int(config['products']['ProductsCount']))
        np.random.shuffle(undefined_inds)
        undefined_inds = undefined_inds[:undefined_count]

        ratings[undefined_inds] = int(config['products']['UndefinedRate'])

        return ratings

    def _change_rating(self) -> None:
        count_products = int(config['products']['ProductsCount'])
        rate = float(config['agents']['RateChangeChance'])

        distribution = [None] + list(range(count_products))
        p = [1 - rate] + [rate / count_products] * count_products
        choice = choices(distribution, weights=p, k=1)[0]

        if choice is not None:
            self.ratings[choice] = np.random.randint(
                low=int(config['products']['MinRate']),
                high=int(config['products']['MaxRate']) + 1
            )

    def _metric_recommendations(self,
                                recommendation: int | None) -> None:
        # TODO: mechanism of rating recommendation
        if recommendation is not None:
            buffer = self.ratings.copy()
            np.random.shuffle(buffer)
            rate = (sum([x ** i for i, x in enumerate(buffer)]) + time()) % 6
            rate = 1 if rate == 0 else rate
            self.ratings[recommendation] = rate
            if rate <= int(config['products']['NegativeRate']):
                self._state = self.States.NEGATIVE
            elif rate == int(config['products']['NeutralRate']):
                self._state = self.States.NEUTRAL
            elif rate >= int(config['products']['PositiveRate']):
                self._state = self.States.POSITIVE

    def change_state(self,
                     recommendation: int | None) -> None:
        if self._state != self.States.CHURN:
            self._metric_recommendations(recommendation)

            self._change_rating()

            if self._state == self.States.NEGATIVE:
                self._dissatisfaction += 1
                if self._dissatisfaction > int(config['agents']
                                               ['DaysBeforeChurn']):
                    self._state = self.States.CHURN
            else:
                self._dissatisfaction -= 1 if self._dissatisfaction > 0 else 0
