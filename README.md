# Imaging Plates calculator curves for any Ion

For now BAS_TR type only was implemented, BAS_MS will be added later

Calculator based on CATima (GSI, library for calculation of energy loss, range, angular scattering and time of flight of the particle passing through matter).

## How to use

1. Carefully install CATima on your system (see https://github.com/hrosiak/catima to install).
2. `git clone https://github.com/dinAlt220/IPCALIB.git`
3. `cd IPCALIB`
4. `main.py` is the main file for calculation, you need change main parameters inside it, see example below:

#Tungsten (as example)

`Atom_mass = 183.84` - atomic mass of incident ion

`Z = 74` - atom number of incident ion

`Q = 0` - chrge of incident ion


`layer_thick = 0.01` - thick of the thin layer [um] (total layers = 50 um (TR type) / layer_thick). Be careful here, choose small but not so small due to calculation time.

`angle = 0.0` - incident angle of ion [deg] (0.0 is pirpendicular)

`energy_range = np.arange(0, 0.7, 0.1)` - energy range for calibration curve [MeV] (the first, the last, bin)


#Scanner parameters (depends of scanner)

`A = 600.0` - [GL/MeV]

`B = 15.0` - [um/MeV]

`C = 25.0` - [GL/MeV]

`L = 44.0` - absoption length [um] (44.0 for TR type)


######___MAIN___######

`ip = IP()` - create class

`ip.set_layer_thick(layer_thick)` - set layer thick

`ip.set_theta_incident(angle)` - set incident angle of ion

`ip.set_type("TR")` - set IP type

`ip.set_ion(Atom_mass, Z, Q)` - set incident ion type

`ip.set_energy_range(energy_range)` - set energy range for calibration curve

`ip.set_params(A, B, C, L)` - set scanner parameters and absoption length of IP

`ip.run()` - run calculation

`ip.save_data()` - save result to /data directory 

5. `python3 main.py`

There will be a plot in the end of calculation which you can save.