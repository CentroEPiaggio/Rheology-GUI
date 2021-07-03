msgCase1 = "To achieve optimal LW at the specified LH, you can use EM values in between this range."
msgCase2 = "To achieve optimal LW at the given EM, you can use LH values in between this range."
msgCase3 = "The green line corresponds to the combination of LH and EM that gives the constrained LW.\n\
If the green line is under the printability window (shaded region), the LW is too small. If it is over the window, the LW is too high."
msgCase4 = "If the point is over the printability window (shaded region), then the resulting LW is too high. If it is lower than the window,\
then the LW is too thin."
msgCase5 = "For the given LH, you need this EM value to achieve the constrained LW. If the point is over the printability window (shaded region),\
 then the LW is too high; on the other hand, if it is lower than the window, the LW is too small."
msgCase6 = "For the given EM, you need this LH value to achieve the constrained LW. If the point is over the printability window (shaded region),\
 then the LW is too high; on the other hand, if it is lower than the window, the LW is too small."
msgCase7 = "The corrected LW represents the LW at the specified combination of EM and LH, which is plotted as a red point in the window.\
 The green line represents the combination of LH and EM that yields the constrained LW. Then, the line error is the difference between the constrained\
 LW and the corrected LW, expressed as a percentage. A positive value means that the printed LW will be greater than the desired one, while in the case of a\
 negative value it will be smaller."

msgRegion1 = "The Region 1 model outputs a minimum pressure required to extrude the material, alongside\
 the pressure to extrude the material at the given flow rate. \
Factors that may affect the pressure include:\n\
    * Needle length and diameter\n\
    * Flow rate\n\
    * Material properties"
msgRegion2 = "The Region 2 model yields a printability window, which can be used to choose the correct combination of\
 EM and LH. The shaded gray area represents the region in which the line has a correct width; above it, the line will be too thick,\
 which may cause material accumulation, while below it the line may be too thin and may break-up during printing."
msgRegion3 = "The Region 3 model output is a minimum infill density (or a maximum porosity value for the scaffold).\
 If an infill density is chosen below this value, there is a risk of printed filament collapse under its weight and reduced shape fidelity.\n\
Moreover, Region 3 also checks if, at this limiting infill, there is a collapse of the first (or more) layers on top of each other due to weight."