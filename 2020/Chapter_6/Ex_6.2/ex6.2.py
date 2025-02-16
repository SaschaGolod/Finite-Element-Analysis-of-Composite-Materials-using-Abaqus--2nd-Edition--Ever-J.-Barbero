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
## recoverGeometry for easy parameterization
session.journalOptions.setValues(recoverGeometry=COORDINATE)
## session colors
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF)
session.graphicsOptions.setValues(backgroundStyle=SOLID, 
    backgroundColor='#FFFFFF', translucencyMode=2)
## careful with indentation
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(5.27, 9.138))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=1.3175, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=0.53, name='__profile__', 
    sheetSize=21.26, transform=
    mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((1.756667, 
    3.046, 1.3175), ), sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 
    6.8535, 1.3175), ), sketchOrientation=RIGHT, origin=(0.0, 0.0, 1.3175)))
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 3.5))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    5.27, 9.138), point1=(8.77, 9.138))
mdb.models['Model-1'].parts['Part-1'].PartitionCellBySketch(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((5.27, 6.092, 
    0.878333), ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], 
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((1.756667, 
    3.046, 1.3175), ), sketchUpEdge=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 6.8535, 1.3175), 
    ))
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((2.959084, 8.910394, 
    1.3175), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    1.339392, 3.233578, 1.3175), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((0.0, 0.875, 1.3175), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((2.625, 0.0, 1.3175), ))
    , line=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 0.0, 
    0.329375), ), sense=REVERSE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((2.959084, 8.910394, 
    1.3175), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    3.930608, 5.904422, 1.3175), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 8.263, 1.3175), 
    ), mdb.models['Model-1'].parts['Part-1'].edges.findAt((2.645, 9.138, 
    1.3175), )), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 
    9.138, 0.329375), ), sense=REVERSE)
mdb.models['Model-1'].Material(name='Fiber')
mdb.models['Model-1'].materials['Fiber'].Elastic(table=((241000.0, 0.2), ))
mdb.models['Model-1'].Material(name='Matrix')
mdb.models['Model-1'].materials['Matrix'].Elastic(table=((3120.0, 0.38), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Fiber', name='Fiber', 
    thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='Matrix', name='Matrix', 
    thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((3.978776, 0.674069, 
    1.3175), ), ), name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName='Matrix', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((2.310916, 0.227605, 
    1.3175), ), ((2.959084, 8.910394, 1.3175), ), ), name='Set-2')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-2'], sectionName='Fiber', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].StaticLinearPerturbationStep(name='Column-1', previous=
    'Initial')
mdb.models['Model-1'].StaticLinearPerturbationStep(name='Column-2', previous=
    'Column-1')
mdb.models['Model-1'].StaticLinearPerturbationStep(name='Column-3', previous=
    'Column-2')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'E', 'U', 'IVOL'))
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.27, 3.758667, 0.878333), ), ((0.0, 5.379333, 0.878333), ), ((0.0, 
    2.333333, 0.439167), ), ((5.27, 6.804667, 0.439167), ), ), name='Set-1')
mdb.models['Model-1'].XsymmBC(createStepName='Column-1', localCsys=None, name=
    'xsymm-C1', region=mdb.models['Model-1'].rootAssembly.sets['Set-1'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    2.936667, 9.138, 0.878333), ), ((2.333333, 0.0, 0.878333), ), ((1.18, 
    9.138, 0.439167), ), ((4.09, 0.0, 0.439167), ), ), name='Set-2')
mdb.models['Model-1'].YsymmBC(createStepName='Column-1', localCsys=None, name=
    'ysymm-C1', region=mdb.models['Model-1'].rootAssembly.sets['Set-2'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.042395, 6.827084, 0.0), ), ((0.227605, 2.310916, 0.0), ), ((1.202417, 
    8.910394, 0.0), ), ), name='Set-3')
mdb.models['Model-1'].ZsymmBC(createStepName='Column-1', localCsys=None, name=
    'zsymm-c1', region=mdb.models['Model-1'].rootAssembly.sets['Set-3'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    2.959084, 8.910394, 1.3175), ), ((2.310916, 0.227605, 1.3175), ), ((
    3.978776, 0.674069, 1.3175), ), ), name='Set-4')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Column-1'
    , distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'disp-C1', region=mdb.models['Model-1'].rootAssembly.sets['Set-4'], u1=
    UNSET, u2=UNSET, u3=1.3175, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.042395, 6.827084, 0.0), ), ((0.227605, 2.310916, 0.0), ), ((2.959084, 
    8.910394, 1.3175), ), ((2.310916, 0.227605, 1.3175), ), ((3.978776, 
    0.674069, 1.3175), ), ((1.202417, 8.910394, 0.0), ), ), name='Set-5')
mdb.models['Model-1'].ZsymmBC(createStepName='Column-2', localCsys=None, name=
    'zsymm-C2', region=mdb.models['Model-1'].rootAssembly.sets['Set-5'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    2.936667, 9.138, 0.878333), ), ((2.333333, 0.0, 0.878333), ), ((1.18, 
    9.138, 0.439167), ), ((4.09, 0.0, 0.439167), ), ), name='Set-6')
mdb.models['Model-1'].YsymmBC(createStepName='Column-2', localCsys=None, name=
    'ysymm-C2', region=mdb.models['Model-1'].rootAssembly.sets['Set-6'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.0, 5.379333, 0.878333), ), ((0.0, 2.333333, 0.439167), ), ), name=
    'Set-7')
mdb.models['Model-1'].XsymmBC(createStepName='Column-2', localCsys=None, name=
    'xsymm-C2', region=mdb.models['Model-1'].rootAssembly.sets['Set-7'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.27, 3.758667, 0.878333), ), ((5.27, 6.804667, 0.439167), ), ), name=
    'Set-8')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Column-2'
    , distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'disp-C2', region=mdb.models['Model-1'].rootAssembly.sets['Set-8'], u1=5.27
    , u2=UNSET, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.27, 3.758667, 0.878333), ), ((0.0, 5.379333, 0.878333), ), ((0.0, 
    2.333333, 0.439167), ), ((5.27, 6.804667, 0.439167), ), ), name='Set-9')
mdb.models['Model-1'].XsymmBC(createStepName='Column-3', localCsys=None, name=
    'xsymm-C3', region=mdb.models['Model-1'].rootAssembly.sets['Set-9'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    5.042395, 6.827084, 0.0), ), ((0.227605, 2.310916, 0.0), ), ((2.959084, 
    8.910394, 1.3175), ), ((2.310916, 0.227605, 1.3175), ), ((3.978776, 
    0.674069, 1.3175), ), ((1.202417, 8.910394, 0.0), ), ), name='Set-10')
mdb.models['Model-1'].ZsymmBC(createStepName='Column-3', localCsys=None, name=
    'zsymm-C3', region=mdb.models['Model-1'].rootAssembly.sets['Set-10'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    2.333333, 0.0, 0.878333), ), ((4.09, 0.0, 0.439167), ), ), name='Set-11')
mdb.models['Model-1'].YsymmBC(createStepName='Column-3', localCsys=None, name=
    'ysymm-C3', region=mdb.models['Model-1'].rootAssembly.sets['Set-11'])
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    2.936667, 9.138, 0.878333), ), ((1.18, 9.138, 0.439167), ), ), name=
    'Set-12')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Column-3'
    , distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'disp-C3', region=mdb.models['Model-1'].rootAssembly.sets['Set-12'], u1=
    UNSET, u2=9.138, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=0.5)
mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].cells.findAt(((
    3.978776, 0.674069, 1.3175), ), ((2.310916, 0.227605, 1.3175), ), ((
    2.959084, 8.910394, 1.3175), ), ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
