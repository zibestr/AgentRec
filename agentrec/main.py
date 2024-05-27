from agents import UserPopulation
from graphic import PopulationApp, AgentPlot
from recommend import ClusteringSystem
import matplotlib.pylab as plt
import tkinter as tk


def update(app: PopulationApp,
           graphic: AgentPlot,
           population: UserPopulation,
           algorithm: ClusteringSystem,
           iteration: int) -> None:
    if population.churn_agents < population.size or iteration < 900:
        metric_coef = app.metric_coef
        algorithm.train()
        recommendations = algorithm.get_recommendations()
        population.iteration(recommendations, metric_coef)
        app.update()
        graphic.update()
        app.draw()
    root_app.after(app.modeling_speed, update,
                   app,
                   graphic,
                   population,
                   algorithm,
                   iteration + 1)


if __name__ == '__main__':
    population = UserPopulation()
    root_app = tk.Tk()

    app = PopulationApp(population, master=root_app)
    graphic = AgentPlot(population)
    algorithm = ClusteringSystem(population)

    update(
        app,
        graphic,
        population,
        algorithm,
        0
    )
    app.mainloop()

    graphic.draw()
    plt.show()
