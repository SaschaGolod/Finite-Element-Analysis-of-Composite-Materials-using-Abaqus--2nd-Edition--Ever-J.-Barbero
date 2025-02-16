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
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=262.850799560547, 
    height=285.0)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
import os
os.chdir(r"C:\SIMULIA\User\Ex_10.2")
openMdb(pathName='C:/SIMULIA/User/Ex_10.1/ex10.1.cae')
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['coh-els'].parts['adhesive']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.models.changeKey(fromName='coh-els', toName='coh-surf')
p = mdb.models['coh-surf'].parts['adhesive']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.saveAs(pathName='C:/SIMULIA/User/Ex_10.2/ex10.2.cae')
a = mdb.models['coh-surf'].rootAssembly
session.viewports['Viewport: 1'].setValues(displayedObject=a)
session.viewports['Viewport: 1'].assemblyDisplay.setValues(
    optimizationTasks=OFF, geometricRestrictions=OFF, stopConditions=OFF)
del mdb.models['coh-surf'].rootAssembly.surfaces['coh-top']
del mdb.models['coh-surf'].rootAssembly.surfaces['coh-bot']
del mdb.models['coh-surf'].constraints['bot']
del mdb.models['coh-surf'].constraints['top']
del mdb.models['coh-surf'].rootAssembly.features['adhesive-1']
mdb.models['coh-surf'].rootAssembly.regenerate()
mdb.models['coh-surf'].parts['beam'].deleteMesh()
mdb.models['coh-surf'].parts['beam'].PartitionEdgeByParam(edges=
    mdb.models['coh-surf'].parts['beam'].edges.findAt(((0.075, 0.0, 0.0), ), ), 
    parameter=0.7)
mdb.models['coh-surf'].parts['beam'].generateMesh()
mdb.models['coh-surf'].rootAssembly.regenerate()
mdb.models['coh-surf'].rootAssembly.Surface(name='top', side1Edges=
    mdb.models['coh-surf'].rootAssembly.instances['beam-1'].edges.findAt(((
    0.0825, 0.0, 0.0), ), ((0.0225, 0.0, 0.0), ), ))
mdb.models['coh-surf'].rootAssembly.Set(edges=
    mdb.models['coh-surf'].rootAssembly.instances['beam-1'].edges.findAt(((
    0.0825, 0.0, 0.0), ), ), name='bond')
mdb.models['coh-surf'].ContactProperty('coh')
mdb.models['coh-surf'].interactionProperties['coh'].TangentialBehavior(
    formulation=FRICTIONLESS)
mdb.models['coh-surf'].interactionProperties['coh'].NormalBehavior(
    allowSeparation=ON, constraintEnforcementMethod=DEFAULT, 
    pressureOverclosure=HARD)
mdb.models['coh-surf'].interactionProperties['coh'].CohesiveBehavior(
    defaultPenalties=OFF, eligibility=SPECIFIED, table=((570000000000000.0, 
    570000000000000.0, 570000000000000.0), ))
mdb.models['coh-surf'].interactionProperties['coh'].GeometricProperties(
    contactArea=0.02, padThickness=None)
mdb.models['coh-surf'].interactionProperties['coh'].Damage(criterion=
    QUAD_TRACTION, evolTable=((280.0, 280.0, 280.0), ), evolutionType=ENERGY, 
    exponent=2.884, initTable=((57000000.0, 57000000.0, 57000000.0), ), 
    mixedModeType=BK, useEvolution=ON, useMixedMode=ON, useStabilization=ON, 
    viscosityCoef=1e-05)
mdb.models['coh-surf'].SurfaceToSurfaceContactStd(adjustMethod=NONE, 
    bondingSet=mdb.models['coh-surf'].rootAssembly.sets['bond'], 
    clearanceRegion=None, createStepName='Initial', datumAxis=None, 
    enforcement=NODE_TO_SURFACE, initialClearance=OMIT, interactionProperty=
    'coh', master=mdb.models['coh-surf'].rootAssembly.surfaces['bot'], name=
    'coh', slave=mdb.models['coh-surf'].rootAssembly.surfaces['top'], sliding=
    FINITE, smooth=0.2, surfaceSmoothing=NONE, thickness=OFF)
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='coh-surf', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Ex-10-2', nodalOutputPrecision=SINGLE, 
    numCpus=4, numDomains=4, numGPUs=0, queue=None, resultsFormat=ODB, scratch=
    '', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Ex-10-2'].submit(consistencyChecking=OFF)