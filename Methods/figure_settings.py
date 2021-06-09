import matplotlib
import matplotlib.pyplot as pl
import numpy as np
import scipy as scp
import pdb
import seaborn as sns


#### Visualisation ###  
def PreFig():
    '''
    @brief: customize figure parameters
    '''
    matplotlib.rc('xtick', labelsize=12) 
    matplotlib.rc('ytick', labelsize=12)


def Separation_axis(pl, ax, xy_rows, xy_cols, outliers, out = 1.2):
    outliers_rows, outliers_cols = outliers
    
    if outliers_rows*(not outliers_cols):
        print("remove outliers of columns variable")
        xmin, xmax = out*np.amin(xy_rows[:, 0]), out*np.amax(xy_rows[:, 0])
        ymin, ymax = out*np.amin(xy_rows[:, 1]), out*np.amax(xy_rows[:, 1])
        
    elif outliers_cols*(not outliers_rows):
        print("remove outliers of rows variable")
        xmin, xmax = out*np.amin(xy_cols[:, 0]), out*np.amax(xy_cols[:, 0])
        ymin, ymax = out*np.amin(xy_cols[:, 1]), out*np.amax(xy_cols[:, 1])
        
    elif (not outliers_rows)*(not outliers_cols):
        print("remove outliers of both rows and columns variables")
        out = 0.90
        xmin1, xmax1 = out*np.amin(xy_rows[:, 0]), out*np.amax(xy_rows[:, 0])
        ymin1, ymax1 = out*np.amin(xy_rows[:, 1]), out*np.amax(xy_rows[:, 1])
        
        xmin2, xmax2 = out*np.amin(xy_cols[:, 0]), out*np.amax(xy_cols[:, 0])
        ymin2, ymax2 = out*np.amin(xy_cols[:, 1]), out*np.amax(xy_cols[:, 1])
        
        xmin, xmax = min(xmin1, xmin2), min(xmax1, xmax2)
        ymin, ymax = min(ymin1, ymin2), min(ymax1, ymax2)
        
    else:
        print("plot all datapoints")
        xmin, xmax = ax.get_xlim()
        ymin, ymax = ax.get_ylim()
    
    pl.plot(np.linspace(xmin, xmax, 5), np.zeros(5), "--", color = "black", linewidth = 0.5)
    pl.plot(np.zeros(5), np.linspace(ymin, ymax, 5), "--", color = "black", linewidth = 0.5)
    
    pl.xlim((xmin, xmax))
    pl.ylim((ymin, ymax))
    
    return ax


def OneAnnotation(ax, lab, coords, col_val, xl, yl):
    ax.annotate("%s"%lab, xy=coords, 
                xytext= (xl, yl), textcoords='offset points', ha='center', va='bottom',
                bbox=dict(boxstyle='round,pad=0.2', fc=col_val, alpha=0.5),
                #arrowprops=dict(arrowstyle='->', #connectionstyle='arc3,rad=0.5', 
                #color= col_val,
                fontsize = 6
                 )
    return ax


def Annotate(ax, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, xy_rows, xy_cols, col):
    '''
    @brief : plot text annotations 
    @params: see function CA
    '''
    xmin, xmax = ax.get_xlim()
    ymin, ymax = ax.get_ylim()
    
    if rows_to_Annot is not None:
        pdist_n = scp.spatial.distance.pdist(xy_rows)
        pdist = scp.spatial.distance.squareform(pdist_n)
        pdist_n[~np.isnan(pdist_n)] = 10000000
        pdist_n[~np.isfinite(pdist_n)] = 10000000
        
        l_special = []
        for j in rows_to_Annot:
            #pdb.set_trace()
            if (np.sum(pdist[j, (j+1):] <= 0.20*np.mean(pdist_n)) != 0)*(j not in l_special)*(j != xy_rows.shape[0]-1):
                xl = 0
                yl = -10
                l_special.append(j)
            else:
                xl = 0
                yl = 2
            
            #if abs((np.linalg.norm(xy_rows[j, :]))/maxdist) >= 0.90:
            try:
                ax = OneAnnotation(ax, int(Label_rows[j]), xy_rows[j, :], "green", xl, yl)
            except:
                ax = OneAnnotation(ax, Label_rows[j], xy_rows[j, :], "green", xl, yl)
        
    
    if cols_to_Annot is not None:
        pdist_n = scp.spatial.distance.pdist(xy_cols)
        pdist = scp.spatial.distance.squareform(pdist_n)
        pdist_n[~np.isnan(pdist_n)] = 10000000
        pdist_n[~np.isfinite(pdist_n)] = 10000000
        
        l_special = []
        for j in cols_to_Annot:
            #pdb.set_trace()
            if (np.sum(pdist[j, (j+1):] <= 0.20*np.mean(pdist_n)) != 0)*(j not in l_special)*(j != xy_cols.shape[0]-1):
                xl = 0
                yl = -10
                l_special.append(j)
            else:
                xl = 0
                yl = 2
            
            ax = OneAnnotation(ax, Label_cols[j], xy_cols[j, :], "pink", xl, yl)
            
    return ax
            


def Display(Coords_rows, Coords_cols, Inertia, Data, rows_to_Annot, cols_to_Annot, Label_rows, Label_cols, 
            markers, col, figtitle, outliers, chosenAxes = np.array([0, 1]), show_inertia = True, reverse_axis = False):  
    """
    @brief: display results
    @params Fact: output of function factors
    @params chosenAxes: chose the two axis to plot
    @params other: see function CA
    """                       
        
    # plot 2 components
    PreFig()
    fig = pl.figure(figsize=(18,10))
    ax = fig.add_subplot(211)
    
    if reverse_axis:
        dim1, dim2 = Inertia[chosenAxes][::-1]
        xy_rows = Coords_rows[:, chosenAxes][:, ::-1] # [:, ::-1] reverse the order of the axis coordinates if necessary
        xy_cols = Coords_cols[:, chosenAxes][:, ::-1]
    else:
        dim1, dim2 = Inertia[chosenAxes]
        xy_rows = Coords_rows[:, chosenAxes] 
        xy_cols = Coords_cols[:, chosenAxes]
        
    # annotate points
    Cols_Labels = [Label_cols[c] for c in Data.columns]
    ax = Annotate(ax, rows_to_Annot, cols_to_Annot, Label_rows, Cols_Labels, xy_rows, xy_cols, col)

    ax.scatter(xy_rows[:, 0], xy_rows[:, 1], marker = markers[0][0], color = col[0], s = markers[0][1], label= "forms")
    ax.scatter(xy_cols[:, 0], xy_cols[:, 1], marker = markers[1][0], color = col[1], s = markers[1][1], label= "text")
    ax.legend(loc= (1.05, 0))
    
    
    # label factor axis
    if show_inertia: # show percentage of inertia
        #pl.xlabel("Dim %d (%.2f %%)"%(chosenAxes[0]+1, 100*dim1/np.sum(Inertia)), fontsize = 14)
        #pl.ylabel("Dim %d (%.2f %%)"%(chosenAxes[1]+1, 100*dim2/np.sum(Inertia)), fontsize = 14)
        pl.xlabel("Dim %d"%(chosenAxes[0]+1,), fontsize = 14)
        pl.ylabel("Dim %d"%(chosenAxes[1]+1,), fontsize = 14)
    else:
        pl.xlabel("Dim 1", fontsize = 14)
        pl.ylabel("Dim 2", fontsize = 14)
        
    # draw axis separation and limits depending on oulier parameters
    ax = Separation_axis(pl, ax, xy_rows, xy_cols, outliers)
    
    
    # aspect ratio of axis
    #ax.set_aspect(1.0/(1.25*ax.get_data_ratio()), adjustable='box')
    ax.set_aspect("equal")
    ax.set_xticks(())
    ax.set_yticks(())
    
    pl.title(figtitle)
    return fig, xy_rows, xy_cols
   




