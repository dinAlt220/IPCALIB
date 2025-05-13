from IP import IP
import numpy as np

#Tungsten
Atom_mass = 183.84 # atomic mass of incident ion
Z = 74 # atom number of incident ion
Q = 0 # chrge of incident ion

# #Aluminum
# Atom_mass = 26.981
# Z = 13
# Q = 0

layer_thick = 0.01 # thick of the thin layer [um] (total layers = 50 um (TR type) / layer_thick)
angle = 0.0 # incident angle of ion [deg] (0.0 is pirpendicular)

energy_range = np.arange(0, 0.7, 0.1) # energy range for calibration curve [MeV] (the first, the last, bin)


#Scaner parameters (depends of scaner)
A = 600.0 # [GL/MeV]
B = 15.0 # [um/MeV]
C = 25.0 # [GL/MeV]

L = 44.0 # absoption length [um] (44.0 for TR type)


######___MAIN___######

ip = IP() # create class

ip.set_layer_thick(layer_thick) # set layer thick
ip.set_theta_incident(angle) # set incident angle of ion
ip.set_type("TR") # set IP type
ip.set_ion(Atom_mass, Z, Q) # set incident ion type
ip.set_energy_range(energy_range) # set energy range for calibration curve
ip.set_params(A, B, C, L) # set scanner parameters and absoption length of IP

ip.run() # run calculation

ip.save_data() # save result to /data directory 