from expriment.Expriment import Expriment
from expriment.RegLogger import RegLogger
import os

expriments = [
    {
        'loss':"MSE"
    },
    {
        'loss':"ICE",
        'sigma':5
    },
    {
        'loss':"ICE",
        'sigma':4.5
    },
    {
        'loss':"ICE",
        'sigma':4.2
    },
    {
        'loss':"ICE",
        'sigma':4.0
    },
    {
        'loss':"ICE",
        'sigma':3.5
    },
    {
        'loss':"ICE",
        'sigma':1
    },
]

logger = RegLogger(os.path.join(os.getcwd(), 'logs'))

for e in expriments:
    exp = Expriment(logger, **e)
    exp.fit()
    exp.save()
    