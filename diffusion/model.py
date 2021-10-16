from mesa import Model
from mesa.time import SimultaneousActivation
from mesa.space import SingleGrid
from .agent import Environment


class Diffusion(Model):
    def __init__(
        self,
        height=50,
        width=50,
        evaporate=0.07,
        diffusion=0.3,
        initdrop=500,
        lowerbound=0.01,
    ):

        super().__init__()

        self.evaporate = evaporate
        self.diffusion = diffusion
        self.initdrop = initdrop
        self.lowerbound = lowerbound

        # create empty schedule
        self.schedule = SimultaneousActivation(self)

        # define grid
        self.grid = SingleGrid(height, width, torus=True)

        # iter through grid, and place agent in each spot
        for (_, x, y) in self.grid.coord_iter():
            # create agent
            cell = Environment((x, y), self)
            if self.random.random() < 0.01:
                cell.add(self.initdrop)
            self.grid.place_agent(cell, (x, y))
            self.schedule.add(cell)

        self.running = True

    def step(self):
        self.schedule.step()


# note: this is why the guy wants to pass x, y, into agent class, he's using it to keep track
# he uses pos of an agent to find its nighbours
