import pandas as pd
import numpy as np
import pdb

def contingency(Data, row_vals, col_vals, missing = (False, False)):
    '''
    @brief           : - Build contingency matrix formed of the frequency of elements 
                         bellonging to categories in row and categories in columns
                       - return (Contigentency table, total number of Observations)
                       -        (ndarray, int)
    @params Data     : panda dataframe 
    @params row_vals : categories to consider in the rows
    @params col_vals : categories to consider in the columns
    @params missing       : list of bool (Imputation, NaNs as a row variable) 
                            either considering a simple uniform data imputation for missing observations
                            or considering missing variables as independend row values, 
                            or none of those 
                            value cannot be (True, True), this params is ignorned
    '''
    
    # column variables
    cols = col_vals
    
    # row variables
    rows = row_vals
    
    ##### treat missing observations as an independent row variable #####
    if missing[1] and not missing[0]:
        rows = list(rows)+["NaN"]
    
    Cont = np.zeros((len(rows), len(cols)), dtype = int)
    row_notin = []
    for i in range(len(rows)):
        for j in range(len(cols)):
            data_col = np.array(Data[cols[j]], dtype = float)
            if rows[i] == "NaN" and missing[1] and not missing[0]:
                Cont[i, j] = np.sum(np.isnan(data_col))
            else:
                Cont[i, j] = np.sum(data_col == rows[i]) 
        if np.sum(Cont[i,:])==0:
            row_notin.append(i)
    
    ##### treat missing observations: uniform imputation of missing variables #####
    if missing[0] and not missing[1]:
        total = len(rows)
        numMissing = np.sum(np.isnan(Data.to_numpy()))
        Cont = Cont + (1/total)*(numMissing)
        # turn counts to integer
        Cont = np.array(Cont, dtype=int)
    
    # create the contingency table by including the row variables which where present in the dataset
    if len(row_notin) == 0:        
        ContDataFrame = pd.DataFrame(data = Cont, index = rows.astype(int), columns = col_vals)
    
    else:
        indexes = np.arange(0, len(rows), 1, dtype = int)
        remove = indexes == row_notin[0]
        for k in range(1, len(row_notin)):
            remove += indexes == row_notin[k]
        
        ContDataFrame = pd.DataFrame(data = Cont[~remove, :], index = row_vals[~remove].astype(int), columns = col_vals)
        Cont = Cont[~remove, :]
    
    return Cont, np.sum(Cont), ContDataFrame 