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
         'ADP': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'maxGrow': 10**-1,
                 'maxLive': 2*10**-1},
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
         'Glc': {'current': 0.0,#8*10**-3,
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

# There are several basic functions of operons, passive/active transporters,
# modifiers, and reaction catalysts.
OPTYPES = ['pas', 'act', 'mod', 'rxn']


class Reaction:
    """Defines a reaction of reactants to products"""

    def __init__(self, reactants, products):
        # Each one must be a list of tuples.  Each tuple should look like:
        # (resourceString, moles/reaction)
        self.reactants = reactants
        self.products = products

    def __str__(self):
        rxn = ""
        for r in self.reactants:
            rxn += (str(r[1]) + "*" + r[0] + " + ")
        rxn = rxn[:-2] + "-> "
        for p in self.products:
            rxn += (str(p[1]) + "*" + p[0] + " + ")
        return rxn[:-3]

    def __repr__(self):
        return str(self)

    def all(self):
        return self.reactants + self.products

    def species(self):
        return [r[0] for r in self.reactants] + [p[0] for p in self.products]

    # Given a chemical species, returns a dictionary of the number of moles
    # needed for all the other species in the reaction.
    # If the given species is not in the reaction, simply returns the inputs.
    def getMoles(self, species, moles):
        if species not in self.species():
            return {species: moles}
        else:
            # Find the tuple containing the species.
            sTup = [t for t in self.all() if t[0] == species][0]
            rxnMoles = float(moles)/sTup[1]
            # Build and return the dictionary
            return dict([(s, m * rxnMoles) for s, m in self.all()])


class Operon:
    """Represents a bacterial operon"""

    # Operons can either transport something ('act' or 'pas'),
    # modify a min/max tolerance ('mod'), or catalyze a reaction ('rxn').
    # transports must be a resource string.
    # modifies must be a 3-tuple with a resource string, min/max Live/Grow, and an offset value.
    # converts must be 
    def __init__(self, name, size, function, effect, energyRequired=0, rate=None):
        self.name = name
        self.size = size
        if function not in OPTYPES:
            raise ValueError("Function must be 'pas', 'act', 'mod', or 'rxn'.")
        else:
            self.func = function
        self.eff = effect
        self.rate = rate
        self.atpReq = energyRequired
        self.on = True

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # Turns the operon off if it is capable of doing so.
    def turnOff(self):
        if self.eff not in DIFFUSES:
            self.on = False

    def turnOn(self):
        self.on = True


class Genome:
    """A layer for organisms to easily retrieve information about a collection of operons"""

    def __init__(self, operons):
        # operons should be a list.  Initializing a genome then compiles info
        # about operons to save calculations down the road.
        self.size = 0
        self.funcs = {'pas': [], 'act': [], 'con': [], 'mod': []}
        for op in operons:
            self.funcs[op.func].append(op)
            self.size += op.size

        def printOps(self):
            for func in self.funcs:
                for op in self.funcs[func]:
                    print op


class Organism:
    """Represents organism populations"""

    def __init__(self, name, genome, resources, count=100, cVol=6.5*10**-16):
        self.name = name
        self.count = count
        self.cVol = cVol
        self.genes = genome
        self.res = resources

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    def printRes(self):
        for key in self.res:
            print key + ":\t" + str(self.res[key]['current'])

    def printChannels(self):
        print "Res\tOpen?\t[Res]"
        for op in self.genes.funcs['pas']:
            print op.eff + "\t" + str(op.on) + "\t" + str(self.res[op.eff]['current'])

    # Returns the current total volume of the population.
    def vol(self):
        return self.cVol * self.count

    # Returns the current number of moles of ATP, as this is often needed.
    def atp(self):
        return self.res['ATP']['current'] * self.vol()

        # Adds the given number of moles (+ or -) to the current pool of resource r.
    def addRes(self, r, moles):
        self.res[r]['current'] = (self.res[r]['current'] * self.vol() + moles) / self.vol()

    # Hydrolyzes the given moles of ATP, converting it to ADP.
    def useATP(self, moles):
        self.addRes('ATP', -moles)
        self.addRes('ADP', moles)
        self.addRes('P', moles)

    # Takes a resource string (like 'H+') and returns True if it can currently
    # undergo passive transport into or out of the organism.
    def canPass(self, r):
        for op in self.genes.funcs['pas']:
            # Only return True if it can tranport r.
            if op.eff == r:
                return True

        # Return False if all operons are checked and none fit the bill.
        return False

    # Takes a resource string and closes all passive channels for the resource.
    def close(self, r):
        for op in self.genes.funcs['pas']:
            if op.eff == r:
                op.turnOff()

    # Opens all passive channels for the resource.
    def open(self, r):
        for op in self.genes.funcs['pas']:
            if op.eff == r:
                op.turnOn()

    # Returns True if that resource concentration is not lethal to the organism.
    def isLivable(self, r, conc):
        return self.res[r]['minLive'] <= conc <= self.res[r]['maxLive']

    # Returns True if the resource concentration does not limit growth.
    def isIdeal(self, r, conc):
        return self.res[r]['minGrow'] <= conc <= self.res[r]['maxGrow']

    # Finds the number of moles required (positive or negative) to reach growth
    # range for the resource r.
    def molsReq(self, r):
        cur = self.res[r]['current']
        minG = self.res[r]['minGrow']
        maxG = self.res[r]['maxGrow']
        if cur < minG:
            return (minG - cur) * self.vol()
        elif cur > maxG:
            return (maxG - cur) * self.vol()
        # Need 0 moles if already within range.
        else:
            return 0

    # Takes an environmental resource dictionary and closes/opens passive
    # channels according concentrations and cellular needs.
    def setChannels(self, envRes):
        for op in self.genes.funcs['pas']:
            r = op.eff                       # Shorthand for the resource.
            current = self.res[r]['current'] # Shorthand for the current internal conc of r.

            # Check if the cell is dying due to the resource.
            if not self.isLivable(r, current):
                # Open the channel if the environment is better, otherwise close it.
                if self.isLivable(r, envRes[r]):
                    self.open(r)
                else:
                    self.close(r)

            # Also check if the cell isn't growing.
            elif not self.isIdeal(r, current):
                # Again, open if the environment is better.
                if self.isIdeal(r, envRes[r]):
                    self.open(r)
                else:
                    self.close(r)

            # If intracellular levels are ideal, then close the channels.
            else:
                self.close(r)

    # Returns a dictionary of the resources available for pooling (i.e. with
    # open passive channels), with the value being a tuple of the moles and volume.
    def resAvailable(self):
        resToPool = dict(zip(RESLIST, [(0,0) for x in RESLIST]))
        for op in self.genes.funcs['pas']:
            resToPool[op.eff] = (self.res[op.eff]['current'] * self.vol(), self.vol())
        return resToPool

    # Updates the organism's internal resources to the new environment,
    # according to which channels are open.
    def setRes(self, envRes):
        for res in envRes:
            if self.canPass(res):
                self.res[res]['current'] = envRes[res]

    # Checks all active transport operons, and if they should be used.
    def exchange(self, envRes):
        for op in self.genes.funcs['act']:
            r = op.eff
            molesNeeded = self.molsReq(r)
            if molesNeeded:
                atpNeeded = molesNeeded * op.atpReq
                if atpNeeded < self.atp():
                    self.useATP(atpNeeded)
                    self.addRes(r, molesNeeded)
                    envRes[r] = envRes[r] - molesNeeded
                else:
                    atpLeft = self.atp() - (self.res['ATP']['minLive'] * self.vol())
                    molesPossible = atpLeft / op.atpReq
                    self.useATP(atpLeft)
                    self.addRes(r, molesPossible)
                    envRes[r] = envRes[r] - molesPossible
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

    def printRes(self):
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
        resources = [{} for org in proportions]
        for i in range(len(resources)):
            for key in self.res:
                resources[i][key] = (self.res[key] * self.vol * proportions[i])
        return resources

    # Updates the environmental resources
    def update(self, resources):
        return resources


class Ecosystem:
    """A collection of organism populations and their environment"""

    def __init__(self, orgs, env):
        self.orgs = orgs
        self.env = env
        self.tracker = dict(zip(orgs, [[] for org in orgs]))  # To track populations

    def equalize(self):
        light = self.env.res['Lux']
        for org in self.orgs:
            org.setChannels(self.env.res)
            self.tracker[org].append(org.count)
        newRes = [org.resAvailable() for org in self.orgs]
        for r in self.env.res:
            self.env.res[r] = ((sum([o[r][0] for o in newRes]) + 
                               self.env.res[r] * self.env.vol)/
                               (sum([o[r][1] for o in newRes]) + self.env.vol))
        for org in self.orgs:
            org.setRes(self.env.res)
        self.env.res['Lux'] = light # Light resets, or can change according to some function



# Define all the operons.
# The diffusion and irradiance operons don't actually exist.
# They simplify the code and act as no-sized, non-ATP-consuming transporters.
operons = [Operon('CO2 Diffusion', 0, 'pas', 'CO2'),
           Operon('O2 Diffusion', 0, 'pas', 'O2'),
           Operon('EtOH Diffusion', 0, 'pas', 'EtOH'),
           Operon('Irradiation', 0, 'pas', 'Lux'),
           Operon('Amino acid transporters', 500, 'pas', 'AAs'),
           Operon('Glucose transporter', 500, 'act', 'Glc', 1),
           Operon('Na+ channel', 500, 'pas', 'Na+'),
           Operon('K+ channel', 500, 'pas', 'K+'),
           Operon('Cl- channel', 500, 'pas', 'Cl-')]

genome = Genome(operons)

# Default organisms
eColi = Organism('E. coli', genome, CELLR)
cDiff = Organism('C. diff', genome, CELLR)
