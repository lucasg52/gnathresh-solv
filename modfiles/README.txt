
Lucas Swanson 7/6/2024
These files will be essential to recreating the results from the old code, since they appear to define some custom parameters that were used. 

see https://neuron.yale.edu/neuron/docs/using-nmodl-files
COMPILATION:
  To compile these files, run the bash script nrnivmodl
  This will create a directory named with your computer's architecture (usually x86_64) that contains object files (pieces of machine code) that NEURON loads for integrating physical variables with each timestep

USAGE:
  Once compiled, move the aforementioned directory to any directory where you will be launching python or NEURON gui to run simulations.
  
