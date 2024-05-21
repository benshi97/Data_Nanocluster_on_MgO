<a target="_blank" href="https://colab.research.google.com/github/benshi97/Data_Nanocluster_on_MgO/blob/main/analyse.ipynb">
  <img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/>
</a>

This repository accompanies the paper **Going for Gold(-Standard): Attaining Coupled Cluster Accuracy in Oxide-Supported Nanoclusters** by Benjamin X. Shi, David J. Wales, Angelos Michaelides and Chang Woo Myung.

The data for plotting all of the graphs in the main text and supplemental material can be found in the folder `Data`. The notebook `analyse.ipynb` can be explored interactively with [Colab](https://colab.research.google.com/github/benshi97/Data_Nanocluster_on_MgO/blob/main/analyse.ipynb). The figures generated by `analyse.ipynb` are stored in the `Figures` folder.


## Paper abstract

The structure of oxide-supported metal nanoclusters plays an essential role in their sharply enhanced catalytic activity over bulk metals. Simulations provide the atomic-scale resolution needed to understand these systems. However, the sensitive mix of metal-metal and metal-support interactions which govern their structure puts stringent requirements on the method used, requiring going beyond standard density functional theory (DFT). The method of choice is coupled cluster theory [specifically CCSD(T)], but its computational cost has so far prevented applications. In this work, we showcase two approaches to make CCSD(T) accuracy readily achievable in oxide-supported nanoclusters. First, we leverage the SKZCAM protocol to provide the first benchmarks of oxide-supported nanoclusters, revealing that it is specifically metal-metal interactions that are challenging to capture with DFT. Second, we propose a CCSD(T) correction (&Delta;CC) to the metal-metal interaction errors in DFT, reaching comparable accuracy to the SKZCAM protocol at significantly lower cost. This forges a path towards studying larger systems at reliable accuracy, which we highlight by identifying a ground state structure in agreement with experiments for Au<sub>20</sub> on MgO; a challenging system where DFT models have yielded conflicting predictions.
