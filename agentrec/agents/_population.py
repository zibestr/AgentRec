from agents import UserAgent
from agents._abstract import _AbstractPopulation
import configparser
import numpy as np
from random import choices

config = configparser.ConfigParser()
config.read('settings.ini')


class UserPopulation(_AbstractPopulation):
    def __init__(self):
        self.agents = [UserAgent() for _ in range(
            int(config['agents']['InitPopulationSize'])
        )]

    @property
    def size(self) -> int:
        return len(self.agents)

    @property
    def neutral_agents(self) -> int:
        return sum(1 for agent in self.agents
                   if agent.state == agent.States.NEUTRAL)

    @property
    def positive_agents(self) -> int:
        return sum(1 for agent in self.agents
                   if agent.state == agent.States.POSITIVE)

    @property
    def negative_agents(self) -> int:
        return sum(1 for agent in self.agents
                   if agent.state == agent.States.NEGATIVE)

    @property
    def churn_agents(self) -> int:
        return sum(1 for agent in self.agents
                   if agent.state == agent.States.CHURN)

    def iteration(self, recommendations: list,
                  metric_coef: int) -> None:
        for agent, rec in zip(self.agents, recommendations):
            agent.change_state(rec, metric_coef)

        rate = float(config['agents']['NewAgentChance'])
        choice = choices([False, True], weights=[1 - rate, rate], k=1)[0]

        if len(self.agents) <= int(config['agents']['MaxPopulationSize']):
            if choice:
                num_agents = np.random.randint(1, 3)
                self.agents += [UserAgent() for _ in range(num_agents)]
