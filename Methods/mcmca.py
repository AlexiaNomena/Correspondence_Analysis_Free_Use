import numpy as np
import pandas as pd
import pdb
import scipy.stats as stats 
from .figure_settings import *

"""
@Brief: Markov Chain Model Correspondence Analysis
"""
#### Build the contigency table = Table of frequencies of each variables  #####
from .shared_func import contingency
           
#### Compute the stochastic matrix corresponding to a Markov Chain Model ####
def MatStochastic_infos(Data, row_vals, col_vals, missing, isCont = False):
    '''
    @brief           : - from the contingency table return three elements 
                       - (Stochastic Matrix, total number of observations, contingency dataframe)
                       - (array, array, ndarray, int)
    @params Data     : panda dataframe (without missing elements or NANs)
    @params row_vals : categories to consider in the rows
    @params col_vals : categories to consider in the columns
    @params missing       : list of bool (Imputation, NaNs as a row variable) 
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
    
    # Build the square matrix of contigency and it's transpose
    SqCont_upper = np.concatenate((np.zeros((Cont.shape[1], Cont.shape[1])), Cont.transpose()), axis = 1)
    SqCont_lower = np.concatenate((Cont, np.zeros((Cont.shape[0], Cont.shape[0]))), axis = 1)
    SqCont = np.concatenate((SqCont_upper, SqCont_lower), axis= 0)
    
    # sum of each rows of SqCont matrix. This operation is the same as computing:
    # the conditional proba wrt rows: each rows of Cont multiplied with the marjinal proba of the row in Cont 
    # the conditional proba wrt columns: each columns of Cont multiplied with the marjinal proba of the columns in Cont.transpose
    marj_sq= np.sum(SqCont, axis = 1)
    
    # stochastic matrix transition for the Markov Chain Model jumping from columns to columns and rows to rows of the dataset
    
    S = SqCont/marj_sq
    
    return S, Num_Obs, ContDataFrame

    
#### compute the factor coordinates (singular value decomposition) ####
def factors(Data, row_vals, col_vals, missing, isCont):
    '''
    @brief           :  - Eigendecomposition
                        - return a dict 
                        - {"Coord_rows"   : projection of the row items onto the factor space dim(rows)x(nr. factors)               (ndarray), 
                          "Coord_columns" : projection of the column items onto the factor space dim(columns)x(nr. factors)         (ndarray), 
                          
                          "Inertia"       : eigenvalues for each factors (ndarray), 
                          "Num_Obs"       : Total number of observation (array),
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
    
    # stochasitc matrix, total number of observations, contingency dataframe
    S, Num_Obs, ContDataFrame = MatStochastic_infos(Data, row_vals, col_vals, missing, isCont) 
     
    try:
        # eigendecomposition, using np.linalg.eig returns values with negligible imaginary parts 
        # therefore I use numpy.real() to remove the imaginary parts
        # eigendecomposition is not unique because eigenvalues are not distinct
        Evalues, Evectors = np.linalg.eig(S) # linalg.eig return normalised eigenvectors (constant*eigenvector is also an eigenvector)
        Evalues, Evectors = np.real(Evalues), np.real(Evectors)
        
        # Eigenvalues in descending order and corresponding Eigenvectors, the first eigenvalue is always 1
        sort = np.argsort(Evalues)[::-1]
        Evalues, Evectors = Evalues[sort], Evectors[:, sort]
        # Standard coordinates: coordinates of row on the principal axes
        
        #pdb.set_trace()
        remove = 1
        coord_rows =  Evectors[len(ContDataFrame.columns):, remove:]#np.sign(Evectors[np.newaxis, 0, remove:])
        
        # Standard coordinates: coordinates of columns on the principal axes
        coord_cols =  Evectors[:len(ContDataFrame.columns), remove:]#*np.sign(Evectors[np.newaxis, 0, remove:])
        
        return {"Coord_rows":coord_rows, "Coord_columns":coord_cols, 
                    "Num_Obs":Num_Obs, "Contingency":ContDataFrame, "Inertia": Evalues}
    except:
        print("Maybe eignevalue computation did not converge, there might be some NaNs in the Stochastic matrix")
        print("Check that there are no rows or columns with no information in the Data table")
        print("The row variables must be present in at least one of the columns of the Data table")



def MCMCA(Data, row_vals, col_vals, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, cols_dating = None, table = True, 
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
                            how to treat missing observations:
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True)
    @reverse_axis         : reverse the order of the axis coordinates         
    @p_val                : p value for chi_square test, not relevant here but just to not get errors in some other implementations
    @params isCont   : Boolean True if data is a contigency table and False if not and then to compute the contingency table          
    '''
    if (len(row_vals) == 1) + (len(col_vals) == 1) != 0:
        print("Data is one-dimensional, analysis cannot be done")
        return None, None, None
    
    else:
    
        # Get the output of function factors
        Fact = factors(Data, row_vals, col_vals, missing, isCont)
        
        Cont = Fact["Contingency"]
        Frame3 = Cont.copy()
        #pdb.set_trace()
        fig2=pl.figure(figsize=(10,10))
        ax3 = fig2.add_subplot(211)
        Frame3.columns = [c+"(%s)"%Label_cols[c] for c in Frame3.columns]
        pd.plotting.table(ax3, Frame3, loc="upper center", fontsize = 12)
        pl.title("Frequency table for "+figtitle)
        ax3.axis("off")
        if Fact is None:
            print("Data might not be feasible")
            return None, None, fig2
        
        else:
            # plot 2 components
            Coords_rows = Fact["Coord_rows"]
            Coords_cols = Fact["Coord_columns"]
            Inertia = Fact["Inertia"]
                
            fig, xy_rows, xy_cols = Display(Coords_rows, Coords_cols, Inertia, Data, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, 
                                  markers, col, figtitle, outliers,
                                  chosenAxes = np.array([0, 1]), 
                                  show_inertia = False, reverse_axis = reverse_axis)
                        
            # Columns labels table
            if cols_dating is not None:
                Labs = {f:[Label_cols[f]+" "+ cols_dating[f]] for f in Cont.columns}
            else:
                Labs = {f:[Label_cols[f]] for f in Cont.columns}
            # Add summary table to the figure
            if table:
                ax2 = fig.add_subplot(212)
        
                LabFrame = pd.DataFrame(Labs)
                pd.plotting.table(ax2, LabFrame, loc = "upper center", fontsize = 12)
        
                ax2.axis("off")
                ax2.set_aspect(1.0/(2.1*ax2.get_data_ratio()), adjustable='box')
        
            
                
            return {"rows_in_fig":xy_rows, "cols_in_fig":xy_cols, "Full_rows":Coords_rows, "Full_cols":Coords_cols, "chosenAxes":np.array([0, 1])}, fig, fig2
    

        
    
                    
    
