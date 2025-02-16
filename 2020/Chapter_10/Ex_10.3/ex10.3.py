# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from optimization import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=178.9453125, 
    height=285.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import os
os.chdir(r"C:\SIMULIA\User\Ex_10.3")
openMdb(pathName='C:/SIMULIA/User/Ex_10.2/ex10.2.cae')
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['coh-surf'].parts['adhesive']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.models.changeKey(fromName='coh-surf', toName='vcct')
p = mdb.models['vcct'].parts['adhesive']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.saveAs(pathName='C:/SIMULIA/User/Ex_10.3/ex10.3.cae')
a = mdb.models['vcct'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(interactions=ON, 
    constraints=ON, connectors=ON, engineeringFeatures=ON, 
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
del mdb.models['vcct'].interactionProperties['coh'].cohesiveBehavior
del mdb.models['vcct'].interactionProperties['coh'].damage
mdb.models['vcct'].interactionProperties['coh'].tangentialBehavior.setValues(
    formulation=FRICTIONLESS)
mdb.models['vcct'].interactionProperties['coh'].geometricProperties.setValues(
    contactArea=0.02, padThickness=None)
mdb.models['vcct'].interactions['coh'].setValues(adjustMethod=NONE, bondingSet=
    mdb.models['vcct'].rootAssembly.sets['bond'], datumAxis=None, enforcement=
    NODE_TO_SURFACE, initialClearance=1e-07, sliding=SMALL, smooth=0.2, 
    supplementaryContact=SELECTIVE, thickness=ON)
mdb.models['vcct'].fieldOutputRequests['F-Output-1'].setValues(variables=('S', 
    'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 'ENRRT', 
    'BDSTAT', 'STATUS'))
mdb.models['vcct'].keywordBlock.synchVersions(storeNodesAndElements=False)
mdb.models['vcct'].keywordBlock.insert(41, 
    '\n*Initial Conditions, type=CONTACT\ntop,bot,bond')
mdb.models['vcct'].keywordBlock.insert(45, 
    '\n*Debond, slave=top, master=bot\n\n*Fracture criterion, type=VCCT, mixed mode behavior=BK, tolerance=0.1\n280.0,280.0,280.0,2.284')
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='vcct', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Ex-10-3', nodalOutputPrecision=SINGLE, 
    numCpus=4, numDomains=4, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
    '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Ex-10-3'].submit(consistencyChecking=OFF)