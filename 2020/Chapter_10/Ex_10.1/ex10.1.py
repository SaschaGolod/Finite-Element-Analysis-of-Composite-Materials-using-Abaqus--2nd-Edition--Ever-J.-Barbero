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
os.chdir(r"C:\SIMULIA\User\Ex_10.1")
execfile('C:/SIMULIA/User/Ex_10.1/ws_composites_dcb.py', __main__.__dict__)
session.viewports['Viewport: 1'].setValues(displayedObject=None)
p = mdb.models['vcct-xpl-shell'].parts['beam']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.saveAs(pathName='C:/SIMULIA/User/Ex_10.1/ex10.1.cae')
session.viewports['Viewport: 1'].partDisplay.setValues(sectionAssignments=ON, 
    engineeringFeatures=ON)
session.viewports['Viewport: 1'].partDisplay.geometryOptions.setValues(
    referenceRepresentation=OFF)
p = mdb.models['coh-els'].parts['adhesive']
session.viewports['Viewport: 1'].setValues(displayedObject=p)
mdb.models['coh-els'].Material(name='cohesive')
mdb.models['coh-els'].materials['cohesive'].Elastic(table=((570000000000000.0, 
    570000000000000.0, 570000000000000.0), ), type=TRACTION)
mdb.models['coh-els'].materials['cohesive'].QuadsDamageInitiation(table=((
    57000000.0, 57000000.0, 57000000.0), ))
mdb.models['coh-els'].materials['cohesive'].quadsDamageInitiation.DamageEvolution(
    mixedModeBehavior=BK, power=2.284, table=((280.0, 280.0, 280.0), ), type=
    ENERGY)
mdb.models['coh-els'].CohesiveSection(material='cohesive', name='cohesive', 
    outOfPlaneThickness=0.02, response=TRACTION_SEPARATION)
mdb.models['coh-els'].parts['adhesive'].Set(faces=
    mdb.models['coh-els'].parts['adhesive'].faces.findAt(((0.023333, 0.000333, 
    0.0), (0.0, 0.0, 1.0)), ), name='Set-1')
mdb.models['coh-els'].parts['adhesive'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['coh-els'].parts['adhesive'].sets['Set-1'], sectionName=
    'cohesive', thicknessAssignment=FROM_SECTION)
mdb.models['coh-els'].rootAssembly.regenerate()
mdb.models['coh-els'].StaticStep(initialInc=0.01, maxNumInc=1000, minInc=1e-08, 
    name='Step-1', nlgeom=ON, previous='Initial')
mdb.models['coh-els'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'PE', 'PEEQ', 'PEMAG', 'LE', 'U', 'RF', 'CF', 'CSTRESS', 'CDISP', 
    'STATUS'))
mdb.models['coh-els'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['coh-els'].rootAssembly.sets['top'], sectionPoints=DEFAULT, 
    variables=('U2', 'RF2'))
mdb.models['coh-els'].parts['beam'].setMeshControls(elemShape=QUAD, regions=
    mdb.models['coh-els'].parts['beam'].faces.findAt(((0.033333, 0.0005, 0.0), 
    (0.0, 0.0, 1.0)), ), technique=STRUCTURED)
mdb.models['coh-els'].parts['beam'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4I, elemLibrary=STANDARD), ElemType(elemCode=CPE3, 
    elemLibrary=STANDARD)), regions=(
    mdb.models['coh-els'].parts['beam'].faces.findAt(((0.033333, 0.0005, 0.0), 
    (0.0, 0.0, 1.0)), ), ))
mdb.models['coh-els'].parts['beam'].seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['coh-els'].parts['beam'].edges.findAt(((0.025, 0.0015, 0.0), ), 
    ), number=400)
mdb.models['coh-els'].parts['beam'].seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['coh-els'].parts['beam'].edges.findAt(((0.0, 0.000375, 0.0), ), 
    ), number=2)
mdb.models['coh-els'].parts['beam'].generateMesh()
mdb.models['coh-els'].parts['adhesive'].setMeshControls(elemShape=QUAD, 
    regions=mdb.models['coh-els'].parts['adhesive'].faces.findAt(((0.023333, 
    0.000333, 0.0), (0.0, 0.0, 1.0)), ), technique=SWEEP)
mdb.models['coh-els'].parts['adhesive'].setSweepPath(edge=
    mdb.models['coh-els'].parts['adhesive'].edges.findAt((0.07, 0.00075, 0.0), 
    ), region=mdb.models['coh-els'].parts['adhesive'].faces.findAt((0.023333, 
    0.000333, 0.0), (0.0, 0.0, 1.0)), sense=REVERSE)
mdb.models['coh-els'].parts['adhesive'].setElementType(elemTypes=(ElemType(
    elemCode=COH2D4, elemLibrary=STANDARD, viscosity=1e-05), ElemType(
    elemCode=UNKNOWN_TRI, elemLibrary=STANDARD)), regions=(
    mdb.models['coh-els'].parts['adhesive'].faces.findAt(((0.023333, 0.000333, 
    0.0), (0.0, 0.0, 1.0)), ), ))
mdb.models['coh-els'].parts['adhesive'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['coh-els'].parts['adhesive'].edges.findAt(((0.0175, 0.001, 
    0.0), ), ), number=280)
mdb.models['coh-els'].parts['adhesive'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['coh-els'].parts['adhesive'].edges.findAt(((0.0, 0.00025, 
    0.0), ), ), number=1)
mdb.models['coh-els'].parts['adhesive'].generateMesh()
mdb.models['coh-els'].rootAssembly.regenerate()
mdb.models['coh-els'].Tie(adjust=ON, master=
    mdb.models['coh-els'].rootAssembly.surfaces['top'], name='top', 
    positionTolerance=0.002, positionToleranceMethod=SPECIFIED, slave=
    mdb.models['coh-els'].rootAssembly.surfaces['coh-top'], thickness=ON, 
    tieRotations=ON)
mdb.models['coh-els'].Tie(adjust=ON, master=
    mdb.models['coh-els'].rootAssembly.surfaces['bot'], name='bot', 
    positionTolerance=0.002, positionToleranceMethod=SPECIFIED, slave=
    mdb.models['coh-els'].rootAssembly.surfaces['coh-bot'], thickness=ON, 
    tieRotations=ON)
mdb.models['coh-els'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'top', region=mdb.models['coh-els'].rootAssembly.sets['top'], u1=0.0, u2=
    0.006, ur3=UNSET)
mdb.models['coh-els'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'bot', region=mdb.models['coh-els'].rootAssembly.sets['bot'], u1=0.0, u2=
    -0.006, ur3=UNSET)
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='coh-els', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Ex-10-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Ex-10-1'].setValues(numCpus=4, numDomains=4)
mdb.jobs['Ex-10-1'].submit(consistencyChecking=OFF)
