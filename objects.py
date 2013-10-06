import random

# A base environmental concentrations dictionary.
# Emulates the laboratory standard LB medium.
# http://en.wikipedia.org/wiki/Lysogeny_broth
ENVC = {'H+': 10**-7.4,
        'CO2': 0,
        'O2': 0,
        'Glc': 3*10**-3,
        'Fru': 0,
        'Lac': 0,
        'AAs': 9.6*10**-2,
        'N': 0,
        'P': 0,
        'NaCl': 3*10**-3}

# A base internal cellular concentrations dictionary.
# Each resource has a dictionary containing min/max/current values.
# All values are in mol/L and are based on the following research article:
# http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2754216/
CELLC = {'H+':  {'current': 10**-7.5,
                 'minLive': 10**-7.0,
                 'minGrow': 10**-7.2,
                 'maxGrow': 10**-7.8,
                 'maxLive': 10**-8.0},
         'ATP': {'current': 8*10**-3,
                 'minLive': 5*10**-4,
                 'minGrow': 2*10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'CO2': {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-3,
                 'maxLive': 10**-2},
         'O2':  {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-3,
                 'maxLive': 10**-2},
         'Glc': {'current': 8*10**-3,
                 'minLive': 0,
                 'minGrow': 10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Fru': {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Lac': {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'AAs': {'current': 1.5*10**-1,
                 'minLive': 10**-2,
                 'minGrow': 10**-1,
                 'maxGrow': 2*10**-1,
                 'maxLive': 3*10**-1},
         'N':   {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1},
         'P':   {'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1}}



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

    # Returns a list of dictionaries, one for each organism in the community.
    # Each dictionary contains the moles of resources available to that organism
    # for the current step.
    def partition(self, community):
        # Find the proportion of each organism by volume
        volumes = [org.volume() for org in community.organisms]
        total = sum(volumes)
        proportions = [ind/total for ind in volumes]

        # Then build a dictionary for each organism, giving it resources
        # proportional to its fractional volume.
        dList = [{} for org in proportions]
        for i in range(len(dList)):
            for key in self.conc:
                dList[i][key] = self.conc[key] * proportions[i]
        return dList

    # Takes 
    def update(self, ):
        return 


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

    def exchange(self, conc):
        return 0


class Operon:
    """Represents a bacterial operon"""

    def __init__(self, name, size, effects):
        self.name = name
        self.size = size
        self.effects = effects


# Define all the operons
operons = {}

# Default organisms
eColi = Organism('E. coli', [], CELLC)
cDiff = Organism('C. diff', [], CELLC, 200)
comm = Community([eColi,cDiff])
print comm.organisms
env = Environment('Lab', 1, ENVC, 37, True)
print env.partition(comm)