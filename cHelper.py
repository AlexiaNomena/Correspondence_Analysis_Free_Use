#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 14:04:43 2021

@author: araharin
"""

import pandas as pd


title = " Smoking tendency amongs staff"
# load data
RawData = "Data/smoke.xls"
RawData = pd.read_excel(RawData, engine='xlrd')

sub = ""
################# Which method would you like to apply? ###################################
# Use "CA" to perform Standard Correspondence Analysis
# Use "MCMCA" to perform MCM Correspondence Analysis
method = "MCMCA"

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
plot_contingency = False # Figures/Separated/

################## Would you like to get the data table? #########################################
plot_data_table = False  # Figures/Separated/

#### Would you like to study a particular subgroup of categories of the row variables (here forms)? Yes = True, No = False ######
subset_rows = False 


row_val = "smoking"
col_val = "_staff_"
ColName = "Staff"
RowName = "Smoking"

precision = 80

compute_rows = False
dtp = ("str", "str")

from implementation import *   #### line 6 of implementation.py must be set to --> from cHelper import *