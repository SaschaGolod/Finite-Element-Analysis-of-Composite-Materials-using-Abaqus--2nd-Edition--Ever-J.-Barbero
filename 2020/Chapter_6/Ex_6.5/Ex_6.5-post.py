""" Post-processing Ex. 6.5 """

# make sure the Work Directory is OK
import os
os.chdir(r'C:\SIMULIA\User\Chapter_6\Ex_6.5')

# Open the Output Database for the current Job
from visualization import *
odb = openOdb(path='Job-1.odb');
myAssembly = odb.rootAssembly;

# Create temporary variable to hold frame repository speeds up the process
frameRepository = odb.steps['Step-1'].frames;
frameS=[];
frameIVOL=[];

# Create a Coordinate System in the Laminate direction (Global)
coordSys = odb.rootAssembly.DatumCsysByThreePoints(name='CSYSLAMINATE',
    coordSysType=CARTESIAN, origin=(0,0,0),
    point1=(1.0, 0.0, 0), point2=(0.0, 1.0, 0.0) )

# Transform stresses from Lamina Coordinates 
# to Laminate Coordinate System defined in CSYSLAMINATE
# stressTrans=odb.steps['Step-1'].frames[-1].fieldOutputs['S']\
#   .getTransformedField(datumCsys=coordSys)
stressTrans=frameRepository[-1].fieldOutputs['S']\
    .getTransformedField(datumCsys=coordSys)

# Insert transformed stresses into frameS
frameS.insert(0,stressTrans.getSubset(position=INTEGRATION_POINT));
frameIVOL.insert(0,frameRepository[-1].fieldOutputs['IVOL']\
    .getSubset(position=INTEGRATION_POINT));

Tot_Vol=0;      # Total Volume
Tot_Stress=0;   # Stress Sum

for II in range(0,len(frameS[-1].values)):
     Tot_Vol=Tot_Vol+frameIVOL[0].values[II].data;
     Tot_Stress=Tot_Stress+frameS[0].values[II].data * frameIVOL[0]\
        .values[II].data;

#Calculate Average
Avg_Stress=Tot_Stress/Tot_Vol;
print 'Abaqus/Standard Stress Tensor Order:'
# From Abaqus Analysis User's Manual - 1.2.2 Conventions 
print ' 11-22-33-12-13-23';
print Avg_Stress;

print 'Laminate Gxy=',Avg_Stress[3]
