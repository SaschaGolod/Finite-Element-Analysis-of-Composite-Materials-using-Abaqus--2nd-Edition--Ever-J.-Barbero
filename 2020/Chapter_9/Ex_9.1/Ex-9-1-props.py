# filename: Ex-9-1-props.py
# use with: abaqusddm-std.obj
## Do not use until the Model is complete and meshed. 
# Inserts material properties into the .inp file and defines the Job
from abaqusConstants import *
from mesh import *
from step import *
from regionToolset import Region
from multiprocessing import cpu_count
from visualization import openOdb
from abaqus import mdb
import csv                  # to write a .CSV file
from UgenKeyword import *   # to write UGENS parameters on the .inp file 
session.journalOptions.setValues(replayGeometry=COORDINATE, recoverGeometry=COORDINATE)
# Enter your model parameters here:
NL = 3                               # number of laminas (scalar)
ModelParameters = {}                 # define a dictionary data tye
ModelParameters['GIc']    = '0.254'
ModelParameters['GIIc']   = '1e16'
ModelParameters['dummy']  = '0'      # for future use
ModelParameters['E1']     = '44700'   
ModelParameters['E2']     = '12700'
ModelParameters['G12']    =  '5800'
ModelParameters['Nu12']   = '.297'
ModelParameters['Nu23']   = '.41'
ModelParameters['Cte1']   = '3.7'
ModelParameters['Cte2']   = '30.'
ModelParameters['tk']     = '.144'
ModelParameters['Lss']    = [(1,0), (8,90), (.5,0)]#[list] of (thickness,angle) pairs
ModelParameters['Strain'] = '1.8735'  # percentage max. strain to run the model 
# do not make any changes below
# define GetKeywordPosition after 'mdb.model' is defined
import string # needed by GetKeywordPosition
def GetKeywordPosition(modelName, blockPrefix, occurrence=1):
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
    return -1 # next line must remain empty

Model = mdb.models['Model-1'] # shortcut name for mdb.models['Model-1']
# Abaqus does not allow UGENS with multiple Cpus. Use numCpus = 1
Job = mdb.Job(name='Job-ddm-exe', 
              model='Model-1',
              nodalOutputPrecision=FULL,
              numCpus=1,
              numDomains=cpu_count(),
              userSubroutine='abaqusddm-std.obj'
              )# job "from model" before adding keyword blocks

Model.keywordBlock.synchVersions(storeNodesAndElements=False)
# set "position" so that *Transverse Shear Stiffness is placed before *End Part 
position = GetKeywordPosition( 'Model-1', '*End Part')-1
Model.keywordBlock.insert(position, UgenKeyword(ModelParameters))
# set "position" so that *Initial Conditions is placed before *Step 
position = GetKeywordPosition( 'Model-1', '*Step')-1
Model.keywordBlock.insert(position, """*Initial Conditions, type=SOLUTION, USER""")
mdb.jobs['Job-ddm-exe'].writeInput(consistencyChecking=OFF)# contains keyword blocks
# set up a new Job "from input file". Note file name "Job-ddm-exe-1" used. 
mdb.JobFromInputFile(activateLoadBalancing=False, atTime=None, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, inputFileName=
    'C:\\SIMULIA\\User\\Job-ddm-exe.inp', memory=90, memoryUnits=PERCENTAGE, 
    multiprocessingMode=DEFAULT, name='Job-ddm-exe-1', nodalOutputPrecision=SINGLE
    , numCpus=1, numDomains=1, parallelizationMethodExplicit=DOMAIN, queue=None
    , scratch='', type=ANALYSIS, userSubroutine=
    'C:\\SIMULIA\\User\\abaqusddm-std.obj', waitHours=0, waitMinutes=0)

# Uncomment or submit Job from CAE
# mdb.jobs['Job-ddm-exe-1'].submit(consistencyChecking=OFF)
# Job.waitForCompletion()
# postprocessing can be added here
# end
