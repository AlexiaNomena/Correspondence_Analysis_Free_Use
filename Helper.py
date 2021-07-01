"""
Analysis : Text vs. Forms
For only one form to analyse
"""

#################### Enter your own data information as in the example here, enter your own data file locations ###########################################
#################### Replace with your own row/column category/names in your excel data file ##############################################################

RawData = "Data/Codings_Decrees_20_01_21.xlsx" # your data file name, including it's location
sheet_name_list = ["Synodal Decrees", "Comparative Corpus"] # the specific names of the excel sheets you would like to include in the analysis

### indicate the folder inside Figures/CA/ Figures/CA/MCMCA in which to put the result (might need to be created), e.g., "Synodal/" but use "" for saving in the figure results folders
sub = ""   

##################### What are the name of the categories of column variable (here texts) you would like to analyse? Always between " " #####################
##################### Replace with your own column category names in your excel data file ###################################################################
columns_list = ["Hermopolisstele", "Hungersnotstele", "Satrapenstele", "Taimuthesstele", "Gallusstele",
             "Alexandriadekret", "Kanopusdekret", "Philensis II Dekret", "Rosettanadekret", 
             "Philensis I Dekret"]

##################### Give the labels of your column category, format "Column_category":"Label" #####################
columns_labels = {"Hermopolisstele":"V1", "Satrapenstele":"V2", "Hungersnotstele":"V3", "Taimuthesstele":"V4", "Gallusstele":"V5", "Pharaon 6":"V6", "Mimosa":"Mim",
             "Alexandriadekret":"S1", "Kanopusdekret":"S2", "Rosettanadekret":"S3", "Philensis II Dekret":"S4", "Philensis I Dekret":"S5"}

##################### give the dating, format "Colunm_category":"Dating" #####################
columns_dating = {"Hermopolisstele":"377 BCE", "Hungersnotstele":"200 BCE", "Taimuthesstele":"100 BCE", "Gallusstele":"29 BCE", 
               "Satrapenstele":"311 BCE", "Mimosa":"000", "Alexandriadekret":"243 BCE", "Kanopusdekret":"238 BCE", 
               "Philensis II Dekret":"186 BCE", "Philensis I Dekret":"185 BCE", "Rosettanadekret":"196 BCE"}

##################### List of possible row variables to analyse (here grammatical forms), format  "Accronym":"Description" ###########
rows_labels = {"Vb": "Verbal forms",  "Comp":"Complete Code", "SP":"Sentence particles", "PI":"Particles I", "PII":"Particles II", "P":"Particles", "Subj": "Subjects"}
rows_list = ["Vb", "Comp", "SP", "PI", "PII", "P", "Subj"]

#################### Which specific row variable (here form) do you want to analyse? ##########################################################################
row_val = "Vb"     # appears in figure name
col_val = "_text_" # appears in figure name
ColName = "Texts" # appears in figure title
RowName = rows_labels[row_val] # appears in figure title
dtp = ("int", "str")


#################### Would you like to study a particular subgroup of categories of the row variables? Yes = True, No = False #################################
subset_rows = False 

#################### If yes, what are the codes of your subgroup of categories of the row variables (here forms codes) ########################################
#################### Replace with your own row category names in your excel data file #########################################################################
rows_to_study = [322, 256, 378, 690, 999]  ### list will only be used if subset_rows = True (each one must be present in at least one of the text)

################# Would you like to annotate a specific row category on the CA or MCMCA figures #######
annot_rows = [322, 256] # example 322 and 256 for verbs, add more if needed

################## Would you like to get the contingency table? #######################################
plot_contingency = True  # Figures/

################## Would you like to get the data table? ##############################################
plot_data_table = True  # Figures/

##################### Which method would you like to apply? ###################################################################################################
# Use "CA" to perform standard Correspondence Analysis
# Use "MCMCA" to perform Markov Chain Model Correspondence Analysis
method = "MCMCA"

################# Is your dataset already a contingency table? Yes = True, No = False #######################
isCont = False

############### What is the p_value for significance filtering ############################
p_value = 0.05 # must be between 0 and 1, if not given then result is not filtered

################# How many factor dimensions to use on clustermap? ########################
### if not given then two factor dimensions will be used 
# cannot exceed the minimun between nr. of texts and nr. forms
num_dim_given = 5

################# Only for CA method, would you like a CA clustermap separated by axis ##############################
separate_by_axis = False # if True, this does not work for the parts of the axis in which there is only one category in it.

##################### Implementation : no changes required ####################################################################################################
# Results can be found in Figure/CA or Figure/MCMCA
from implementation import *    #### line 6 of implementation.py must be set to --> from cHelper import*


             

