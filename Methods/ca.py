import numpy as np
import pandas as pd
import pdb
import scipy.stats as stats 
from .figure_settings import *

"""
@Brief: Standard Correspondence Analysis
"""
#### Build the contigency table = Table of frequencies of each variables  #####
from .shared_func import contingency   
           
#### Compute the matrix Marginals and deviation from Marginals (deviation from independence) ####
def Deviation_infos(Data, row_vals, col_vals, missing, isCont = False):
    '''
    @brief           : - from the contingency table return seven elements 
                       - (marjinal proba of the row variables, marjinal proba of the column variables, 
                          Matrix deviation from independence, total number of observations, 
                          contingency dataframe,
                          inverse square root of row marjinals, inverse square root of columns marjinals)
                       - (array, array, ndarray, int)
    @params Data     : panda dataframe (without missing elements or NANs)
    @params row_vals : categories to consider in the rows
    @params col_vals : categories to consider in the columns
    @params missing  : list of bool (Imputation, NaNs as a row variable) 
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True)
    @params isCont   : Boolean True if data is a contigency table and False if not and then to compute the contingency table 
    '''
    
    # contigency
    if isCont:
        Cont, Num_Obs, ContDataFrame = Data.to_numpy(dtype=float), np.sum(Data.to_numpy(dtype=float)), Data
    else:
        Cont, Num_Obs, ContDataFrame = contingency(Data, row_vals, col_vals, missing)
    
    # table of joint proba
    joint_proba = Cont/Num_Obs
    
    # marjinals of the rows, vector composed of the marjinals of each row
    marj_rows= np.sum(joint_proba, axis = 1)
    
    # marginals of the columns, vector composed of the marjinals of each column 
    marj_columns = np.sum(joint_proba, axis=0)

        
    # Compute deviation matrix Conditional proba minus the product of the marginals
    D = joint_proba - marj_rows[:, np.newaxis]*marj_columns
    
    # Standardise the deviation matrix

    Dr = np.diag(1/np.sqrt(marj_rows))
    Dc = np.diag(1/np.sqrt(marj_columns))
    
    D = Dr.dot(D.dot(Dc))
    
    return marj_rows, marj_columns, D, Num_Obs, ContDataFrame, Dr, Dc
       
#### compute the factor coordinates (singular value decomposition) ####
def factors(Data, row_vals, col_vals, missing, isCont):
    '''
    @brief           : - Singular value decomposition
                       - return a dict 
                       - {"Coord_rows"     : projection of the row items onto the factor space dim(rows)x(nr. factors)              (ndarray), 
                          "Coord_columns"  : projection of the column items onto the factor space dim(columns)x(nr. factors)        (ndarray), 
                          "Factor_rows"    : the contribution of each rows to each factor space dim(rows)x(nr. factors)             (ndarray),
                          "Factor_columns" : the contribution of each columns to each factor space dim(columns)x(nr.factors)        (ndarray),
                          
                          "Inertia"       : square of singular values = eigenvalues for each factors (ndarray), 
                          "Num_Obs"       : Total number of observation (array), 
                          "Deg_Freedm"    : Degree of freedom of the Dataset (integer),
                          "Contingency"   : Contingency DataFrame}
    @params Data     : panda dataframe, missing elements (NaNs) will be ignored
    @params row_vals : categories to consider in the rows
    @params col_vals : categories to consider in the columns
    @params missing       : list of bool (Imputation, NaNs as a row variable) 
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True)
    @params isCont   : Boolean True if data is a contigency table and False if not and then to compute the contingency table 
    '''
    
    # marjinals of row, marjinals of columns, matrix deviation from independence, total number of observations, contingency dataframe
    
    marj_rows, marj_columns, D, Num_Obs, ContDataFrame, Dr, Dc = Deviation_infos(Data, row_vals, col_vals, missing, isCont)  

    # singular value decomposition D.shape = (M, N), U.shape(M, K), len(Svalues) = K, VT.shape(K,N), K=min(M,N) <-- due to param full_matrice = False
    try:
        U, Svalues, VT = np.linalg.svd(D, full_matrices = False) 
        
        V = VT.transpose()
        #Sigma = np.zeros((len(Svalues), len(Svalues)))
        Sigma = np.diag(Svalues)
    
        # Standard coordinates: coordinates of row on the principal axes
        coord_rows = Dr.dot(U)
        
        # Standard coordinates: coordinates of columns on the principal axes
        coord_cols = Dc.dot(V)
        
        # row factors/principal coordinates: contribution of the row profiles on each axis corresponding to the singular values
        Factors_rows = Dr.dot(U.dot(Sigma))
        
        # column factors/principal coordinates:contribution of the colum profiles on each axis corresponding to the singular values
        Factors_cols = Dc.dot(V.dot(Sigma))
        
        return {"Coords_rows":coord_rows, "Coords_columns":coord_cols, "Factors_rows":Factors_rows, "Factors_columns": Factors_cols, "Inertia":Svalues**2, 
                    "Num_Obs":Num_Obs, "Deg_Freedm":(len(marj_rows)-1)*(len(marj_columns)-1), "Contingency":ContDataFrame, 
                    "marj_rows": marj_rows, "marj_cols":marj_columns, "Residuals":D}
    except:
        print("Maybe SVD did not converge, there might be some NaNs in the Deviation matrix")
        print("Check that there are no rows or columns with no information in the Data table")
        print("The row variables must be present in at least one of the columns of the Data table")
        
    
#### A few summary tables and chi-square test ####            
def CA_Summary(Fact, missing, contributions_nans = None):
    '''
    @brief : build summary table for correspondence analysis
    @params Fact: output of function factors
    @params missing       : list of bool (Imputation, NaNs as a row variable) 
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True)
    '''
    # Inertia
    Inertia = (Fact["Inertia"])
    
    # Percentage Inertia
    Perc_I = 100*Inertia/np.sum(Inertia)
    
    # Chi_square
    Num_Obs = Fact["Num_Obs"]
    Chi_square = Num_Obs*np.sum(Inertia)

    # p_value 
    degree_freedom = Fact["Deg_Freedm"]
    p_value = 1 - stats.chi2.cdf(Chi_square, degree_freedom)
    
    # print summary table
    if missing[1] and not missing[0]:
        sort_contr = np.argsort(contributions_nans)[::-1] # sort in descending order
        Inertia = Inertia[sort_contr]
        contributions_nans = contributions_nans[sort_contr]*100
        Perc_I = Perc_I[sort_contr]
        T1 = {"Dimensions":["F%d"%i for i in sort_contr+1], "Inertia":["%.4f"%val for val in Inertia], 
                            "Perc_Inertia":["%.2f"%perc for perc in Perc_I], "NaNs CTR (perc.)":["%.2f"%c for c in contributions_nans]}
        
    else:
        T1 = {"Dimensions":["F%d"%i for i in range(1,len(Inertia)+1)], "Inertia":["%.2f"%val for val in Inertia], "Perc_Inertia":["%.2f"%perc for perc in Perc_I]}
    
    T2 = {"Chi_square":["%.3f"%Chi_square], "df":["%d"%degree_freedom], "p_value":["%.3f"%p_value]}
    Frame2 = pd.DataFrame(T2)

    Frame1 = pd.DataFrame(T1)

    Frame3 = Fact["Contingency"]
    print("---------------------------------")
    print(Frame1)
    print("---------------------------------")
    print(Frame2)
    print("---------------------------------")
    print(Frame3)
    print("---------------------------------")

    return Frame1, Frame2, Frame3, p_value

def WhichAxes(Fact, missing = (False, False)):
    contributions_nans = None
    Inertia = Fact["Inertia"]

    if missing[1] and not missing[0]:
        # Nan is one of the last row variables 
        Coords_rows = Fact["Factors_rows"]
        contributions_nans = Fact["marj_rows"][-1]*Coords_rows[-1, :]**2/np.sum(Inertia)
        sort_contr = np.argsort(contributions_nans)[::-1] # sort in descending order
        test = contributions_nans[sort_contr] <= 0.5 
        
        chosenAxes = sort_contr[test][:2]
        
    else:
        indexes = np.arange(0, len(Inertia), 1., dtype = int )
        test = (indexes == 0) + (indexes == 1)
        chosenAxes = indexes[test]
    
    return contributions_nans, chosenAxes 
 

def CA(Data, row_vals, col_vals, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, cols_dating = None, table = True, 
          markers = [("o", 50), ("o",50)], col = ["grey", "red"], figtitle="None", outliers = (True, True),
          missing = (False, False), reverse_axis = False, p_val = 0.01, isCont = False): 
    '''
    @brief: perform correspondence analysis and return summarry table and figure
    @params Data          : panda dataframe (without missing elements or NANs)
    @params row_vals      : list of categories to consider in the rows (list or array)
    @params col_vals      : list categories to consider in the columns (list or array)
    @params rows_to_Annot : list of index of the row items to annotate, if None then no annotation (list or array)
    @params cols_to_Annot : list of index of the row items to annotate, if None then no annotation (list or array)
    @params Labels_rows   : list of labels respectivelly corresponding to the row items that is in row_vals
    @params Labels_rows   : list of labels respectivelly corresponding to the column items that is in col_vals
    @params table         : Include summary table in the plot or not (bool)
    @params markers       : pyplot markertypes, markersize: [ (marker for the form items, size), (marker for the text items, size)] 
    @params col           : pyplot colortypes : [color for the form items, color for the text items]  
    @params figtitle      : The title of the figure in the analysis (string)
    @params figfilename   : Name of the figure file to save (string)
    @params outliers      : Include or not oultiers of row item, outliers of column items (Boolean, Boolean)
    @params missing       : list of bool (Imputation, NaNs as a row variable)
                            # how to treat missing observations:
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True)
    @reverse_axis         : reverse the order of the axis coordinates 
    @p_val                : p value for chi_square test
    @params isCont   : Boolean True if data is a contigency table and False if not and then to compute the contingency table                     
    '''
    if (len(row_vals) == 1) + (len(col_vals) == 1) != 0:
        print("Data is one-dimensional, analysis cannot be done")
        return None, None, None
    
    else:
    
        # Get the output of function factors
        Fact = factors(Data, row_vals, col_vals, missing, isCont)
        
        if Fact is None:
            print("Data might not be feasible")
            return None, None, None

        else:
            # Simple summary, contingency, and p_values
            contributions_nans, chosenAxes = WhichAxes(Fact, missing)
            Frame1, Frame2, Cont, p_value = CA_Summary(Fact, missing, contributions_nans) 
            
            Frame3 = Cont.copy()        
            fig2=pl.figure(figsize=(10,10))
            ax3 = fig2.add_subplot(211)
            Frame3.columns = [c+"(%s)"%Label_cols[c] for c in Frame3.columns]
            pd.plotting.table(ax3, Frame3, loc="upper center", fontsize = 12)
            pl.title("Frequency table for "+figtitle)
            ax3.axis("off")
            
            if p_value > p_val:
                print("###################################################################")
                print("Requested p_value level is not achieved, thus no result is plotted")
                print("###################################################################")
                
                return None, None, fig2
            
            else:
                Coords_rows = Fact["Factors_rows"]
                Coords_cols = Fact["Factors_columns"]
                Inertia = Fact["Inertia"]
                
                fig, xy_rows, xy_cols = Display(Coords_rows, Coords_cols, Inertia, Data, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, 
                                  markers, col, figtitle, outliers,
                                  chosenAxes = chosenAxes, 
                                  show_inertia = True, reverse_axis = True)
                
                # Print simple summary table
                # Columns labels table
                if cols_dating is not None:
                    Labs = {f:[Label_cols[f]+" "+ cols_dating[f]] for f in Cont.columns}
                else:
                    Labs = {f:[Label_cols[f]] for f in Cont.columns}
                    
                # Add summary table to the figure
                if table:
                    ax2 = fig.add_subplot(212)
            
                    pd.plotting.table(ax2, Frame1, loc = "center", fontsize = 12)
                    pd.plotting.table(ax2, Frame2, loc = "lower center", fontsize = 12)
                    
                    LabFrame = pd.DataFrame(Labs)
                    pd.plotting.table(ax2, LabFrame, loc = "upper center", fontsize = 12)
            
                    ax2.axis("off")
                    ax2.set_aspect(1.0/(2.1*ax2.get_data_ratio()), adjustable='box')
                    #ax2.set_aspect("equal")
            
                
                
                            
                
                return {"rows_in_fig":xy_rows, "cols_in_fig":xy_cols, "Full_rows":Coords_rows, "Full_cols":Coords_cols, "chosenAxes":chosenAxes, "Residuals":Fact["Residuals"], "Full_result":Fact}, fig, fig2
           

        
    
                    
    
