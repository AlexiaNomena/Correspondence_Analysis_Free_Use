## Description
Perform standard correspondence analysis of two categorical variables (code module `ca.py` in the folder Methods/).
Software designed to be suitable for any users from any disciplines.

Code can be used to perform correspondence analysis on any dataset that can be transformed into a pandas DataFrame (see the code `ca.py` in the folder Methods/).

The method `mcmca.py` can be used for correspondence analysis of dataset that could be assumed to be generated from a Markov Chain Model.

## Specific Project
Project Ef5-4: "The evolution of Ancient Egyptian - Quantitative and Non- Quantitative Mathematical Linguistics".
Institutions: ZIB(Zuse Institute Berlin) & MATH+(Berlin Mathematics Research Center).

## Software requirements
python version: 3.7 or +
packages: numpy, pandas, matplotlib, matplotlib.pyplot, scipy, scipy.stats, seaborn.

You can also get all these using conda by creating a new environment with the spec file `myPy3_spec.txt` (for a guidance, click [here](https://conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html))

## Code Execution
### Users with little to no background in python 
`Helper.py`: performs one CA analysis (in this specific project: text vs. grammatical form) 

Please enter all the inputs by following the corresponding questions/decriptions.

`implementation.py` is required to obtain the CA figures.

### Users with a moderate background in python
`implementation.py` can be used to modify the default figure parameter settings. For further modifications, see all the codes in folder Methods/

If the dataset is already a contingency table, then the parameter `isCont` must be given as `True`.

## Data type
Numerical coding of texts in Égyptien de Tradition, each single data consisting of a ten digits number encoding for the grammatical structure of a sentence. 

Examples can be found [here](data_link).
Data/ can be used to include data.

## Results
Figures/ folder is the default location of figure outputs.

## Sample Figures

### Standard CA figure and a few statistics
Visualising the usual correspondence analysis results

### Association clustermap
Visualising the strenght of the association between the variables and identify similar clusters (similarity in the strenght of the associations)

### Variable clustermap
Identify similar clusters of variables (chi-square similarity)
 






