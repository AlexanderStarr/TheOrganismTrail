from constants import *
from objects import *

# Define all the reactions
reactions = {'Aerobic respiration': Reaction({'Glc':1, 'O2': 6, 'ADP': 38, 'P': 38}, {'CO2': 6, 'ATP': 38}),
             'Alcohol fermentation': Reaction({'Glc':1, 'ADP': 2, 'P':2}, {'EtOH': 2, 'CO2': 2, 'ATP': 2}),
             'ATP Hydrolysis': Reaction({'ATP': 1}, {'ADP': 1, 'P': 1}),
             'Photosynthesis': Reaction({'CO2': 6}, {'Glc': 1, 'O2': 6}),
             'ADP Production': Reaction({'N': 5, 'P': 2}, {'ADP': 1}),
             'AA Degradation': Reaction({'AAs': 2}, {'N': 3}),
             'AA Production': Reaction({'N': 3}, {'AAs': 2})}

# Define all the operons.
# The diffusion and irradiance operons don't actually exist.
# They simplify the code and act as no-sized, non-ATP-consuming transporters.
operons = {'CO2 Diffusion': Operon('CO2 Diffusion', 1000000, 'pas', 'CO2'),
           'O2 Diffusion': Operon('O2 Diffusion', 0, 'pas', 'O2'),
           'Temp Diffusion': Operon('Temp Diffusion', 0, 'pas', 'Temp'),
           'EtOH Diffusion': Operon('EtOH Diffusion', 0, 'pas', 'EtOH'),
           'Irradiation': Operon('Irradiation', 0, 'pas', 'Lux'),
           'Glucose channel': Operon('Glucose channel', 500, 'pas', 'Glc'),
           'Glucose transporter': Operon('Glucose transporter', 500, 'act', 'Glc', 1),
           'H+ transporter': Operon('H+ transporter', 500, 'act', 'H+', 0.3),
           'K+ transporter': Operon('K+ transporter', 500, 'act', 'K+', 0.3),
           'Na+ transporter': Operon('Na+ transporter', 500, 'act', 'Na+', 0.5),
           'Cl- transporter': Operon('Cl- transporter', 500, 'act', 'Cl-', 0.5),
           'Amino acid channel': Operon('Amino acid channel', 500, 'pas', 'AAs'),
           'Amino acid transporter': Operon('Amino acid transporter', 500, 'act', 'AAs', 1),
           'Na+ channel': Operon('Na+ channel', 500, 'pas', 'Na+'),
           'K+ channel': Operon('K+ channel', 500, 'pas', 'K+'),
           'Cl- channel': Operon('Cl- channel', 500, 'pas', 'Cl-'),
           'Aerobic respiration': Operon('Aerobic respiration', 1000, 'rxn', reactions['Aerobic respiration']),
           #'Photosynthesis': Operon('Photosynthesis', 1000, 'rxn', reactions['Photosynthesis']),
           'DNA Polymerase': Operon('DNA Polymerase', 1000, 'misc', 'DNAPol'),
           'ADP Production': Operon('ADP Production', 1000, 'rxn', reactions['ADP Production']),
           'AA Degradation': Operon('AA Degradation', 1000, 'rxn', reactions['AA Degradation']),
           'AA Production': Operon('AA Production', 1000, 'rxn', reactions['AA Production']),
           'P Channel': Operon('P transporter', 500, 'pas', 'P')}

genome = Genome(operons.values())

# Default environments, setting all of them to ENVR will use the same dictionary!
environments = {'Lab': Environment('Lab', 1, ENVR),
                'Blood': Environment('Blood', 5, ENVR)}

# Default organisms
eColi = Organism('E. coli', genome, CELLR)
cDiff = Organism('C. diff', genome, CELLR, 200)