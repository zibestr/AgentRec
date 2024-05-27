from agents._abstract import _AbstractPopulation
import tkinter as tk
import configparser

config = configparser.ConfigParser()
config.read('settings.ini')


class PopulationApp(tk.Frame):
    def __init__(self,
                 population: _AbstractPopulation,
                 master=None):
        super().__init__(master)
        master.title('Population Dynamic')
        master.geometry(config['app']['WindowSize'])
        self.population = population

        self.pack()

        canvas_size = tuple(map(int, config['app']['CanvasSize'].split('x')))
        self.canvas = tk.Canvas(self,
                                height=canvas_size[0],
                                width=canvas_size[1])
        self.canvas.pack()

        self.speed_slider = tk.Scale(self,
                                     from_=1, to=20,
                                     orient='horizontal')
        self.speed_slider.set(1)
        self.speed_slider.pack()

        self.metric_slider = tk.Scale(self,
                                      from_=1, to=5,
                                      orient='horizontal')
        self.metric_slider.set(1)
        self.metric_slider.pack()

    @property
    def modeling_speed(self) -> int:
        return 100 // int(self.speed_slider.get())

    @property
    def metric_coef(self) -> int:
        return int(self.metric_slider.get())

    def draw(self):
        self.canvas.delete("all")
        for agent in self.population.agents:
            self.canvas.create_oval(
                agent.coords[0],
                agent.coords[1],
                agent.coords[0] + int(config['app']['AgentSize']),
                agent.coords[1] + int(config['app']['AgentSize']),
                fill=agent.color
            )
