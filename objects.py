import random

# A starter environmental resources dictionary.
# All values are mol/L, except Temp and Lux, which are in Kelvin and Lux.
# Based on standard LB medium and standard growth conditions.
# http://en.wikipedia.org/wiki/Lysogeny_broth
ENVR = {'H+'  : 10**-7.4,
        'K+'  : 3.3*10**-3,
        'Na+' : 1.8*10**-1,
        'Cl-' : 1.8*10**-1,
        'CO2' : 3.3*10**-2,
        'O2'  : 3.3*10**-2,
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
                 'ideal'  : 10**-7.4,
                 'maxGrow': 10**-7.2,
                 'maxLive': 10**-7.0},
         'K+':  {'current': 2.1*10**-1,
                 'minLive': 10**-1,
                 'minGrow': 1.5*10**-1,
                 'ideal'  : 2*10**-1,
                 'maxGrow': 2.5*10**-1,
                 'maxLive': 3*10**-1},
         'Na+': {'current': 5*10**-3,
                 'minLive': 10**-3,
                 'minGrow': 3*10**-3,
                 'ideal'  : 3.5*10**-3,
                 'maxGrow': 1.4*10**-2,
                 'maxLive': 2*10**-2},
         'Cl-': {'current': 5*10**-3,
                 'minLive': 10**-3,
                 'minGrow': 3*10**-3,
                 'ideal'  : 3.5*10**-3,
                 'maxGrow': 1.4*10**-2,
                 'maxLive': 2*10**-2},
         'ATP': {'current': 8*10**-3,
                 'minLive': 5*10**-4,
                 'minGrow': 2*10**-3,
                 'ideal'  : 9*10**-3,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'ADP': {'current': 8*10**-3,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-1,
                 'maxLive': 2*10**-1},
         'CO2': {'current': 3.3*10**-2,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-1,
                 'maxLive': 10**-1},
         'O2':  {'current': 3.3*10**-2,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-1,
                 'maxLive': 10**-1},
         'Glc': {'current': 8*10**-3,
                 'minLive': 0.0,
                 'minGrow': 10**-3,
                 'ideal'  : 10**-2,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Fru': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'Lac': {'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 2*10**-2},
         'AAs': {'current': 1.5*10**-1,
                 'minLive': 10**-2,
                 'minGrow': 10**-1,
                 'ideal'  : 2*10**-1,
                 'maxGrow': 2*10**-1,
                 'maxLive': 3*10**-1},
         'N':   {'current': 8*10**-3,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1},
         'P':   {'current': 8*10**-3,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**-2,
                 'maxLive': 10**-1},
         'EtOH':{'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 1.09,   # These correspond to ~6%...
                 'maxLive': 1.71},  # ...and ~10% ABV
         'Temp':{'current': 310.0,
                 'minLive': 273.0,
                 'minGrow': 281.0,
                 'ideal'  : 310.0,
                 'maxGrow': 318.0,
                 'maxLive': 344.0},
         'Lux' :{'current': 0.0,
                 'minLive': 0.0,
                 'minGrow': 0.0,
                 'ideal'  : 0.0,
                 'maxGrow': 10**5,
                 'maxLive': 1.7*10**5}}

# Some resources diffuse freely across membranes.
DIFFUSES = ['CO2', 'O2', 'EtOH', 'Lux', 'Temp']

# There are several basic functions of operons, passive/active transporters,
# modifiers, and reaction catalysts.
OPTYPES = ['pas', 'act', 'mod', 'rxn', 'misc']


class Reaction:
    """Defines a reaction of reactants to products"""

    def __init__(self, reactants, products):
        # Each one must be a dictionary, with resource strings as keys and
        # the corresponding number of moles as the value.
        self.reactants = reactants
        self.products = products

    def __str__(self):
        rxn = ""
        for r in self.reactants:
            rxn += (str(self.reactants[r]) + "*" + r + " + ")
        rxn = rxn[:-2] + "-> "
        for p in self.products:
            rxn += (str(self.products[p]) + "*" + p + " + ")
        return rxn[:-3]

    def __repr__(self):
        return str(self)

    def all(self):
        return self.reactants + self.products

    def species(self):
        D = {}
        D.update(self.reactants)
        D.update(self.products)
        return D

    # Takes a list of tuples.  Each tuple contains a resource string and the
    # moles of that resource available/desired.  Finds the limiting reactant/
    # product, and returns a dictionary specifying the moles used/produced in
    # the reaction.  Moles consumed get negative values.
    def getMoles(self, speciesL):
        concD = {}
        # Find the limiting reactant/product of the ones provided.
        rxnMoles = min([float(m)/self.species()[s] for s, m in speciesL])
        # Then for each species, multiply the number of rxnMoles by the moles
        # produced per reaction and store it in the dictionary.
        for s in self.reactants:
            concD[s] = -self.reactants[s] * rxnMoles
        for s in self.products:
            concD[s] = self.products[s] * rxnMoles
        return concD


class Operon:
    """Represents a bacterial operon"""

    # Operons can either transport something ('act' or 'pas'),
    # modify a min/max tolerance ('mod'), or catalyze a reaction ('rxn').
    # function must be one of the above operon-types, and then effect for each
    # is different.
    # For 'pas' or 'act', effect must be a resource string.
    # For 'rxn', effect must be a Reaction object.
    # For 'mod', effect must be a tuple of (resourceStr, min/maxStr, offset).
    # For 'misc', effect must be a special string.
    def __init__(self, name, size, function, effect, energyRequired=0, rate=None):
        self.name = name
        self.size = size
        if function not in OPTYPES:
            raise ValueError("Function must be 'pas', 'act', 'mod', 'rxn' or 'misc'.")
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
        self.funcs = {'pas': [], 'act': [], 'rxn': [], 'mod': [], 'misc': []}
        for op in operons:
            self.funcs[op.func].append(op)
            self.size += op.size

        dnaPols = 0
        for op in self.funcs['misc']:
            if op.eff == 'DNAPol':
                dnaPols += 1
        self.dnaPols = dnaPols


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

    def printSummary(self):
        print self.name + ": " + str(self.count)
        limitedBy = ""
        dyingFrom = ""
        for r in self.res:
            if not self.canGrow(r):
                limitedBy = limitedBy + str(r) + ": " + str(self.res[r]['current']) + "  "
                if not self.canLive(r):
                    dyingFrom = dyingFrom + str(r) + ": " + str(self.res[r]['current']) + "  "
        print "Limited by: " + limitedBy
        print "Dying from: " + dyingFrom 
        print ""

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
            # Only return True if it can tranport r and is on.
            if op.eff == r and op.on:
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
    # If no concentration is given, it checks the current concentration of r.
    def canLive(self, r, conc=None):
        if not conc:
            conc = self.res[r]['current']
        return self.res[r]['minLive'] <= conc <= self.res[r]['maxLive']

    # Returns True if the resource concentration does not limit growth.
    # If no concentration is given, it checks the current concentration of r.
    def canGrow(self, r, conc=None):
        if not conc:
            conc = self.res[r]['current']
        return self.res[r]['minGrow'] <= conc <= self.res[r]['maxGrow']

    # Finds the number of moles required (positive or negative) to reach the
    # the ideal concentration for the resource r.
    def molsReq(self, r):
        cur = self.res[r]['current']
        ideal = self.res[r]['ideal']
        return (ideal - cur) * self.vol()

    # Takes an environmental resource dictionary and closes/opens passive
    # channels according to concentrations and cellular needs.
    def setChannels(self, envRes):
        for op in self.genes.funcs['pas']:
            r = op.eff                       # Shorthand for the resource.
            current = self.res[r]['current'] # Shorthand for the current internal conc of r.

            # Check if the cell is dying due to the resource.
            if not self.canLive(r, current):
                # Open the channel if the environment is better, otherwise close it.
                if self.canLive(r, envRes[r]):
                    self.open(r)
                else:
                    self.close(r)

            # Also check if the cell isn't growing.
            elif not self.canGrow(r, current):
                # Again, open if the environment is better.
                if self.canGrow(r, envRes[r]):
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
            if op.on:
                resToPool[op.eff] = (self.res[op.eff]['current'] * self.vol(), self.vol())
        return resToPool

    # Updates the organism's internal resources to the new environment,
    # according to which channels are open.
    def diffuseRes(self, envRes):
        for res in envRes:
            if self.canPass(res):
                self.res[res]['current'] = envRes[res]

    # Checks all active transport operons, and if they should be used.
    # Order matters here!  Most important active transport should go first.
    # Otherwise ATP might be used up obtaining non-vital resources.
    def exchangeRes(self, envRes):
        for op in self.genes.funcs['act']:
            r = op.eff
            molesNeeded = self.molsReq(r)
            if molesNeeded:
                atpNeeded = abs(molesNeeded * op.atpReq)
                if atpNeeded < self.atp():
                    self.useATP(atpNeeded)
                    self.addRes(r, molesNeeded)
                    envRes[r] = envRes[r] - molesNeeded
                else:
                    atpLeft = self.atp() - (self.res['ATP']['minLive'] * self.vol())
                    molesPossible = atpLeft / op.atpReq
                    if molesNeeded < 0.0:
                        molesPossible *= -1
                    self.useATP(atpLeft)
                    self.addRes(r, molesPossible)
                    envRes[r] = envRes[r] - molesPossible
        return envRes

    # Converts things to place concentrations in the growth range.
    # Goes through the rxn operons in the order they were added, so
    # earlier operons may use up some resources, leaving none for later ones.
    def convertRes(self):
        # For every reaction, check if it should run and if so, for what values.
        for op in self.genes.funcs['rxn']:
            # Reactants remove a resource, products create a resource
            reac = op.eff.reactants.keys()
            prod = op.eff.products.keys()
            desired = []

            # Check if we need any more of the products or less of the reactants.
            for r in prod:
                need = self.molsReq(r)
                if need > 0:
                    desired.append((r, need))
            for r in reac:
                need = self.molsReq(r)
                if need < 0:
                    desired.append((r, abs(need)))
                # If the current concentration is already below ideal, then we
                # only allocate as much as we can.
                else:
                    canSpare = (self.res[r]['current'] - self.res[r]['minGrow']) * self.vol()
                    if canSpare <= 0:
                        canSpare = 0.0
                    desired.append((r, canSpare))

            # Perform the reaction given our desired constraints.
            react = op.eff.getMoles(desired)

            # Update the resources used in the reaction.
            for r in react:
                self.addRes(r, react[r])

    # Returns a factor by which the genome can increase in 1 minute.
    def calcGrowth(self):
        # DNA polymerase replicates ~1000bp/sec/enzyme, so the time required
        # for replication depends on the genome size and number of DNA pols.
        # It also requires resources, and can be limited by that.
        # But we won't take that into consideration yet.
        rateLimit = 60 * 1000.0 * self.genes.dnaPols
        #resLimit = 6.022*10**23 * min((self.res['N']/4.0, resAvailable['P']/3.0))
        return (rateLimit / self.genes.size)

    # Handles the division of the organisms.  Division rate is based upon the
    # genome size and (eventually) available resources.
    # Returns a dictionary of resources released (all zero, unless cells died).
    def divide(self):
        # First check if cells should multiply or die.
        canGrow = True
        canLive = True
        factor = 0.0
        for r in self.res:
            if not self.canLive(r, self.res[r]['current']):
                factor -= 0.1
                canLive = False
            if not self.canGrow(r, self.res[r]['current']):
                canGrow = False
        if canGrow:
            factor = self.calcGrowth()
            #print factor
            #molesBP = factor * self.genes.size * self.count * 6.022*10**-23
            #print molesBP
            #self.printRes()
            #print ""
            #self.addRes('N', -molesBP * 4.0)
            #self.printRes()
            #print ""
            #self.addRes('P', -molesBP * 3.0)

        # Adjust the count based on the growth factor.
        self.count = self.count * (1.0 + factor)

        # Distribute/release resources based on the growth factor.
        resReleased = {}
        for r in self.res:
            if not canLive:
                resReleased[r] = self.res[r]['current'] * abs(factor) * self.vol()
            else:
                resReleased[r] = 0.0
            self.res[r]['current'] = self.res[r]['current'] / (1.0 + abs(factor))
        return resReleased


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
    # community should be a list of organisms.
    def partition(self, community):
        # Find the proportion of each organism by volume
        volumes = [org.vol() for org in community]
        total = sum(volumes)
        proportions = [x/total for x in volumes]

        # Then build a dictionary for each organism, giving it resources
        # proportional to its fractional volume.
        resources = []
        for i in range(len(community)):
            resources.append({})
            for key in self.res:
                resources[i][key] = (self.res[key] * self.vol * proportions[i])
        return resources

    # Updates the environmental resources by summing the number of moles
    # each organism has left for the environment.
    # resources should be a list of dictionaries, like that created by partition().
    def update(self, partition):
        for r in self.res:
            totalMoles = sum([o[r] for o in partition])
            self.res[r] = totalMoles / self.vol

    def addRes(self, r, moles):
        if r in self.res:
            self.res[r] = (self.res[r] * self.vol + moles) / self.vol


class Ecosystem:
    """A collection of organism populations and their environment"""

    def __init__(self, orgs, env):
        self.orgs = orgs
        self.env = env
        self.tracker = dict(zip(orgs, [[] for org in orgs]))  # To track populations

    def printPops(self):
        for org in self.orgs:
            print str(org) + ": " + str(org.count)

    def cycle(self):
        # Set the amount of light.
        light = self.env.res['Lux']
        diffusedRes = []

        # Every organism will set channels, add its count to the tracker,
        # and tell the amount of resources available for diffusion.
        for org in self.orgs:
            self.tracker[org].append(org.count)
            org.setChannels(self.env.res)
            diffusedRes.append(org.resAvailable())

        # Then the new environmental concentration will be found.
        for r in self.env.res:
            # New conc = (moles from cells + moles from env) / total volume
            self.env.res[r] = ((sum([o[r][0] for o in diffusedRes]) + 
                               self.env.res[r] * self.env.vol)/
                               (sum([o[r][1] for o in diffusedRes]) + self.env.vol))

        # Then the resources will diffuse into/out of cells
        for org in self.orgs:
            org.diffuseRes(self.env.res)

        # After diffusion, the environmental resources will be partitioned
        # and each cell can actively transport its share.  Then the environment
        # must be updated.
        partition = self.env.partition(self.orgs)
        for i in range(len(self.orgs)):
            partition[i] = self.orgs[i].exchangeRes(partition[i])
        self.env.update(partition)

        # And finally each organism performs internal processes and grows/dies.
        for org in self.orgs:
            org.convertRes()
            resReleased = org.divide()
            for r, m in resReleased.items():
                self.env.addRes(r, m)
        
        org.convertRes()
        self.env.res['Lux'] = light # Light resets, or can change according to some function


# Define all the reactions
reactions = [Reaction({'Glc':1, 'O2': 6, 'ADP': 38, 'P': 38}, {'CO2': 6, 'ATP': 38}),
             Reaction({'Glc':1, 'ADP': 2, 'P':2}, {'EtOH': 2, 'CO2': 2, 'ATP': 2}),
             Reaction({'ATP': 1}, {'ADP': 1, 'P': 1})]

# Define all the operons.
# The diffusion and irradiance operons don't actually exist.
# They simplify the code and act as no-sized, non-ATP-consuming transporters.
operons = [Operon('CO2 Diffusion', 1000000, 'pas', 'CO2'),
           Operon('O2 Diffusion', 0, 'pas', 'O2'),
           Operon('Temp Diffusion', 0, 'pas', 'Temp'),
           Operon('EtOH Diffusion', 0, 'pas', 'EtOH'),
           Operon('Irradiation', 0, 'pas', 'Lux'),
           Operon('Amino acid transporters', 500, 'pas', 'AAs'),
           Operon('Glucose transporter', 500, 'act', 'Glc', 1),
           Operon('Na+ channel', 500, 'pas', 'Na+'),
           Operon('K+ channel', 500, 'pas', 'K+'),
           Operon('K+ transporter', 500, 'act', 'K+', 1),
           Operon('Cl- channel', 500, 'pas', 'Cl-'),
           Operon('Aerobic respiration', 1000, 'rxn', reactions[0]),
           Operon('DNA Polymerase', 1000, 'misc', 'DNAPol')]

genome = Genome(operons)

# Default organisms
eColi = Organism('E. coli', genome, CELLR)
cDiff = Organism('C. diff', genome, CELLR, 200)
