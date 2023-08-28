#!/usr/bin/env python
# coding: utf-8

# Script to perform basis set extrapolation of HF and correlation energies for both the cc-pVXZ and def2-XZVP basis sets

import numpy as np
from ase.units import Hartree



def get_cbs(
    hf_X,
    corr_X,
    hf_Y,
    corr_Y,
    X=2,
    Y=3,
    family="cc",
    convert_Hartree=False,
    shift=0.0,
    output=True,
):
    """
    Function to perform basis set extrapolation of HF and correlation energies for both the cc-pVXZ and def2-XZVP basis sets
    
    Parameters
    ----------
    hf_X : float
        HF energy in X basis set
    corr_X : float
        Correlation energy in X basis set
    hf_Y : float
        HF energy in Y basis set where Y = X+1 cardinal zeta number
    corr_Y : float
        Correlation energy in Y basis set
    X : int
        Cardinal zeta number of X basis set
    Y : int
        Cardinal zeta number of Y basis set
    family : str
        Basis set family. Options are 'cc', 'def2', 'acc', and 'mixcc'. Where cc is for non-augmented correlation consistent basis sets, def2 is for def2 basis sets, acc is for augmented correlation consistent basis sets while mixcc is for mixed augmented + non-augmented correlation consistent basis sets
    convert_Hartree : bool
        If True, convert energies to Hartree
    shift : float
        Energy shift to apply to the CBS energy
    output : bool
        If True, print CBS energies

    Returns
    -------
    hf_cbs : float
        HF CBS energy
    corr_cbs : float
        Correlation CBS energy
    tot_cbs : float
        Total CBS energy
    """

    # Dictionary of alpha parameters followed by beta parameters in CBS extrapoation. Refer to: Neese, F.; Valeev, E. F. Revisiting the Atomic Natural Orbital Approach for Basis Sets: Robust Systematic Basis Sets for Explicitly Correlated and Conventional Correlated Ab Initio Methods. J. Chem. Theory Comput. 2011, 7 (1), 33–43. https://doi.org/10.1021/ct100396y.
    alpha_dict = {
        "def2_2_3": 10.39,
        "def2_3_4": 7.88,
        "cc_2_3": 4.42,
        "cc_3_4": 5.46,
        "cc_4_5": 5.46,
        "acc_2_3": 4.30,
        "acc_3_4": 5.79,
        "acc_4_5": 5.79,
        "mixcc_2_3": 4.36,
        "mixcc_3_4": 5.625,
        "mixcc_4_5": 5.625,
    }

    beta_dict = {
        "def2_2_3": 2.40,
        "def2_3_4": 2.97,
        "cc_2_3": 2.46,
        "cc_3_4": 3.05,
        "cc_4_5": 3.05,
        "acc_2_3": 2.51,
        "acc_3_4": 3.05,
        "acc_4_5": 3.05,
        "mixcc_2_3": 2.485,
        "mixcc_3_4": 3.05,
        "mixcc_4_5": 3.05,
    }

    # Check if X and Y are consecutive cardinal zeta numbers
    if Y != X + 1:
        print("Y does not equal X+1")

    # Check if basis set family is valid
    if family != "cc" and family != "def2" and family != "acc" and family != "mixcc":
        print("Wrong basis set family stated")

    # Get the corresponding alpha and beta parameters depending on the basis set family
    alpha = alpha_dict["{0}_{1}_{2}".format(family, X, Y)]
    beta = beta_dict["{0}_{1}_{2}".format(family, X, Y)]

    # Perform CBS extrapolation for HF and correlation components
    hf_cbs = hf_X - np.exp(-alpha * np.sqrt(X)) * (hf_Y - hf_X) / (
        np.exp(-alpha * np.sqrt(Y)) - np.exp(-alpha * np.sqrt(X))
    )
    corr_cbs = (X ** (beta) * corr_X - Y ** (beta) * corr_Y) / (
        X ** (beta) - Y ** (beta)
    )

    # Convert energies from Hartree to eV if convert_Hartree is True
    if convert_Hartree == True:
        if output == True:
            print(
                "CBS({0}/{1}) HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}".format(
                    X,
                    Y,
                    hf_cbs * Hartree + shift,
                    corr_cbs * Hartree,
                    (hf_cbs + corr_cbs) * Hartree + shift,
                )
            )
        return (
            hf_cbs * Hartree + shift,
            corr_cbs * Hartree,
            (hf_cbs + corr_cbs) * Hartree,
        )
    else:
        if output == True:
            print(
                "CBS({0}/{1})  HF: {2:.9f} Corr: {3:.9f} Tot: {4:.9f}".format(
                    X, Y, hf_cbs + shift, corr_cbs, (hf_cbs + corr_cbs) + shift
                )
            )
        return hf_cbs + shift, corr_cbs, (hf_cbs + corr_cbs) + shift

