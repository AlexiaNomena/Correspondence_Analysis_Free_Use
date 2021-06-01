from Methods.Read_Data import *  # module for reading and cleaning the dataset
from Methods.ca import *         # module for standard correspondence analysis
from Methods.mcmca import *       # module for markov chain model correspondence analysis
from Methods.figure_maps import *  # module for clustermaps other maps

from Helper import *
### Clean data #######
if not isCont:
    Data = Cleaned_Data(RawData, sheet_name_list, columns_list, form = row_val, form_labels = rows_labels)
    '''
    @what Cleaned_Data does:    - clean the whole dataset to produce a panda dataframe of qualitative variables needed: text vs form
                                - text in the columns and form in the rows
                                - if form is None, then the analysis is text vs complete code
    
    @params RawData:          excel file containing code data
    @params sheet_name_list:  list of sheet names or sheet number to include in the analysis  [string, string, ....] or [int, int, int]
    @params text_list:        list of texts to include in the analysis                        [string, string, ....]
    @params form:             qualitative variables in the rows, values: "SP", "PI", "PII", "Vb", "Subj", "Comp"
    @params form_labels:      dictionary for the labels of te forms:                 {form:string, ....}
    '''
else:
    isCont = isCont
    ### You can directly enter your data as a contingency table, howvever you need to check if the row/columns category names are consistent ###
    import pandas as pd 
    # in this setting, the column category data start at second index of dataset but you have to check for consistency 
    data_dic = {cols:list(RawData[cols]) for cols in RawData.columns[1: ]}
    # Make the panda dataFrame. index = name of row categories, in this case row category name are given as first column of dataset but you have to check for consistency
    Data = pd.DataFrame(data = data_dic, index = list(RawData[RawData.columns[0]])) 

    
# Throw analysis figs in one pdf, specify the location and name of figure, the name of the row variabls is appended to it to differentiate the filename
from matplotlib.backends.backend_pdf import PdfPages
if method == "CA":# for CA
    method = CA
    if separate_by_axis:
        try:
            pdf= PdfPages("Figures/CA/"+sub+"CA_text_"+row_val+"_F1_to_F%d_separated.pdf"%num_dim_given)
        except:
            pdf= PdfPages("Figures/CA/"+sub+"CA_text_"+row_val+"_F1_to_F2_separated.pdf")
            
    else:
        try:
            pdf= PdfPages("Figures/CA/"+sub+"CA_text_"+row_val+"_F1_to_F%d_all.pdf"%num_dim_given)
        except:
            pdf= PdfPages("Figures/CA/"+sub+"CA_text_"+row_val+"_F1_to_F2_all.pdf")
            
    standard = True
    
    specify_rows = None
    specify_cols = None
    specific_rows_cols = (specify_rows, specify_cols) 
    

elif method == "MCMCA": # for MCMCA
    method = MCMCA
    pdf= PdfPages("Figures/MCMCA/"+sub+"MCMCA_text_"+row_val+".pdf")
    standard = False
    # specify which variables to show on the clustermap  # must be lists e.g. (np.arange(100, 120, dtype = int), None)
    specify_rows = None
    specify_cols = None
    specific_rows_cols = (specify_rows, specify_cols)
    
    

else:
    print("Method is not available")
    

# how many factor dimensions to use on the clustermap
try:
    num_dim = num_dim_given

except:
    num_dim = 2

# Throw other tables in one pdf
if plot_contingency:     
    pdf2 = PdfPages("Figures/"+"Contingency_text_%s.pdf"%row_val)

if plot_data_table:
    pdf3 = PdfPages("Figures/"+"Data_text_%s.pdf"%row_val)
    
# Row_Vals(Data) gives all the codes for the forms existing in the rows of the dataset
# Data.columns gives all the texts existing in the columns of the dataset 
AllCols = Data.columns
AllRows = Row_Vals(Data) # take all row elements of the dataset

# in case one only study a subset of the code
if subset_rows:
    AllRows = np.array(rows_to_study)


### annotate a specific form on the plot #####
try:
    rows_annot = []
    for s in range(len(annot_rows)):
        ind = np.where(AllRows == annot_rows[s])[0]
        if len(ind) >= 1: # row should appear only one time
            rows_annot = rows_annot + list(ind)
except:
    rows_annot = None


try:
    p_value = p_value
except:
    p_value = 1 # we do not filter by p_value
    
######### Analysis ##########        
Perform_CA, fig, contfig = method(Data, 
                row_vals = AllRows,   # List of form items to consider in the analysis (choose from codes of the forms)
                col_vals = AllCols,      # List of Text items to consider in the analysis (choose from texts_list)
                rows_to_Annot = rows_annot,         # indexes of the form items to annotate, if None then no annotation
                cols_to_Annot = np.arange(0,len(AllCols),  dtype=int), # indexes of the text items to annotate
                Label_rows = Row_Vals(Data),  # list of labels respectivelly corresponding to the form items that is in row_vals
                Label_cols = columns_labels,     # dictionary of labels respectivelly corresponding to the text items that are in col_vals
                cols_dating = columns_dating,    # dictionary of dates respectivelly corresponding to the text items that are in col_vals
                table = True,                 # Include summary table in the figure or not = True or False
                markers =[(".",10), ("+",30)],# pyplot markertypes, markersize: [(marker for the form items, size), (marker for the text items, size)] 
                col = ["grey", "red"],        # pyplot colortypes : [color for the form items, color for the text items]                  
                figtitle = "Text vs. " + rows_labels[row_val], # The title of the figure in the analysis
                outliers = (True, True), # to show (True) or not to show (False) the outliers of (row values, col values)
                p_val = p_value, # default is 0.01
                reverse_axis = False,    # True if reverse the order of the axis coordinates                      
                isCont = isCont          # input boolean parameter for: Is your data already a contingency table? 
                )


#save contingency table
if plot_contingency:
    pdf2.savefig(contfig, bbox_inches='tight', lw = 0.5)  

 #save data table
if plot_data_table:  
    fig2= pl.figure(figsize=(10,10))
    ax3 = fig2.add_subplot(211)
    pd.plotting.table(ax3, Data, loc="upper center", fontsize = 12)
    pl.title("Data table for text vs. "+rows_labels[row_val])
    ax3.axis("off")
    pdf3.savefig(fig2, bbox_inches = 'tight')

if (Perform_CA is not None)*(fig is not None): # means that the analysis was successfull
    pdf.savefig(fig, bbox_inches='tight') 
    
    
    # Plot clustermaps to see the correspondence within rows and columns
    ClustFigs = Cluster_maps(Perform_CA, 
                                   rows_labels[row_val], 
                                   Label_rows = Row_Vals(Data), 
                                   Label_cols = [columns_labels[c] for c in Data.columns], 
                                   standard = standard,
                                   num_dim = num_dim, 
                                   specific_rows_cols = specific_rows_cols, 
                                   axis_separation = separate_by_axis # parameter for CA only: if True then separate the clusters by axis, otherwise use the full plane
                                   )
    for i in range(len(ClustFigs)):
        pdf.savefig(ClustFigs[i], bbox_inches='tight')
    

pdf.close()

if plot_contingency: 
    pdf2.close()

if plot_data_table:
    pdf3.close()        
