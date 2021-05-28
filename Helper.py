"""
Analysis : Text vs. Forms
For only one form to analyse
"""

#################### Enter your data information ################################################
RawData = "Data/Codings_Decrees_20_01_21.xlsx"
sheet_name_list = ["Synodal Decrees", "Comparative Corpus"] 

#sheet_name_list = ["Synodal Decrees"]
sub = ""#"Synodal/" # indicate the subfolder for the result (might need to be created), use "" for saving in the main figure folder Figures/

##################### what are the name of the texts you would like to analyse? Always between " " #####################
text_list = ["Hermopolisstele", "Hungersnotstele", "Satrapenstele", "Taimuthesstele", "Gallusstele",
             "Alexandriadekret", "Kanopusdekret", "Philensis II Dekret", "Rosettanadekret", 
             "Philensis I Dekret"]

##################### give the labels, format "Text":"Label" #####################
text_labels = {"Hermopolisstele":"V1", "Satrapenstele":"V2", "Hungersnotstele":"V3", "Taimuthesstele":"V4", "Gallusstele":"V5", "Pharaon 6":"V6", "Mimosa":"Mim",
             "Alexandriadekret":"S1", "Kanopusdekret":"S2", "Rosettanadekret":"S3", "Philensis II Dekret":"S4", "Philensis I Dekret":"S5"}


##################### give the dating, format "Text":"Dating" #####################
text_dating = {"Hermopolisstele":"377 BCE", "Hungersnotstele":"200 BCE", "Taimuthesstele":"100 BCE", "Gallusstele":"29 BCE", 
               "Satrapenstele":"311 BCE", "Mimosa":"000", "Alexandriadekret":"243 BCE", "Kanopusdekret":"238 BCE", 
               "Philensis II Dekret":"186 BCE", "Philensis I Dekret":"185 BCE", "Rosettanadekret":"196 BCE"}

##################### List of forms to analyse, format  "Accronym":"Description" ###########
form_labels = {"Vb": "Verbal forms",  "Comp":"Complete Code", "SP":"Sentence particles", "PI":"Particles I", "PII":"Particles II", "P":"Particles", "Subj": "Subjects"}
form_list = ["Vb", "Comp", "SP", "PI", "PII", "P", "Subj"]

################## Which form do you want to analyse? #################################
form = "Vb"

#### Would you like to study a particular group of forms? Yes = True, No = False ######
subset_rows = False 

#### If yes, what are the codes of your subset of forms ####################
form_codes_to_study = [322, 256, 378, 690, 999]  ### list will only be used if subset_rows = True (each one must be present in at least one of the text)

################# Would you like to annotate specific form code on the CA or MCMCA figures #######
annot_forms = [322, 256] # example 322 and 256 for verbs, add more if needed

################## Would you like to get the contingency table? ##################################
plot_contingency = True  # Figures/Separated/

################## Would you like to get the data table? #########################################
plot_data_table = True  # Figures/Separated/

################# Which method would you like to apply? ###################################
# Use "CA" to perform standard Correspondence Analysis
# Use "MCMCA" to perform Markov Chain Model Correspondence Analysis
method = "CA"

################# Is your dataset already a contingency table? Yes = True, No = False #######################
isCont = False

############### What is the p_value for significance filtering ############################
p_value = 0.05 # must be between 0 and 1, if not given then result is not filtered

################# How many factor dimensions to use on clustermap? #######################
### if not given then two factor dimensions will be used 
# cannot exceed the minimun between nr. of texts and nr. forms
num_dim_given = 5


################# Only for CA method, would you like a CA clustermap separated by axis ##############################
separate_by_axis = False

###################### Implementation : no changes required ##############################
# Results set in Figure/CA or Figure/MCMCA
from implementation import *    


             

