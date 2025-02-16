# Example-11-1-no-hole-TM #updated 10/18/2023
# "Finite Element Analysis of Composite Materials Using Abaqus, next edition" 
# DDM6TM includes temp-dependent properties, fatigue f(N), & mech. strain
# Fatigue and mech. strain not used in this example
# Plate subjected to DT = Tmin - SFT
# Using ddm6tm2017.obj
# ModelParameters['Temp']   = '-156'  # lowest temperature Tmin
# ModelParameters['SFT']    = ' 177'  # stress free temperature SFT 
# Monotonic cooling : N = 1
# ModelParameters['Cycles']   = '1'   # number of cycles N, if N==1 : monotonic cooling, DT=Tmin-SFT
# ModelParameters['BetaGIc']  = '0.0' # [1/m], zero if Cycles=1
# ModelParameters['BetaGIIc'] = '0.0' # [1/m], zero if Cycles=1
# Fatigue : N > 1
# ModelParameters['Cycles'] = 'N'   # number of cycles, N > 1
# ModelParameters['BetaGIc']  = '-0.204' # [1/m], mode I fracture
# ModelParameters['BetaGIIc'] = '-0.204' # [1/m], mode II fracture

# Load the Python Modules
from abaqusConstants import *
from mesh import *
from step import *
from regionToolset import Region
from multiprocessing import cpu_count
from visualization import openOdb
from abaqus import mdb
import csv                  # utilities to write a .CSV file
import os
# Set up the WorkDirectory
# os.chdir(r"C:\SIMULIA\User\DDM6TM2017")
from UgenKeywordTM_UGENS import * # utilities to write UGENS parameters on Job.inp file
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

# Enter your model parameters here 
ModelParameters = {}                        # define a dictionary data type
# Elastic properties
# Quadratic temp-dependent properties: P = a + bT + cT^2
ModelParameters['E1a']       = '271270.586' # [MPa]
ModelParameters['E1b']       = '-8.10997'
ModelParameters['E1c']       = '1.18938E-02'
ModelParameters['E2a']       = '6554.2638'       
ModelParameters['E2b']       = '-11.6689'
ModelParameters['E2c']       = '4.9329E-04'
ModelParameters['G12a']      =  '3998.0213'
ModelParameters['G12b']      =  '-8.84364'
ModelParameters['G12c']      =  '6.1187E-03'
ModelParameters['Nu12a']     =  '0.3147'
ModelParameters['Nu12b']     =  '-6.9707E-05'
ModelParameters['Nu12c']     =  '-4.0521E-07'
ModelParameters['Nu23a']     =  '0.5557'
ModelParameters['Nu23b']     =  '-1.0089E-04'
ModelParameters['Nu23c']     =  '-1.1402E-06'
# Thermal properties
# Cubic temp-dependent properties: P = a + bT + cT^2 + dT^3
ModelParameters['CTE1a']     = '-0.9766711'   # [microstrain]
ModelParameters['CTE1b']     = '-9.0549E-05'     
ModelParameters['CTE1c']     = '-7.6732E-06'     
ModelParameters['CTE1d']     = '2.3038E-08' 
ModelParameters['CTE2a']     = '38.4684'     
ModelParameters['CTE2b']     = '8.9456E-02'     
ModelParameters['CTE2c']     = '-3.6454E-04'     
ModelParameters['CTE2d']     = '0.0'      
# Fracture properties 
# Quadratic temp-dependent properties: P = A + BT + BT^2   
ModelParameters['GIcA']       = '0.18187' # [kJ/m^2]
ModelParameters['GIcB']       = '0.0'      
ModelParameters['GIcC']       = '0.0' 
ModelParameters['TGImax']     = '24'      # [Celsius]
ModelParameters['TGImin']     = '-184'    # [Celsius]
ModelParameters['GIIcA']      = '1'      
ModelParameters['GIIcB']      = '0.0'      
ModelParameters['GIIcC']      = '0.0' 
ModelParameters['TGIImax']    = '24'      # [Celsius]
ModelParameters['TGIImin']    = '-184'    # [Celsius]
# Temperature range for elastic (e) and thermal (t) properties
ModelParameters['SFT']        = '177'     # Stress free temperature
ModelParameters['Temax']      = '120'     # Upper limit(e) [Celsius]
ModelParameters['Temin']      = '-156'    # Lower limit(e) [Celsius]
ModelParameters['Ttmax']      = '120'     # Upper limit(t) [Celsius]
ModelParameters['Ttmin']      = '-156'    # Lower limit(t) [Celsius]
# Fiber failure properties 
ModelParameters['F1t']        = '1900.87' # [MPa]
ModelParameters['F1c']        = '441.2'
ModelParameters['F2c']        = '57.23'
ModelParameters['mWeibull']   = '8.9'     # []
# Thermal Fatigue properties
# BetaGIc & BetaGIIc only needed for thermal fatigue, define f(N) mode I and II
# If they are not used: BetaGIc & BetaGIIc = 0
# If monotonic cooling is simulated, then Cycles = 1, no fatigue. 
# Otherwise, enter the number of cycles
# If Cycles != 0, then BetaGIc & BetaGIIc can not be = 0
ModelParameters['Cycles']   = '1'   # number of cycles
ModelParameters['BetaGIc']  = '0.0' # [1/m]
ModelParameters['BetaGIIc'] = '0.0' # [1/m]
# LSS 1/2 symm. laminate starting at k=1 bottom surface
ModelParameters['Lss']      = [(0,1), (90,1), (0,1), (90,1)] # a [list] of tuples (angle,thickness) 
ModelParameters['tk']       = '0.127'   # Ply thickness
NL = len(ModelParameters['Lss'])
# Load
ModelParameters['Strain']   = '0'       # max. strain [NOT USED IN THIS SCRIPT]
ModelParameters['Temp']     = '-156'    # lowest temperature Tmin
# Geometry
ShellDimensionX = 100.                  # model dimensions
ShellDimensionY = 100.                  # model dimensions
Arclength       =  30.
ModelParameters['IntegrationPoints']   = '3' # Simpson
#
# DDM6TM needs 45 material properties 
PROPERTIES = 45 + 2*NL  
# and state variables: (3 state variables + 3 damages + 3 stresses + 3 energies) per layer
VARIABLES = 12*NL
WholeLaminateThickness = 2.*sum([x[0] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])#updated 10/15/2023
IntegrationPoints = float(ModelParameters['IntegrationPoints'])
#
# Generate the Abaqus model    
mdb.close()
Model = mdb.models['Model-1']
# Function UgensKeyword, use it after 'mdb' name is defined
import string # first import string, which is needed by GetKeywordPosition
def GetKeywordPosition(modelName, blockPrefix, occurrence=1):
    # Usage: set "position" so that *Initial Conditions is placed before *Step on the .inp file
    # position = GetKeywordPosition( 'Model-1', '*Step')-1
    # Model.keywordBlock.insert(position, """*Initial Conditions, type=SOLUTION, USER""")
    if blockPrefix == '':
        return len(mdb.models[modelName].keywordBlock.sieBlocks)-1
    pos = 0
    foundCount = 0
    for block in mdb.models[modelName].keywordBlock.sieBlocks:
        if string.lower(block[0:len(blockPrefix)])==\
           string.lower(blockPrefix):
            foundCount = foundCount + 1
            if foundCount >= occurrence:
                return pos
        pos=pos+1
    return -1

# Part 
Sketch = Model.ConstrainedSketch(name='LaminateSketch', sheetSize=10.*ShellDimensionX)
Sketch.rectangle(point1 = (0.0, 0.0),
                 point2 = (ShellDimensionX, ShellDimensionX))

Part = Model.Part(dimensionality = THREE_D,
                  name           = 'Laminate',
                  type           = DEFORMABLE_BODY)
                  
Part.BaseShell(sketch=Sketch)

Instance = Model.rootAssembly.Instance(dependent = OFF,
                                       name='Laminate-1', 
                                       part=Part)

Part.Set(faces=Part.faces, name='WholeLaminate')
SetEdge=Model.rootAssembly.instances['Laminate-1'].edges

# Dummy Material used for later locating the KeywordBlock 
# Material properties
Material = mdb.models['Model-1'].Material(name='Material-1')

Model.HomogeneousShellSection(idealization=NO_IDEALIZATION, 
    integrationRule=SIMPSON, material='Material-1', name='Section-1', 
    numIntPts=3, poissonDefinition=DEFAULT, preIntegrate=OFF, temperature=
    GRADIENT, thickness=WholeLaminateThickness, thicknessField='', thicknessModulus=None, 
    thicknessType=UNIFORM, useDensity=OFF)
Section = mdb.models['Model-1'].sections['Section-1']
Section.TransverseShearShell(k11=1.0, k12=0.0, k22=1.0)

Part.SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    Part.sets['WholeLaminate'], sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)

# Assembly
Model.rootAssembly.DatumCsysByDefault(CARTESIAN)
Instance = Model.rootAssembly.Instance(dependent = OFF,
                                       name='Laminate-1', 
                                       part=Part)

SetEdge=Model.rootAssembly.instances['Laminate-1'].edges

# STEP
# minInc, reduce it as much as needed
# maxNumInc, set to a larger number to allow for reduced minInc
Step = Model.StaticStep(timePeriod=float(ModelParameters['SFT'])-float(ModelParameters['Temp']),
                        initialInc=1.,
                        minInc=0.0001,
                        maxInc=1.,
                        maxNumInc=1000,
                        name='ApplyThermalStrain',
                        previous='Initial')
                        
Model.fieldOutputRequests['F-Output-1'].setValues(variables=('U', 'RF', 'SDV'))
                        
# BC
# symm X=0
Model.XsymmBC(createStepName='Initial', name='SymmetryX', 
              region=Region(edges=Instance.edges.findAt(((0.0, ShellDimensionY/2., 0.0), ), )))
# symm Y=0
Model.YsymmBC(createStepName='Initial', name='SymmetryY', 
              region=Region(edges=Instance.edges.findAt(((ShellDimensionX/2., 0.0, 0.0), ), )))
# fix (0,0,0)
Model.EncastreBC(createStepName='Initial', name='NoRigidBodyMotion',
                 region=Region(vertices=Instance.vertices.findAt(((0.0, 0.0, 0.0), ), )))

# Membrane only
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='MembraneOnly', 
    region=Region(faces=mdb.models['Model-1'].rootAssembly.instances['Laminate-1'].faces.findAt(
    ((ShellDimensionX/2., ShellDimensionY/2., 0.0), (0.0, 0.0, 0.0)), )), u1=UNSET, u2=UNSET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)

# Predefined Field 
# apply initial temperature = SFT
Model.Temperature(createStepName='Initial', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(float(ModelParameters['SFT']), ), name='Predefined Field-1', region=
    Model.rootAssembly.instances['Laminate-1'].sets['WholeLaminate'])

# apply final temperature = Temp
Model.Temperature(createStepName='ApplyThermalStrain', 
    crossSectionDistribution=CONSTANT_THROUGH_THICKNESS, distributionType=
    UNIFORM, magnitudes=(float(ModelParameters['Temp']), ), name='Predefined Field-2', region=
    Model.rootAssembly.instances['Laminate-1'].sets['WholeLaminate'])

# Controls 
Model.steps['ApplyThermalStrain'].control.setValues(
    allowPropagation=OFF, resetDefaultValues=OFF, displacementField=(0.02, 
    0.01, 0.0, 0.0, 0.02, 1e-05, 0.001, 1e-08, 1.0, 1e-05, 1e-08), 
    electricalPotentialField=(0.005, 0.01, 0.0, 0.0, 0.02, 1e-05, 0.001, 1e-08, 
    1.0, 1e-05), hydrostaticFluidPressureField=(0.005, 0.01, 0.0, 0.0, 0.02, 
    1e-05, 0.001, 1e-08, 1.0, 1e-05), rotationField=(0.005, 0.01, 0.0, 0.0, 
    0.02, 1e-05, 0.001, 1e-08, 1.0, 1e-05)) 

# Mesh 
InstancePart = Model.rootAssembly
InstancePart.setElementType(elemTypes=(ElemType(elemCode=S4R), ), 
                    regions=Region(faces = Part.faces))
InstancePart.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    InstancePart.instances['Laminate-1'], ), size=ShellDimensionX/4)#/elements per side
InstancePart.generateMesh(regions=(
    InstancePart.instances['Laminate-1'], ))

# Abaqus does not allow UGENS with multiple Cpus
# Do not use numCpus=cpu_count(). Use numCpus=1
Job = mdb.Job(name='Job', 
              model='Model-1',
              nodalOutputPrecision=FULL,
              numCpus=1,
              numDomains=cpu_count(),
              userSubroutine='ddm6tm-2017-std.obj')
# DO NOT write .inp file incrementally, it will break! wait till the end to write it!
# mdb.jobs['Job'].writeInput(consistencyChecking=OFF)

Model.keywordBlock.synchVersions(storeNodesAndElements=False)

# Set position to replace *Shell Section by *Shell General Section
WholeLaminateThickness = 2.*sum([x[1] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])
position = GetKeywordPosition( 'Model-1', '*Shell Section')
Model.keywordBlock.replace(
    position, '*Shell General Section, elset=WholeLaminate, USER, PROPERTIES='
    +str(PROPERTIES)+', VARIABLES='+str(VARIABLES)+'\n'+str(WholeLaminateThickness)+', '
    +str(IntegrationPoints))

# Model.keywordBlock.insert(5, UgenKeyword(ModelParameters))
# Set "position" so that *properties are placed before *Transverse shear on the .inp file
position = GetKeywordPosition( 'Model-1', '*Transverse Shear')-1
Model.keywordBlock.insert(position, UgenKeywordTM_UGENS(ModelParameters))

# Remove *Material
position = GetKeywordPosition( 'Model-1', '*Material')
Model.keywordBlock.replace(position, '**')

# Model.keywordBlock.insert(30, """*Initial Conditions, type=SOLUTION, USER""")
# set "position" so that *Initial Conditions is placed before *Step on the .inp file
position = GetKeywordPosition( 'Model-1', '*Step')-1
Model.keywordBlock.insert(position, """*Initial Conditions, type=SOLUTION, USER""")

# Write the .inp file (only once!)
mdb.jobs['Job'].writeInput(consistencyChecking=OFF)
# execution starts here
Job.submit()
Job.waitForCompletion()

# Post-processing 
fo = open('Job.txt', 'wb')      # log file
ofile = open('Job.csv', 'wb')   # results file
Writer = csv.writer(ofile)
Header = ['Life']
for i in range(NL):
    Header.append('Crack density '+str(i+1))

Writer.writerow(Header)
Results = openOdb(path='Job.odb', readOnly=True)#avoid warning
# print len(Results.steps['ApplyThermalStrain'].frames) # 336, so [0,335], last frame is 335
frame  = Results.steps['ApplyThermalStrain'].frames[-1] # at Tmin
cd = [] # crack density
cd.append(ModelParameters['Cycles'])
for i in range(NL):
    cd.append(frame.fieldOutputs['SDV'+str(12*i+1)].values[0].dataDouble)#2017 use dataDouble

Writer.writerow(cd) # results file
fo.write(str(cd))   # log file
fo.close()
ofile.close()
Results.close()
# mdb.close()
