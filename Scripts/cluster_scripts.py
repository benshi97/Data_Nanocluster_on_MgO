#!/usr/bin/env python
# coding: utf-8

# Description: Contains functions for reading and plotting data from MRCC, ORCA and VASP calculations.

import numpy as np
from ase import units
from scipy.stats import linregress
from datetime import datetime

# Some constants
Hartree = 27.211386245988
Bohr = 0.5291772105638411
cm1_to_eV = 1 / 8065.54429
hundredcm1 = 100 * cm1_to_eV * 1000


def get_mrcc_walltime(filename):
    """
    Reads the walltime from the mrcc.out file.
        
    Parameters
    ----------
    filename : str
        The location of the 'mrcc.out' file to read from.
        
    Returns
    -------
    float
        The walltime in seconds.
        
    Notes
    -----
    This function reads the 'mrcc.out' file and extracts the start and end time information to calculate the total walltime taken by the MRCC calculation. The function calculates the time duration between the timestamps found in the file and returns it in seconds.
    """

    # Get the start and end time from the file
    orig_time = datetime(1, 1, 1, 0, 0)
    total_time = datetime(1, 1, 1, 0, 0)

    f = open(filename)
    a = f.readlines()
    b1 = datetime.strptime(
        a[19].split()[1] + "-" + a[19].split()[2], "%Y-%m-%d-%H:%M:%S"
    )
    b2 = datetime.strptime(
        a[-3].split()[1] + "-" + a[-3].split()[2], "%Y-%m-%d-%H:%M:%S"
    )
    total_time = total_time + (b2 - b1)
    f.close()
    return (total_time - orig_time).total_seconds()


def read_vib_freq(filename, lines=None):
    """
    Read vibrational frequencies from a file.
    
    Parameters
    ----------
    filename : str
        The name of the file to read vibrational frequencies from.
    lines : list
        List of lines from the file. If not provided, the function will read lines from the file.
        
    Returns
    -------
    freq : list
        List of real vibrational frequencies.
    i_freq : list
        List of imaginary vibrational frequencies.
        
    Notes
    -----
    This function reads vibrational frequency information from a given file. It extracts both real and imaginary vibrational frequencies from the lines containing the frequency data. The frequencies are extracted based on the presence of "THz" in the data. Real frequencies are extracted unless the "f/i=" label is found, in which case imaginary frequencies are extracted. The function returns two lists containing the real and imaginary frequencies respectively.
    """

    freq = []
    i_freq = []

    # If lines are not provided, read lines from the file
    if lines is None:
        with open(filename, "r", encoding="ISO-8859-1") as f:
            lines = f.readlines()

    for line in lines:
        data = line.split()
        if "THz" in data:
            if "f/i=" not in data:
                freq.append(float(data[-2]))  # Append real frequency to the freq list
            else:
                i_freq.append(float(data[-2]))  # Append imaginary frequency to the i_freq list
    return freq, i_freq


def get_vibrational_energy_contribution(vib_energies, temperature):
    """
    Calculates the change in internal energy due to vibrations from 0K to the specified temperature for a set of vibrations given in eV and a temperature given in Kelvin. Returns the energy change in eV.
    
    Parameters
    ----------
    vib_energies : list
        List of vibrational energies in eV.
    temperature : float
        Temperature in Kelvin.

    Returns
    -------
    float
        The change in internal energy in eV.
    """

    # Calculate the product of Boltzmann constant (kB) and temperature (kT)
    kT = units.kB * temperature
    
    dU = 0.0  # Initialize the change in internal energy

    # Iterate through the list of vibrational energies
    for energy in vib_energies:
        dummy_ene = energy * 0.001  # Convert energy from millielectronvolts to eV
        # Calculate the energy contribution from each vibration and accumulate
        dU += dummy_ene / (np.exp(dummy_ene / kT) - 1.0)
    
    return dU  # Return the total change in internal energy in eV


def get_ZPE_correction(vib_energies):
    """
    Calculates the zero-point vibrational energy correction from a list of vibrational energies given in eV. 

    Parameters
    ----------
    vib_energies : list
        List of vibrational energies in eV.

    Returns
    -------
    float
        The zero-point vibrational energy correction in eV.
    """
    zpe = 0.0  # Initialize the zero-point energy correction

    # Iterate through the list of vibrational energies
    for energy in vib_energies:
        dummy_ene = energy * 0.001  # Convert energy from millielectronvolts to eV
        zpe += 0.5 * dummy_ene  # Calculate the contribution to zero-point energy
    
    return zpe  # Return the total zero-point vibrational energy correction in eV


def get_quasi_rrho(r_freq, i_freq, T):
    """
    Uses the quasi rigid rotor harmonic approximation to calculate the thermal change and zero-point energies from vibrational frequencies in cm-1 and a temperature in Kelvin.
    
    Parameters
    ----------
    r_freq : list
        List of real vibrational frequencies in cm-1.
    i_freq : list
        List of imaginary vibrational frequencies in cm-1.
    T : float
        Temperature in Kelvin.
        
    Returns
    -------
    dU : float
        The total change in energy including thermal energy and zero-point energy in eV.
    eth : float
        The thermal energy in eV.
    zpe : float
        The zero-point energy in eV.
    kT : float
        The product of Boltzmann constant (kB) and temperature (kT) in eV.
    """

    k = units.kB  # Boltzmann constant
    combined_freq = r_freq + [0.0001] * len(i_freq)  # Combine real and imaginary frequencies
    kT = k * T * 1000  # Calculate kT in eV

    dU = 0  # Initialize total energy change
    zpe = 0.0  # Initialize zero-point energy correction
    eth = 0.0  # Initialize thermal energy contribution
    for i in combined_freq:
        omega = 1 / (1 + ((hundredcm1 / i) ** 4))  # Calculate the vibrational frequenecy in meV
        dURRho = i / (np.exp(i / kT) - 1.0) + 0.5 * i  # Calculate the contribution to thermal energy from this frequency
        zpe += omega * 0.5 * i  # Calculate the contribution to zero-point energy
        eth += omega * i / (np.exp(i / kT) - 1.0) + (1 - omega) * 0.5 * kT  # Calculate the thermal energy contribution
        dU += omega * dURRho + (1 - omega) * 0.5 * kT  # Calculate the total energy change
    
    return dU, eth, zpe, kT  # Return the calculated values


def get_ad_rrho(r_freq, i_freq, dof, T):
    """
    Uses the quasi rigid rotor harmonic approximation to calculate the thermal change and zero-point energies from vibrational frequencies in cm-1 and a temperature in Kelvin. SPECIFICALLY for gas molecules which have degrees of freedom controlled by symmetry, such as 3N-6 or 3N-5 for non-linear and linear molecules, respectively.
     
    Parameters
    ----------
    r_freq : list
        List of real vibrational frequencies in cm-1.
    i_freq : list
        List of imaginary vibrational frequencies in cm-1.
    dof : int
        Degrees of freedom of the molecule.
    T : float
        Temperature in Kelvin.

    Returns
    -------
    dU : float
        The total change in energy including thermal energy and zero-point energy in eV.
    eth : float
        The thermal energy in eV.
    zpe : float
        The zero-point energy change in eV.
    kT : float
        The product of Boltzmann constant (kB) and temperature (kT) in eV.
    """
   
    k = units.kB  # Boltzmann constant
    combined_freq = r_freq + [0.0001] * len(i_freq)  # Combine real and imaginary frequencies
    kT = k * T * 1000  # Calculate kT in eV

    dU = 0  # Initialize total energy change
    zpe = 0.0  # Initialize zero-point energy correction
    eth = 0.0  # Initialize thermal energy contribution
    for i in combined_freq:
        omega = 1 / (1 + ((hundredcm1 / i) ** 4))  # Calculate the dimensionless parameter omega
        dURRho = i / (np.exp(i / kT) - 1.0) + 0.5 * i  # Calculate the contribution to energy due to vibrations
        zpe += omega * 0.5 * i  # Calculate the contribution to zero-point energy
        eth += omega * i / (np.exp(i / kT) - 1.0) + (1 - omega) * 0.5 * kT  # Calculate the thermal energy contribution
        dU += omega * dURRho + (1 - omega) * 0.5 * kT  # Calculate the total energy change
    
    return dU, eth, zpe, kT  # Return the calculated values


def find_co_gamma(eads_list, tot_atom_list=[6, 22, 34, 42, 58, 82, 84, 100, 108]):
    """
    Function to find the optimal extrapolation power for clusters in the SKZCAM protocol.
    
    Parameters
    ----------
    eads_list : list
        List of Eads values with increasing cluster size
    tot_atom_list : list
        List of total number of atoms in the cluster
        
    Returns
    -------
    float
        The optimal extrapolation power
        
    Notes
    -----
    This function takes a list of Eads values and a list of total number of atoms in the cluster and finds the optimal extrapolation power for the SKZCAM protocol. The optimal extrapolation power is found by calculating the mean square deviation (MSD) of the Eads values from the extrapolated values for a range of extrapolation powers. The extrapolation power that gives the lowest MSD is returned.
    """
    
    power_list = []

    # Generate a list of power values from 0.1 to 10.0 with step 0.01
    for i in range(1000):
        power_list += [np.round(0.1 + 0.01 * i, 3)]

    msd_list = []
    msd_best = []

    # Iterate over the power values
    for k in range(1000):
        length = len(eads_list)

        # Perform linear regression
        slope, intercept, r, p, se = linregress(
            [1 / (x ** (power_list[k])) for x in tot_atom_list[:length]],
            [float(x) for x in eads_list[:length]],
        )

        # Calculate predicted values using linear regression coefficients
        predicted_values = [
            intercept + slope / (x ** (power_list[k])) for x in tot_atom_list[:length]
        ]

        # Calculate Mean Squared Deviation (MSD) and store in msd_list
        msd_list += [
            np.sqrt(
                np.mean(
                    np.square(np.array(predicted_values) - np.array(eads_list[:length]))
                )
            )
        ]

    # Find the power value that corresponds to the minimum MSD
    msd_best = [
        power_list[msd_list.index(min(msd_list))],
        min(msd_list),
        msd_list.index(min(msd_list)),
    ]

    # Return the optimal power value that minimizes MSD
    return msd_best[0]


def get_eads(
    filename, code_format="mrcc", typ="ccsdt", structs=["AD_SLAB", "SLAB_CP", "AD_CP"]
):
    """
    Function to calculate the Eads value for a given cluster.
    
    Parameters
    ----------
    filename : str
        The location of the directory containing the output files.
    code_format : str
        The code format. Options are 'mrcc', 'vasp', 'quantum_espresso', 'cc4s', 'vasp_wodisp', 'dftd3', 'orca', 'orca_mp2'
    typ : str
        The type of calculation performed. Options are 'ccsdt', 'ccsdt_tot', 'lccsdt', 'lccsdt_tot', 'lccsdt_lmp2_tot', 'ccsdt_mp2_tot', 'hf', 'lmp2', 'lmp2_tot', 'lmp2_corr', 'mp2', 'lccsd', 'lccsdt_lccsd_tot', 'fnoccsdt_tot', 'fnoccsd_tot', 'fnoccsdt_mp2_tot', 'fnoccsdt', 'fnoccsd', 'fnoccsdt_mp2', 'ccsd', 'ccsd_tot', 'dft', 'B2PLYP', 'DSDPBEP86'
    structs : list
        List of directories containing the output files for the three structures for adsorption energy.
        
    Returns
    -------
    float
        The adsorption energy in its original units.
        
    """

    if code_format == "mrcc":
        a = find_energy(
            filename + "/{0}/mrcc.out".format(structs[0]),
            code_format=code_format,
            typ=typ,
        )
        b = find_energy(
            filename + "/{0}/mrcc.out".format(structs[1]),
            code_format=code_format,
            typ=typ,
        )
        c = find_energy(
            filename + "/{0}/mrcc.out".format(structs[2]),
            code_format=code_format,
            typ=typ,
        )
        eads = a - b - c
    elif "orca" in code_format:
        a = find_energy(
            filename + "/{0}/orca.out".format(structs[0]),
            code_format=code_format,
            typ=typ,
        )
        b = find_energy(
            filename + "/{0}/orca.out".format(structs[1]),
            code_format=code_format,
            typ=typ,
        )
        c = find_energy(
            filename + "/{0}/orca.out".format(structs[2]),
            code_format=code_format,
            typ=typ,
        )
        eads = a - b - c
    elif "vasp" in code_format:
        a = find_energy(
            filename + "/{0}/OUTCAR".format(structs[0]),
            code_format=code_format,
            typ=typ,
        )
        b = find_energy(
            filename + "/{0}/OUTCAR".format(structs[1]),
            code_format=code_format,
            typ=typ,
        )
        c = find_energy(
            filename + "/{0}/OUTCAR".format(structs[2]),
            code_format=code_format,
            typ=typ,
        )
        eads = a - b - c
    return eads


def find_energy(filename, typ="ccsdt", code_format="mrcc"):
    """
    Function to parse the energy from a MRCC or ORCA output file.
    
    Parameters
    ----------
    filename : str
        The location of the output file to read from.
    typ : str
        The type of method to read. Options are 'ccsdt', 'ccsdt_tot', 'lccsdt', 'lccsdt_tot', 'lccsdt_lmp2_tot', 'ccsdt_mp2_tot', 'hf', 'lmp2', 'lmp2_tot', 'lmp2_corr', 'mp2', 'lccsd', 'lccsdt_lccsd_tot', 'fnoccsdt_tot', 'fnoccsd_tot', 'fnoccsdt_mp2_tot', 'fnoccsdt', 'fnoccsd', 'fnoccsdt_mp2', 'ccsd', 'ccsd_tot', 'dft', 'B2PLYP', 'DSDPBEP86'
    code_format : str
        The code format. Options are 'mrcc', 'vasp', 'quantum_espresso', 'cc4s', 'vasp_wodisp', 'dftd3', 'orca', 'orca_mp2'
        
    Returns
    -------
    float
        The energy in the original units.
    """

    if code_format == "mrcc":
        if typ == "lccsdt":
            search_word = "CCSD(T) correlation energy + MP2 corrections [au]:"
        elif typ == "lccsdt_tot":
            search_word = "Total LNO-CCSD(T) energy with MP2 corrections [au]"
        elif typ == "lccsdt_lmp2_tot":
            search_word = "Total LMP2 energy [au]"
        elif typ == "ccsdt_mp2_tot":
            search_word = "Total MP2 energy [au]"
        elif typ == "ccsdt":
            search_word = "CCSD(T) correlation energy [au]:"
        elif typ == "ccsdt_tot":
            search_word = "Total CCSD(T) energy"
        elif typ == "hf":
            search_word = "Reference energy [au]:    "
        elif typ == "lmp2":
            search_word = "LMP2 correlation energy [au]:         "
        elif typ == "lmp2_tot":
            search_word = "DF-MP2 energy [au]:       "
        elif typ == "lmp2_corr":
            search_word = "DF-MP2 correlation energy [au]:   "
        elif typ == "mp2":
            search_word = "MP2 correlation energy [au]:   "
        elif typ == "lccsd":
            search_word = "CCSD correlation energy + 0.5 MP2 corrections [au]:"
        elif typ == "lccsdt_lccsd_tot":
            search_word = "Total LNO-CCSD energy with MP2 corrections [au]:"
        elif typ == "fnoccsdt_tot":
            search_word = "Total CCSD(T+) energy + MP2 + PPL corr. [au]"
        elif typ == "fnoccsd_tot":
            search_word = "Total CCSD energy + MP2 + PPL corr. [au]:"
        elif typ == "fnoccsdt_mp2_tot":
            search_word = "DF-MP2 energy [au]:"
        elif typ == "fnoccsdt":
            search_word = "CCSD(T+) correlation en. + MP2 + PPL corr. [au]:"
        elif typ == "fnoccsd":
            search_word = "CCSD correlation energy + MP2 + PPL corr. [au]:"
        elif typ == "fnoccsdt_mp2":
            search_word = "DF-MP2 correlation energy"

        elif typ == "ccsd":
            search_word = "CCSD correlation energy [au]: "
        elif typ == "ccsd_tot":
            search_word = "Total CCSD energy [au]: "
        elif typ == "dft":
            search_word = "***FINAL KOHN-SHAM ENERGY:"
        elif typ == "B2PLYP":
            search_word = "MP2 contribution [au]:"
        elif typ == "DSDPBEP86":
            search_word = "SCS-MP2 contribution [au]:"

        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            if typ == "dft":
                return float(a[-1].split()[-2])
            elif "fnoccsdt_mp2" in typ:
                return float(a[0].split()[-1])

            else:
                return float(a[-1].split()[-1])

    elif code_format == "vasp":
        search_word = "energy  without entropy="
        with open(filename, "r", encoding="ISO-8859-1") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-1])

    elif code_format == "quantum_espresso":
        search_word = "!    total energy              ="
        with open(filename, "r", encoding="ISO-8859-1") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-2])

    elif code_format == "cc4s":
        if typ == "CCSD corr":
            search_word = "Ccsd correlation energy:"
        elif typ == "CCSD FS":
            search_word = "Finite-size energy correction:"
        elif typ == "CCSD BSIE":
            search_word = "Ccsd-Bsie energy correction:"
        elif typ == "HF":
            search_word = "energy  without entropy="
        elif typ == "(T) corr":
            search_word = "(T) correlation energy:"
        elif typ == "MP2 FS":
            search_word = "Finite-size energy correction:"
        elif typ == "MP2 corr":
            search_word = "converged values  "

        with open(filename, "r", encoding="ISO-8859-1") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-1])

    elif code_format == "vasp_wodisp":
        search_word = "energy without entropy ="
        with open(filename, "r", encoding="ISO-8859-1") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-1])

    elif code_format == "dftd3":
        search_word = " Edisp /kcal,au"
        with open(filename, "r", encoding="ISO-8859-1") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-1])

    elif code_format == "orca":
        if typ == "lccsdt":
            search_word = "Final correlation energy"
        elif typ == "mp2":
            search_word = "E(MP2)"
        elif typ == "ccsd":
            search_word = "E(CORR)"
        elif typ == "ccsdt":
            search_word = "Final correlation energy"
        elif typ == "hf":
            search_word = "E(0)"
        elif typ == "hf_lmp2":
            search_word = "Total Energy"
        elif typ == "lmp2":
            search_word = "E(SL-MP2) including corrections"
        elif typ == "ri-mp2":
            search_word = "RI-MP2 CORRELATION ENERGY"
        # elif typ == 'mp2':
        #     search_word = 'MP2 correlation energy [au]:   '
        elif typ == "lccsd":
            search_word = "E(CORR)(corrected)"
        elif typ == "dft":
            search_word = "FINAL SINGLE POINT ENERGY"
        # elif typ == 'ccsd':
        #     search_word = 'CCSD correlation energy [au]: '
        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        elif typ == "hf_lmp2":
            return float(a[-1].split()[-4])
        elif typ == "ri-mp2":
            return float(a[-1].split()[-2])
        else:
            return float(a[-1].split()[-1])

    elif code_format == "orca_mp2":
        if typ == "lccsdt":
            search_word = "Final correlation energy"
        # elif typ == 'ccsdt':
        #     search_word = 'CCSD(T) correlation energy [au]:'
        elif typ == "hf":
            search_word = "Total energy after final integration"
        elif typ == "lmp2":
            search_word = "DLPNO-MP2 CORRELATION ENERGY"
        # elif typ == 'mp2':
        #     search_word = 'MP2 correlation energy [au]:   '
        elif typ == "lccsd":
            search_word = "E(CORR)(corrected)"
        # elif typ == 'ccsd':
        #     search_word = 'CCSD correlation energy [au]: '

        with open(filename, "r") as fp:
            a = [line for line in fp if search_word in line]
        if len(a) == 0:
            return 0.0
        else:
            return float(a[-1].split()[-2])
