import lasio as ls
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
%matplotlib inline

def calc_overburden_psig(las_file, dens_curv, depth_curv, acc=9.8):
    # pa to psig = 0.000145038
    las_file["OBG"] = dens_curv * 1000 * acc * 0.1524 *0.000145038  # pa
    las_file["OBG_inc"] = las_file["OBG"].cumsum() + 3600
    # 3600 compensates for the missing logging interval
def calc_nomral_trend(las_file):
    #get coeficients
    polyfit = np.polyfit(las_file.depth_m, las_file["DT"], deg=2)
    #create a fitting function from coef
    polyfunc = np.poly1d(polyfit)
    y_fitted = polyfunc(las_file.depth_m)
    las_file["NCL"] = y_fitted

toplot = ["GR","RHOB", "DT", "OBG_inc"]
colors = ["green","red", "blue", "black"]

#Load las file and convert to pandas DataFrame
las_file = ls.read("volve.LAS")
las_file = las_file.df()
#Load calibration file, Depth, Pressure
calib_df = pd.read_csv("calb.txt", sep="\t")
las_file["depth_m"] = las_file.index
# create a filter for our data frame to avoid convergence issues
las_file = las_file[ las_file["DT"] > 0 ]

#Calculate necessary parameter for pore pressure
calc_overburden_psig(las_file, las_file["RHOB"], las_file["depth_m"])
calc_nomral_trend(las_file)

# mud density HP = 0.052 * dens * depth_ft
#                = 0.052 * 8.33 lb/gal  * depth_ft
                #= 0.433 * depth_ft

density_grad = 0.433
las_file["Mud"] = density_grad*las_file.depth_m * 3.28
las_file["PP-3"] = las_file["OBG_inc"] - ((las_file["OBG_inc"] - las_file["Mud"])*(las_file.NCL/las_file["DT"])**3)
las_file["PP-2.5"] = las_file["OBG_inc"] - ((las_file["OBG_inc"] - las_file["Mud"])*(las_file.NCL/las_file["DT"])**2.5)
las_file["PP-2"] = las_file["OBG_inc"] - ((las_file["OBG_inc"] - las_file["Mud"])*(las_file.NCL/las_file["DT"])**2)
# create a filter to delete the negative values
las_file = las_file[  las_file["PP-3"] >= 0  ]
las_file = las_file[  las_file["PP-2.5"] >= 0  ]
las_file = las_file[  las_file["PP-2"] >= 0  ]
#Create the subplot
fig, axs = plt.subplots(1,4, sharey=True, figsize=(15,30))

# lets plot everything
for i in range(   len(toplot) ):
    #for i in range(0, len(toplot) )
    var = toplot[i]
    clr = colors[i]
    axs[i].plot(las_file[var], las_file.depth_m, label=var, color=clr)    
    axs[i].legend();axs[i].grid()

#view the compaction trend line
axs[2].plot(las_file.NCL, las_file.depth_m, color="black")
#plotting the pore pressure
axs[3].plot(las_file["PP-3"], las_file.depth_m, ls="dashed", lw=0.5, label="Pore Pressure n=3")
axs[3].plot(las_file["PP-2.5"], las_file.depth_m, ls="dashed", lw=0.5, label="Pore Pressure n=2.5")
axs[3].plot(las_file["PP-2"], las_file.depth_m, ls="dashed", lw=0.5, label="Pore Pressure n=2")

axs[3].scatter(calib_df["FP"]*14.5, calib_df.MD,
               label="WL - Formation Pressure", 
               c="brown", marker="*", s=10)
axs[3].legend()
axs[0].invert_yaxis()

fig.tight_layout()
fig.savefig("pore pressure.pdf")

#exporting the work...
las_file.to_excel("pore pressure.xlsx")
las_file.to_csv("pp.csv")




