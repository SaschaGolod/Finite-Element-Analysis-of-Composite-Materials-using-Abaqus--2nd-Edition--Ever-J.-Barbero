# srecover2D.py
from visualization import *
# Open the Output Data Base for the current Job
odb = openOdb(path='Job-1.odb');
myAssembly = odb.rootAssembly;

# Creating a temporary variable to hold the frame repository 
# provides the same functionality and speeds up the process
frameRepository = odb.steps['Step-2'].frames;

i = -1
# Get the results for frame [i], -1 is the last frame. 
frameS = frameRepository[i].fieldOutputs['S'].values;
frameE = frameRepository[i].fieldOutputs['E'].values;
frameIVOL = frameRepository[i].fieldOutputs['IVOL'].values;
Tot_Vol=0.;         # Total Volume
Tot_Stress=0.;      # Stress Sum
Tot_Strain = 0.;    # Strain Sum

# Calculate Average
for II in range(0,len(frameS)):
     Tot_Vol+=frameIVOL[II].data;
     Tot_Stress+=frameS[II].data * frameIVOL[II].data;
     Tot_Strain+=frameE[II].data * frameIVOL[II].data;

Avg_Stress = Tot_Stress/Tot_Vol;
Avg_Strain = Tot_Strain/Tot_Vol; 

print '2D Abaqus/Standard Stress Tensor Order: 11-22-33-12'
# from Abaqus Analysis User's Manual - 1.2.2 Conventions
print 'frame ', i
print 'Average stresses Global CSYS: 11-22-33-12';
print Avg_Stress,' TPa';
print 'Average strain Global CSYS: 11-22-33-12';
print Avg_Strain;
odb.close()