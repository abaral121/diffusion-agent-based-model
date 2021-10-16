from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from .model import Diffusion
import math


def log_norm(value, lower, upper):
    value = min(value, upper)
    value = max(value, lower)
    lower_log = math.log(lower)
    upper_log = math.log(upper)
    value_log = math.log(value)

    return (value_log - lower_log) / (upper_log - lower_log)


def diffusion_portrayal(agent):
    if agent is None:
        return
    portrayal = {"Shape": "rect", "w": 1, "h": 1, "Filled": "True", "Layer": 0}

    red = int(
        log_norm(agent.amount, agent.model.lowerbound, agent.model.initdrop) * 255
    )

    portrayal["Color"] = "#FF%02x%02x" % (255 - red, 255 - red)

    return portrayal


canvas_element = CanvasGrid(diffusion_portrayal, 50, 50, 500, 500)


model_params = {
    "height": 50,
    "width": 50,
    "evaporate": UserSettableParameter(
        "slider", "Evaporation rate", 0.07, 0.1, 0.30, 0.01
    ),
    "diffusion": UserSettableParameter(
        "slider", "Diffusion rate", 0.03, 0.0, 1.0, 0.10
    ),
    "initdrop": UserSettableParameter("slider", "Initial Drop", 500, 100, 1000, 50),
}


server = ModularServer(Diffusion, [canvas_element], "Chemical Diffusion", model_params)
