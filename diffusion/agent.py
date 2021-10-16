from mesa import Agent


class Environment(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
        self.amount = 0.0

    def step(self):
        # getting pheremons from agent
        all_p = self.amount
        neighbors = self.model.grid.get_neighbors(self.pos, True)

        # sum all neighbor p amounts and get avg
        for n in neighbors:
            all_p += n.amount
        ave_p = all_p / (len(neighbors) + 1)

        # calculates diff between agent and the avg neighbor p vals
        self._nextAmount = (1 - self.model.evaporate) * (
            self.amount + (self.model.diffusion * (ave_p - self.amount))
        )

        if self._nextAmount < self.model.lowerbound:
            self._nextAmount = 0

    def advance(self):
        self.amount = self._nextAmount

    def add(self, amount):
        self.amount += amount

    def get_pos(self):
        return self.pos
