# Created by: Henry Stoldt
# June 2020

'''
.. note:: Not Implemented - Planning only
Objective: To make use of external aerodynamics data for a configuration, obtained from sources like CFD, flight, or wind tunnel experiments

Where will the data be used: In the rocket.getAppliedForce() function.

External data comes in the form of a data table including relevant 'key' columns (Ex: Mach, AOA, AOSS, Fin Deflections) and 'value' columns (Ex: Cl, Cd, Cm)
This data is loaded into a table for interpolation, and stored in a 'external aero data' object
    We can do n-dimensional linear interpolation with scipy's LinearNDInterpolator class. Not sure about higher-order interpolation - which would also require more data points
This object also precalculates OpenRocket aero predictions for each of the conditions for which external data is provided

The code will have two data interpolation modes:
    1) Dense-data mode: data is interpolated directly between external data points. OpenRocket models unused
    2) Sparse-data mode: data is interpolated directly between external data points, adjusted towards the OpenRocket model results.
        Adjustment strength is related to distance from external data points

Data extrapolation will work using the sparse-data mode.

Possible aero coefficients inputted:

Independent Variables:
Mach number
Reynolds number?
AOA
Roll Angle
Canard 1 Angle
Canard 2 Angle
Canard 3 Angle
Canard 4 Angle


OpenRocket/Dependent Variables:
CA = Axial drag force coeff
CD = Drag force coeff
Cf = Skin friction drag coefficient
Cl = Roll moment coefficient
Cld = Roll damping moment coefficient
Clf = Roll forcing moment coefficient
Cm = Pitch moment coefficient
Cma = Pitch moment coefficient derivative wrt AOA
CN = Normal force coefficient
CNa = Normal force coefficient derivative wrt AOA

Add command to output the columns expected in an externalData table for a given rocket
Have columns to interpolate over generated by the rocket at run time - interpolation info compiled while querying openrocket forces
Then interpolate + blend data
'''