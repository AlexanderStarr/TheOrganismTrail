import random

# Blank concentrations dictionary
concs = {'H+':0,
         'CO2':0,
         'O2':0,
         'Glc':0,
         'Fru':0,
         'Lac':0,
         'AAs':0,
         'N':0,
         'P':0}



class Environment:
    """Represents a microbiological environment"""

    def __init__(self, name, volume, conc, temp, light):
        self.name = name
        self.volume = volume
        self.conc = conc
        self.temp = temp
        self.light = light

    def __str__(self):
        return self.name

    def remove():
        return conc

    def add():
        return conc


class Community:
    """A collection organism populations"""

    def __init__(self, organisms):
        self.organisms = organisms


class Organism:
    """Represents organism populations"""

    def __init__(self, name, operons, conc, count=100, cellVolume=6*10**-13):
        self.name = name
        self.count = count
        self.cellVolume = cellVolume
        self.operons = operons
        self.conc = conc
        self.genomeSize = sum([x.size for x in operons])

    def __str__(self):
        return self.name

    def volume(self):
        return self.cellVolume * self.count

    def uptake(self, env):
        return 0

    def expel(self):
        return


class Operon:
    """Represents a bacterial operon"""

    def __init__(self, name, size, effects):
        self.name = name
        self.size = size
        self.effects = effects


# Define all the operons
operons = {}

# Default organisms
eColi = Organism('E. coli', [], {'atp':100})