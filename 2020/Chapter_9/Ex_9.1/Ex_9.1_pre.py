# Exercise 9.1 "Finite Element Analysis of Composite Materials : with Abaqus" 
# using abaqusddm-std.obj (original DDM)
# load the Python Modules
from abaqusConstants import *
from mesh import *
from step import *
from regionToolset import Region
from multiprocessing import cpu_count
from visualization import openOdb
from abaqus import mdb
import csv                  # utilities to write a .CSV file
from UgenKeyword import *   # utilities to write the UGENS parameters on the Job.inp file directly from CAE
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)

# Enter your model parameters here 
NL = 3                                  # number of laminas (scalar)
ModelParameters = {}                    # define a dictionary data tye
ModelParameters['E1']       = '44700'   # add to the dictionary
ModelParameters['E2']       = '12700'
ModelParameters['G12']      =  '5800'
ModelParameters['Nu12']     = '.297'
ModelParameters['Nu23']     = '.41'
ModelParameters['Cte1']     = '3.7'
ModelParameters['Cte2']     = '30.'
ModelParameters['GIIc']     = '1e16'
ModelParameters['GIc']      = '0.254'
ModelParameters['tk']       = '.144'
ModelParameters['dummy']   = '0'
ModelParameters['Lss']      = [(1,0), (8,90), (.5,0)] # a [list] of tuples (thickness angle)
ModelParameters['Strain'] = '1.8735'    # max. strain to run the model in %
ShellDimensionX = 10.                   # model dimensions
ShellDimensionY = 10.                   # model dimensions

# Generate the Abaqus model
# Ignore Warning: 
# The following parts have some elements without any section assigned: Laminate
mdb.close()
Model = mdb.models['Model-1']
# import/define GetKeywordPosition after 'mdb.model' is defined
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
    return -1 #next line empty

# shell dimensions
Sketch = Model.ConstrainedSketch(name='LaminateSketch', sheetSize=10.*ShellDimensionX)
Sketch.rectangle(point1 = (0.0, 0.0),
                 point2 = (ShellDimensionX, ShellDimensionX)
                 )

Part = Model.Part(dimensionality = THREE_D,
                  name           = 'Laminate',
                  type           = DEFORMABLE_BODY
                  )
                  
Part.BaseShell(sketch=Sketch)

Instance = Model.rootAssembly.Instance(dependent = ON,
                                       name='Laminate-1', 
                                       part=Part
                                       )

Part.Set(faces=Part.faces,
         name='WholeLaminate'
         )

# STEP
# minInc, reduce it as much as needed
# maxNumInc, set to a bigger number to allow for reduced minInc
Step = Model.StaticStep(timePeriod=float(ModelParameters['Strain']),
                        initialInc=0.01,
                        minInc=0.0001,
                        maxInc=0.01,
                        maxNumInc=1000,
                        name='ApplyStrain',
                        previous='Initial'
                        )
                        
Model.fieldOutputRequests['F-Output-1'].setValues(variables=('U', 'RF', 'SDV'))
                        
Model.XsymmBC(createStepName='Initial',
              name='SymmetryX', 
              region=Region(edges=Instance.edges.findAt(((0.0, ShellDimensionY/2., 0.0), ), ))
              )

Model.YsymmBC(createStepName='Initial',
              name='SymmetryY', 
              region=Region(edges=Instance.edges.findAt(((ShellDimensionX/2., 0.0, 0.0), ), ))
              )

Model.EncastreBC(createStepName='Initial',
                 name='NoRigidBodyMotion',
                 region=Region(vertices=Instance.vertices.findAt(((0.0, 0.0, 0.0), ), ))
                 )
                 
Model.DisplacementBC(createStepName='ApplyStrain',
                     name='Strain',
                     region=Region(edges=Instance.edges.findAt(((ShellDimensionX, ShellDimensionY/2., 0.0), ), )),
                     u1=ShellDimensionX*float(ModelParameters['Strain'])/100.
                     )

# membrane only
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-4', 
    region=Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Laminate-1'].faces.findAt(
    ((ShellDimensionX/2., ShellDimensionY/2., 0.0), (0.0, 0.0, 0.0)), )), u1=UNSET, u2=UNSET, u3=
    SET, ur1=SET, ur2=SET, ur3=SET)

# CONTROLS
# Abaqus default R_n^alpha=0.005 (first value in the list); changed to 0.02 
# R_n^alpha: convergence criterion for ratio of largest residual to corresponding average flux norm
mdb.models['Model-1'].steps['ApplyStrain'].control.setValues(
    allowPropagation=OFF, resetDefaultValues=OFF, displacementField=(0.02, 
    0.01, 0.0, 0.0, 0.02, 1e-05, 0.001, 1e-08, 1.0, 1e-05, 1e-08), 
    electricalPotentialField=(0.005, 0.01, 0.0, 0.0, 0.02, 1e-05, 0.001, 1e-08, 
    1.0, 1e-05), hydrostaticFluidPressureField=(0.005, 0.01, 0.0, 0.0, 0.02, 
    1e-05, 0.001, 1e-08, 1.0, 1e-05), rotationField=(0.005, 0.01, 0.0, 0.0, 
    0.02, 1e-05, 0.001, 1e-08, 1.0, 1e-05))

Part.setElementType(elemTypes=(ElemType(elemCode=S4R), ), 
                    regions=Region(faces = Part.faces)
                    )

Part.seedPart(size=ShellDimensionX) # only one element

Part.generateMesh()

# Abaqus does not allow UGENS with multiple Cpus
# Do not use numCpus=cpu_count(). Use numCpus=1
Job = mdb.Job(name='Job-ddm-exe', 
              model='Model-1',
              nodalOutputPrecision=FULL,
              numCpus=1,
              numDomains=cpu_count(),
              userSubroutine='abaqusddm-std.obj'
              )# temporary job before adding keyword blocks

Model.keywordBlock.synchVersions(storeNodesAndElements=False)
# set "position" so that *Transverse Shear Stiffness is placed before *End Part in the .inp file
position = GetKeywordPosition( 'Model-1', '*End Part')-1
Model.keywordBlock.insert(position, UgenKeyword(ModelParameters))
# set "position" so that *Initial Conditions is placed before *Step in the .inp file
position = GetKeywordPosition( 'Model-1', '*Step')-1
Model.keywordBlock.insert(position, """*Initial Conditions, type=SOLUTION, USER""")
mdb.jobs['Job-ddm-exe'].writeInput(consistencyChecking=OFF)# contains keywordblocks
# set up a new Job "from input file" 
mdb.JobFromInputFile(activateLoadBalancing=False, atTime=None, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, inputFileName=
    'C:\\SIMULIA\\User\\Job-ddm-exe.inp', memory=90, memoryUnits=PERCENTAGE, 
    multiprocessingMode=DEFAULT, name='Job-ddm-exe-1', nodalOutputPrecision=SINGLE
    , numCpus=1, numDomains=1, parallelizationMethodExplicit=DOMAIN, queue=None
    , scratch='', type=ANALYSIS, userSubroutine=
    'C:\\SIMULIA\\User\\abaqusddm-std.obj', waitHours=0, waitMinutes=0)

# execution starts here
mdb.jobs['Job-ddm-exe-1'].submit(consistencyChecking=OFF)
Job.waitForCompletion()
# Post processing available in Ex_9.1_post.py
