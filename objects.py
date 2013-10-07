import random

# A starter environmental concentrations dictionary.
# Based on the standard LB medium.
# http://en.wikipedia.org/wiki/Lysogeny_broth
ENVR = {'H+': 10**-7.4,
        'NaCl': 3.3*10**-3,
        'CO2': 0,
        'O2': 0,
        'Glc': 3*10**-3,
        'Fru': 0,
        'Lac': 0,
        'AAs': 9.6*10**-2,
        'N': 0,
        'P': 0,
        'EtOH': 0}

RESLIST = ['H+', 'NaCl', 'CO2', 'O2', 'Glc', 'Fru', 'Lac', 'AAs', 'N', 'P', 'EtOH']

# A starter internal cellular concentrations dictionary.
# Based on E. coli.
# Each resource has a dictionary containing min/max/current values.
# All values are in mol/L and are based on the following research article:
# http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2754216/
CELLR = {'H+':  {'current': 10**-7.5,
                 'minLive': 10**-7.0,
                 'minGrow': 10**-7.2,
                 'maxGrow': 10**-7.8,
                 'maxLive': 10**-8.0},
         'NaCl':{'current': 5*10**-3,
                 'minLive': 10**-3,
                 'minGrow': 3*10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
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
                 'maxLive': 10**-1},
         'EtOH':{'current': 0,
                 'minLive': 0,
                 'minGrow': 0,
                 'maxGrow': 1.09,   # These correspond to ~6% and ~10% ABV
                 'maxLive': 1.71}}

# Some resources diffuse freely across membranes.
DIFFUSES = ['CO2', 'O2', 'EtOH']


class Operon:
    """Represents a bacterial operon"""

    def __init__(self, name, size, energyRequired, transports):
        self.name = name
        self.size = size
        self.atpReq = energyRequired
        self.trans = transports
        self.on = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # Turns the operon off if it is capable of doing so.
    def turnOff(self):
        if self.trans not in DIFFUSES:
            self.on = False

    def turnOn(self):
        self.on = True

    def canPassTrans(self, r=False):
        if r:
            return (not self.atpReq) and (self.trans == r) and (self.on)
        else:
            return (not self.atpReq) and (self.on)


class Organism:
    """Represents organism populations"""

    def __init__(self, name, ops, res, count=100, cVol=6*10**-13):
        self.name = name
        self.count = count
        self.cVol = cVol
        self.ops = ops
        self.res = res
        self.gSize = sum([x.size for x in ops])

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def print_res(self):
        for key in self.res:
            print key + ":\t" + str(self.res[key]['current'])

    # Returns the current total volume of the population.
    def vol(self):
        return self.cVol * self.count

    # Takes a resource string (like 'H+') and returns True if it can currently
    # undergo passive transport into or out of the organism.
    def canPass(self, r):
        for op in self.ops:
            # Only return True if it can tranport r.
            if op.canPassTrans(r):
                return True

        # Return False if all operons are checked and none fit the bill.
        return False

    # Takes a resource string and closes all passive channels for the resource.
    def close(self, r):
        for op in self.ops:
            if (op.trans == r) and (not op.atpReq):
                op.turnOff()

    # Opens all passive channels for the resource.
    def open(self, r):
        for op in self.ops:
            if (op.trans == r) and (not op.atpReq):
                op.turnOn()

    # Returns a dictionary of the resources available for pooling (i.e. with
    # open channels), with the value being a tuple of the moles and volume.
    def resAvailable(self):
        resToPool = dict(zip(RESLIST, [(0,0) for x in RESLIST]))
        for op in self.ops:
            if op.canPassTrans():
                resToPool[op.trans] = (self.res[op.trans]['current'] * self.vol(), self.vol())
        return resToPool

    # Updates the organism's internal resources to the new environment,
    # according to which channels are open.
    def setRes(self, envRes):
        for res in envRes:
            if self.canPass(res):
                self.res[res]['current'] = envRes[res]


    # Adds/removes resources from both the cell and the "checked out"
    # environmental resources dictionary.  Then returns the updated dictionary.
    # Organisms will try to adjust their internal resources within minGrow and
    # maxGrow for that resource, but are limited by concentrations and genes.
    def exchange(self, envRes):
        return envRes


class Environment:
    """Represents a microbiological environment"""

    def __init__(self, name, vol, res, temp, light):
        self.name = name
        self.vol = vol
        self.res = res
        self.temp = temp
        self.light = light

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # Returns a list of dictionaries, one for each organism in the community.
    # Each dictionary contains the moles of resources available to that organism
    # for the current step.  Organisms essentially "check out" a resource
    # dictionary, actively add/remove resources, then return it to the environment.
    def partition(self, community):
        # Find the proportion of each organism by volume
        volumes = [org.vol() for org in community.orgs]
        total = sum(volumes)
        proportions = [x/total for x in volumes]

        # Then build a dictionary for each organism, giving it resources
        # proportional to its fractional volume.
        # Environmental concentrations are included to figure out diffusion.
        resources = [{} for org in proportions]
        for i in range(len(resources)):
            for key in self.res:
                resources[i][key] = (self.res[key] * self.vol * proportions[i], self.res[key])
        return resources

    # Updates the environmental resources
    def update(self, resources):
        return resources


class Ecosystem:
    """A collection of organism populations and their environment"""

    def __init__(self, orgs, env):
        self.orgs = orgs
        self.env = env

    def equalize(self):
        newRes = [org.resAvailable() for org in self.orgs]
        for r in self.env.res:
            self.env.res[r] = ((sum([o[r][0] for o in newRes]) + 
                               self.env.res[r] * self.env.vol)/
                               (sum([o[r][1] for o in newRes]) + self.env.vol))
        for org in self.orgs:
            org.setRes(self.env.res)



# Define all the operons.
# Some of these are non-existant, particularly the diffusion ones.
# They simplify calculations, and act as no-sized, non-ATP-consuming transporters.
operons = [Operon('CO2 Diffusion', 0, 0, 'CO2'),
           Operon('O2 Diffusion', 0, 0, 'O2'),
           Operon('EtOH Diffusion', 0, 0, 'EtOH'),
           Operon('Amino acid transporters', 500, 0, 'AAs'),
           Operon('Glucose transporter', 500, 0, 'Glc'),
           Operon('NaCl channel', 500, 0, 'NaCl')]

# Default organisms
eColi = Organism('E. coli', dict(zip(operons, [1 for op in operons])), CELLR)
cDiff = Organism('C. diff', dict(zip(operons, [1 for op in operons])), CELLR)
print 'Before:'
eColi.print_res()
#print 'cDiff'
#cDiff.print_res()
env = Environment('Lab', 1, ENVR, 37, True)
comm = Ecosystem([eColi,cDiff], env)
comm.equalize()
print 'After:'
eColi.print_res()
#print 'cDiff'
#cDiff.print_res()
