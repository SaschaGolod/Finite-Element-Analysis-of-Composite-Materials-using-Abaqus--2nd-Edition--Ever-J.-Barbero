# Begin the Post-Processing
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# Open The Output Data Base of the Current Job
odb = openOdb(path='Job-1.odb');
myAssembly = odb.rootAssembly;

# Creating a temporary variable to hold the frame repository 
# provides the same functionality and speeds up the process
frameRepository = odb.steps['Step-Gamma13'].frames;
frameE=[];
frameS=[];
frameIVOL=[];

# Get only the last frame [-1]
frameE.insert(0,frameRepository[-1].fieldOutputs['E'].getSubset(position=INTEGRATION_POINT));
frameS.insert(0,frameRepository[-1].fieldOutputs['S'].getSubset(position=INTEGRATION_POINT));
frameIVOL.insert(0,frameRepository[-1].fieldOutputs['IVOL'].getSubset(position=INTEGRATION_POINT));

# Total Volume, Strain, Stress
Tot_Vol=0;
Tot_Strain=0;
Tot_Stress=0;

for II in range(0,len(frameS[-1].values)):
     Tot_Vol=Tot_Vol+frameIVOL[0].values[II].data;
     Tot_Strain=Tot_Strain+frameE[0].values[II].data * frameIVOL[0].values[II].data;
     Tot_Stress=Tot_Stress+frameS[0].values[II].data * frameIVOL[0].values[II].data;

# Calculate Average
Avg_Strain=Tot_Strain/Tot_Vol;
Avg_Stress=Tot_Stress/Tot_Vol;

print 'Abaqus/Standard Stress Tensor Order:'
# From Abaqus Analysis User's Manual - 1.2.2 Conventions
# Convention used for stress and strain components
print ' 11-22-33-12-13-23';
print Avg_Strain;
print Avg_Stress;
print 'G12=',Avg_Stress[-1]
