#Begin Post Processing
#Open the Output Data Base for the current Job
from visualization import *
odb = openOdb(path='Job-1.odb', readOnly=True);#avoid warning
myAssembly = odb.rootAssembly;

#Creating a temporary variable to hold the frame repository provides the same functionality and speeds up the process
frameRepository = odb.steps['Column-1'].frames;
frameS=[];
frameIVOL=[];
#Get only the last frame [-1]
frameS.insert(0,frameRepository[-1].fieldOutputs['S'].getSubset(position=INTEGRATION_POINT));
frameIVOL.insert(0,frameRepository[-1].fieldOutputs['IVOL'].getSubset(position=INTEGRATION_POINT));
#Total Volume
Tot_Vol=0;
#Stress Sum
Tot_Stress=0;
#
for II in range(0,len(frameS[-1].values)):
     Tot_Vol=Tot_Vol+frameIVOL[0].values[II].data;
     Tot_Stress=Tot_Stress+frameS[0].values[II].data * frameIVOL[0].values[II].data;

#Calculate Average
Avg_Stress = Tot_Stress/Tot_Vol;
#print 'Abaqus/Standard Stress Tensor Order:'
#From Abaqus Analysis User's Manual - 1.2.2 Conventions - Convention used for stress and strain components
#print 'Average stresses Global CSYS: 11-22-33-12-13-23';
#print Avg_Stress;
C11 = Avg_Stress[2]#z-component,1-direction
C21 = Avg_Stress[0]#x-component,2-direction
C31 = Avg_Stress[1]#y-component,3-direction in Fig. 6.5

#Srecover macro--need to make this into a Python function
#Creating a temporary variable to hold the frame repository provides the same functionality and speeds up the process
frameRepository = odb.steps['Column-2'].frames;
frameS=[];
frameIVOL=[];
#Get only the last frame [-1]
frameS.insert(0,frameRepository[-1].fieldOutputs['S'].getSubset(position=INTEGRATION_POINT));
frameIVOL.insert(0,frameRepository[-1].fieldOutputs['IVOL'].getSubset(position=INTEGRATION_POINT));
#Total Volume
Tot_Vol=0;
#Stress Sum
Tot_Stress=0;
#
for II in range(0,len(frameS[-1].values)):
     Tot_Vol=Tot_Vol+frameIVOL[0].values[II].data;
     Tot_Stress=Tot_Stress+frameS[0].values[II].data * frameIVOL[0].values[II].data;

#Calculate Average
Avg_Stress = Tot_Stress/Tot_Vol;
#print 'Abaqus/Standard Stress Tensor Order:'
#From Abaqus Analysis User's Manual - 1.2.2 Conventions - Convention used for stress and strain components
#print 'Average stresses Global CSYS: 11-22-33-12-13-23';
#print Avg_Stress;
C12 = Avg_Stress[2]#z-component,1-direction
C22 = Avg_Stress[0]#x-component,2-direction
C32 = Avg_Stress[1]#y-component,3-direction in Fig. 6.5

#Srecover.py
#Creating a temporary variable to hold the frame repository provides the same functionality and speeds up the process
frameRepository = odb.steps['Column-3'].frames;
frameS=[];
frameIVOL=[];
#Get only the last frame [-1]
frameS.insert(0,frameRepository[-1].fieldOutputs['S'].getSubset(position=INTEGRATION_POINT));
frameIVOL.insert(0,frameRepository[-1].fieldOutputs['IVOL'].getSubset(position=INTEGRATION_POINT));
#Total Volume
Tot_Vol=0;
#Stress Sum
Tot_Stress=0;
#
for II in range(0,len(frameS[-1].values)):
     Tot_Vol=Tot_Vol+frameIVOL[0].values[II].data;
     Tot_Stress=Tot_Stress+frameS[0].values[II].data * frameIVOL[0].values[II].data;

#Calculate Average
Avg_Stress = Tot_Stress/Tot_Vol;
#print 'Abaqus/Standard Stress Tensor Order:'
#From Abaqus Analysis User's Manual - 1.2.2 Conventions - Convention used for stress and strain components 
#print 'Average stresses in Global CSYS: 11-22-33-12-13-23';
#print Avg_Stress;
C13 = Avg_Stress[2]#z-component,1-direction
C23 = Avg_Stress[0]#x-component,2-direction
C33 = Avg_Stress[1]#y-component,3-direction in Fig. 6.5

EL=C11-2*C12*C21/(C22+C23)              # Longitudinal E1 modulus
nuL=C12/(C22+C23)                       # 12 Poisson coefficient
ET=(C11*(C22+C23)-2*C12*C12)*(C22-C23)/(C11*C22-C12*C21)
                                        # Transversal E2 modulus
nuT=(C11*C23-C12*C21)/(C11*C22-C12*C21) # 23 Poisson coefficient
GT=(C22-C23)/2 # or GT=ET/2/(1+nuT)     # 23 Shear stiffness

print "If Moduli are entered in TPa and dimensions in microns, results are in TPa"
print "E1=",EL,"TPa"
print "E2=",ET,"TPa"
print "PR12=",nuL
print "PR23=",nuT
print "G23=",GT,"TPa"


