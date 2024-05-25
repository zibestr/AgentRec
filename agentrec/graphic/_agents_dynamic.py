from agents._abstract import _AbstractPopulation
import matplotlib.pyplot as plt
import numpy as np


class AgentPlot:
    def __init__(self,
                 population: _AbstractPopulation,
                 figsize: tuple[int, int] = (8, 6)):
        self.figure = plt.figure(figsize=figsize)
        self.population = population
        self.axes = self.figure.add_axes(plt.Axes(self.figure, 111))
        self.iteration = 0
        self.neutral_history: list[int] = []
        self.positive_history: list[int] = []
        self.negative_history: list[int] = []
        self.churn_history: list[int] = []

    def update(self):
        self.iteration += 1

        self.neutral_history.append(
            self.population.neutral_agents
        )
        self.positive_history.append(
            self.population.positive_agents
        )
        self.negative_history.append(
            self.population.negative_agents
        )
        self.churn_history.append(
            self.population.churn_agents
        )

    def draw(self):
        self.axes.clear()

        self.axes.plot(np.arange(1, self.iteration + 1),
                       self.neutral_history,
                       c='blue',
                       label='Neutral')

        self.axes.plot(np.arange(1, self.iteration + 1),
                       self.positive_history,
                       c='green',
                       label='Positive')

        self.axes.plot(np.arange(1, self.iteration + 1),
                       self.negative_history,
                       c='red',
                       label='Negative')

        self.axes.plot(np.arange(1, self.iteration + 1),
                       self.churn_history,
                       c='gray',
                       label='Churn')

        self.axes.grid()
        self.figure.draw(self.figure.canvas.get_renderer())
        self.figure.legend()
