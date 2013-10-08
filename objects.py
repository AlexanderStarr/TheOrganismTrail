import random

# A starter environmental resources dictionary.
# All values are mol/L, except Temp and Lux, which are in Kelvin and Lux.
# Based on standard LB medium and standard growth conditions.
# http://en.wikipedia.org/wiki/Lysogeny_broth
ENVR = {'H+'  : 10**-7.4,
        'K+'  : 3.3*10**-3,
        'Na+' : 1.8*10**-1,
        'Cl-' : 1.8*10**-1,
        'CO2' : 0.0,
        'O2'  : 0.0,
        'Glc' : 3.3*10**-3,
        'Fru' : 0.0,
        'Lac' : 0.0,
        'AAs' : 9.7*10**-2,
        'N'   : 0.0,
        'P'   : 0.0,
        'EtOH': 0.0,
        'Temp': 310.0,
        'Lux' : 1000.0}

RESLIST = ENVR.keys()

# A starter internal cellular concentrations dictionary.
# Based on Escherichia coli.
# Each resource has a dictionary containing min/max/current values.
# All values are in mol/L and are based on the following research article:
# http://www.ncbi.nlm.nih.gov/pmc/articles/PMC2754216/
CELLR = {'H+':  {'current': 10**-7.4,
                 'minLive': 10**-8.0,
                 'minGrow': 10**-7.8,
                 'maxGrow': 10**-7.2,
                 'maxLive': 10**-7.0},
         'K+':  {'current': 2.1*10**-1,
                 'minLive': 10**-1,
                 'minGrow': 1.5*10**-1,
                 'maxGrow': 2.5*10**-1,
                 'maxLive': 3*10**-1},
         'Na+': {'current': 5*10**-3,
                 'minLive': 10**-3,
                 'minGrow': 3*10**-3,
                 'maxGrow': 1.4*10**-2,
                 'maxLive': 2*10**-2},
         'Cl-': {'current': 5*10**-3,
                 'minLive': 10**-3,
                 'minGrow': 3*10**-3,
                 'maxGrow': 1.4*10**-2,
                 'maxLive': 2*10**-2},
         'ATP': {'current': 8*10**-3,
                 'minLive': 5*10**-4,
                 'minGrow': 2*10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'CO2': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-3,
                 'maxLive': 10**-2},
         'O2':  {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-3,
                 'maxLive': 10**-2},
         'Glc': {'current': 8*10**-3,
                 'minLive': 0.0,
                 'minGrow': 10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Fru': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Lac': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'AAs': {'current': 1.5*10**-1,
                 'minLive': 10**-2,
                 'minGrow': 10**-1,
                 'maxGrow': 2*10**-1,
                 'maxLive': 3*10**-1},
         'N':   {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1},
         'P':   {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1},
         'EtOH':{'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 1.09,   # These correspond to ~6%...
                 'maxLive': 1.71},  # ...and ~10% ABV
         'Temp':{'current': 310.0,
                 'minLive': 273.0,
                 'minGrow': 281.0,
                 'maxGrow': 318.0,
                 'maxLive': 344.0},
         'Lux' :{'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**5,
                 'maxLive': 1.7*10**5}}

# Some resources diffuse freely across membranes.
DIFFUSES = ['CO2', 'O2', 'EtOH', 'Lux', 'Temp']


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

    def __init__(self, name, ops, res, count=100, cVol=6.5*10**-16):
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

    def print_channels(self):
        print "Res\tOpen?\t[Res]"
        for op in self.ops:
            if op.trans:
                print op.trans + "\t" + str(op.on) + "\t" + str(self.res[op.trans]['current'])


    # Returns the current total volume of the population.
    def vol(self):
        return self.cVol * self.count

    # Returns the current concentration of ATP, as this is often needed.
    def atp(self):
        return self.res['ATP']['current']

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

    # Returns True if that resource concentration is not lethal to the organism.
    def isLivable(self, r, conc):
        return self.res[r]['minLive'] <= conc <= self.res[r]['maxLive']

    # Returns True if the resource concentration does not limit growth.
    def isIdeal(self, r, conc):
        return self.res[r]['minGrow'] <= conc <= self.res[r]['maxGrow']

    # Takes an environmental resource dictionary and closes/opens channels
    # according concentrations and cellular needs.
    def setChannels(self, envRes):
        for op in self.ops:
            # Checks that the operon is for a passive transporter.
            if op.trans and not op.atpReq:
                r = op.trans                     # Shorthand for the resource.
                current = self.res[r]['current'] # Shorthand for the current internal conc of r.

                # Check if the cell is dying due to the resource.
                if not self.isLivable(r, current):
                    # Open the channel if the environment is better, otherwise close it.
                    if self.isLivable(r, envRes[r]):
                        self.open(r)
                    else:
                        self.close(r)

                # Also check if the cell isn't dying OR growing.
                elif not self.isIdeal(r, current):
                    # Again, open if the env is better.
                    if self.isIdeal(r, envRes[r]):
                        self.open(r)
                    else:
                        self.close(r)

                # If intracellular levels are ideal, then close the channels.
                else:
                    self.close(r)

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

    def __init__(self, name, vol, res):
        self.name = name
        self.vol = vol
        self.res = res

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def print_res(self):
        for key in self.res:
            print key + ":\t\t" + str(self.res[key])

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
        for org in self.orgs:
            org.setChannels(self.env.res)
        newRes = [org.resAvailable() for org in self.orgs]
        for r in self.env.res:
            self.env.res[r] = ((sum([o[r][0] for o in newRes]) + 
                               self.env.res[r] * self.env.vol)/
                               (sum([o[r][1] for o in newRes]) + self.env.vol))
        for org in self.orgs:
            org.setRes(self.env.res)



# Define all the operons.
# The diffusion and irradiance operons don't actually exist.
# They simplify the code and act as no-sized, non-ATP-consuming transporters.
operons = [Operon('CO2 Diffusion', 0, 0, 'CO2'),
           Operon('O2 Diffusion', 0, 0, 'O2'),
           Operon('EtOH Diffusion', 0, 0, 'EtOH'),
           Operon('Irradiation', 0, 0, 'Lux'),
           Operon('Amino acid transporters', 500, 0, 'AAs'),
           Operon('Glucose transporter', 500, 0, 'Glc'),
           Operon('Na+ channel', 500, 0, 'Na+'),
           Operon('K+ channel', 500, 0, 'K+'),
           Operon('Cl- channel', 500, 0, 'Cl-')]

# Default organisms
eColi = Organism('E. coli', dict(zip(operons, [1 for op in operons])), CELLR)
cDiff = Organism('C. diff', dict(zip(operons, [1 for op in operons])), CELLR)
