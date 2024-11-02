# gnathresh-solv
This is a toolkit that facilitates numerical experiments involving propogation thresholds in neuron models in [the NEURON software](https://www.neuron.yale.edu/neuron/).
This project began as an undergraduate research project aimed at modeling sodium channel density threshold (g_Na,Thresh) in rat neocortical cells, as described in [Munro & Kopell 2012](https://doi.org/10.1152/jn.00709.2011). Thus, some of the NMODL code in this repository (see /modfiles) is taken from that paper's source code ([ModelDB](https://modeldb.science/136309?tab=2&file=Munro_Kopell_corticalcontrol),  [github](https://github.com/ModelDBRepository/136309)).

# Usage
This code is for researchers using the NEURON software who seek to quickly calculate propagation thresholds in their models. It is more likely, however, that it will be used to recreate results found in \[an upcoming paper\], which uses this code.

Tools are organized into units known as 'environments,' which are classes whose instance attributes are akin to parameters/controlled variables of the experiments, and whose instance methods are akin to the execution of the experiments themselves. The purpose of the environment classes is to provide a quick & easy interface to the set of functions and data members required to preform a certain type of numerical experiment. For example, gnatsolv.enviro.death.DeathEnviro provides a *somewhat* optimized binary-search algorithm for finding the g_Na,Thresh of a resting cell that is briefly stimulated somewhere in the axonal tree.

The most useful pieces of this repository lie in the /src/gnatsolv/tools and /src/gnatsolv/enviro directories. The code therein can be set up to calculate other forms of propogation threshold just as easily as for calculating g_Na,Thresh.

There are additional tools for checking experimental integrity (checksum.py) and for visualizing membrane activity without generating pt3d geometry data, which is something that affects results (see [issue](https://github.com/neuronsimulator/nrn/issues/3171))
