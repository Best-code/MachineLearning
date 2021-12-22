from typing import List
from random import choices

#https://www.youtube.com/watch?v=nhT56blfRpE

Genome = List[int]
Population = List[Genome]
Thing = namedtuple("Thing",['name','value','weight'])

things = [
    Thing('Laptop',500,2200),
    Thing('Headphones',150,160),
    Thing('Coffee Mug',60,350),
    Thing('Notepad',40,333),
    Thing('Water Bottle',30,192),
    ]

def generateGenome(length):
    return choices([0,1], k=length)

def generatePopulations(size,genomeLength):
    return [generateGenome(genomeLength) for _ in range(size)]

def fitness(genome,things,weightLimit):
    if len(genome) != len(things):
        raise ValueError("Genoem and things must be of the same length")
    weight = 0
    value = 0
    for i, thing in enumerate(things):
        if genome[i] == 1:
            weight += things.weight
            value += thing.value
            
            if weight > weightLimit:
                return 0
            
    return value


