import pandas as pd

##### Example for using Contingency Excel files #######
title = " Smoking tendency amongs staff"
##### 
row_val = "staff" # appears in figure name
col_val = "_smoking_" # appears in figure name
ColName = "Smoking"  # appears in figure title
RowName = "Staff" # appears in figure name

# load data
RawData = "Data/smoke.xls" ### You can download this dataset at http://www.carme-n.org/?sec=data7
RawData = pd.read_excel(RawData, engine='xlrd') # must be transformed into a panda dataframe

# in this setting, the column category data start at second column of dataset but you have change if needed, e.g., remove [1: ] if columns category names starts from first column of dataset 
data_dic = {cols:list(RawData[cols]) for cols in RawData.columns[1: ]} # in this example columns categories names starts at the second column index of RawData
# index = name of row categories, in this case row category name are given as first column of dataset but you can directly enter your row category names as a list, i.e., ["item_1", "item_2", ...]
row_list = list(RawData[RawData.columns[0]])

# Recreate the panda dataFrame
Data = pd.DataFrame(data = data_dic, index = row_list)

sub = ""
################# Which method would you like to apply? ###################################
# Use "CA" to perform Standard Correspondence Analysis
# Use "MCMCA" to perform MCM Correspondence Analysis
method = "CA"

################# How many factor dimensions to use on clustermap? #######################
### if not given then two factor dimensions will be used 
# cannot exceed the minimun between nr. of texts and nr. forms
num_dim_given = 4 # Only maximum 2 for TensorCA when using parameter rescale = True

################# Is your dataset already a contingency table? Yes = True, No = False #######################
isCont = True

############### What is the p_value for significance filtering ############################
p_value = 1 # must be between 0 and 1, if not given then result is not filtered

################# How many factor dimensions to use on clustermap? #######################
### if not given then two factor dimensions will be used 
# cannot exceed the minimun between nr. of texts and nr. forms
num_dim_given = 2 # Only maximum 2 for TensorCA when using parameter rescale = True

################# Only for CA method, would you like a CA clustermap separated by axis ##############################
separate_by_axis = False


################## Would you like to get the contingency table? ##################################
plot_contingency = True # Figures/Separated/

################## Would you like to get the data table? #########################################
plot_data_table = True  # Figures/Separated/

#### Would you like to study a particular subgroup of categories of the row variables (here forms)? Yes = True, No = False ######
subset_rows = False 


dtp = ("str", "str") # datatype for (rows,columns)

from implementation import *   #### line 6 of implementation.py must be set to --> from cHelper import *