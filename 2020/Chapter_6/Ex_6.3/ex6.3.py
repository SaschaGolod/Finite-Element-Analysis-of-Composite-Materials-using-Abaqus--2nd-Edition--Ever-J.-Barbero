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
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=200.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-5.27, -9.138), 
    point2=(5.27, 9.138))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=2.635, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=1.06, name='__profile__', 
    sheetSize=42.52, transform=
    mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((-1.756667, 
    -3.046, 2.635), ), sketchPlaneSide=SIDE1, 
    sketchUpEdge=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 
    4.569, 2.635), ), sketchOrientation=RIGHT, origin=(0.0, 0.0, 2.635)))
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, 3.5))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    5.27, 9.138), point1=(8.77, 9.138))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    -5.27, 9.138), point1=(-8.77, 9.138))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    -5.27, -9.138), point1=(-8.77, -9.138))
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    5.27, -9.138), point1=(8.77, -9.138))
mdb.models['Model-1'].parts['Part-1'].PartitionCellBySketch(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((5.27, 3.046, 
    1.756667), ), ), sketch=mdb.models['Model-1'].sketches['__profile__'], 
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((-1.756667, 
    -3.046, 2.635), ), sketchUpEdge=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 4.569, 2.635), ))
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((1.756667, -3.046, 
    0.0), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    -3.930608, -5.904422, 2.635), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((-5.27, -8.263, 2.635), 
    ), mdb.models['Model-1'].parts['Part-1'].edges.findAt((-2.645, -9.138, 
    2.635), )), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 
    -9.138, 0.65875), ), sense=REVERSE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((0.536913, -8.836044, 
    0.0), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    2.036422, -7.798608, 2.635), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((4.395, -9.138, 2.635), 
    ), mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, -6.513, 
    2.635), )), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 
    -9.138, 0.65875), ), sense=REVERSE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((4.968044, -0.75242, 
    0.0), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    3.930608, 5.904422, 2.635), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 8.263, 2.635), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((2.645, 9.138, 2.635), 
    )), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt((5.27, 9.138, 
    0.65875), ), sense=REVERSE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((-0.536913, 8.836044, 
    0.0), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((
    -5.27, 6.513, 2.635), ), 
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((-2.036422, 7.798608, 
    2.635), ), mdb.models['Model-1'].parts['Part-1'].edges.findAt((-4.395, 
    9.138, 2.635), )), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt(
    (-5.27, 9.138, 0.65875), ), sense=REVERSE)
mdb.models['Model-1'].parts['Part-1'].PartitionCellByExtrudeEdge(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((-4.968044, -1.919087, 
    0.0), ), ), edges=(mdb.models['Model-1'].parts['Part-1'].edges.findAt((3.5, 
    0.0, 2.635), ), ), line=mdb.models['Model-1'].parts['Part-1'].edges.findAt(
    (5.27, 9.138, 0.65875), ), sense=REVERSE)
mdb.models['Model-1'].Material(name='Fiber')
mdb.models['Model-1'].materials['Fiber'].Elastic(table=((241000.0, 0.2), ))
mdb.models['Model-1'].Material(name='Matrix')
mdb.models['Model-1'].materials['Matrix'].Elastic(table=((3120.0, 0.38), ))
mdb.models['Model-1'].HomogeneousSolidSection(material='Fiber', name='Fiber', 
    thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='Matrix', name='Matrix', 
    thickness=None)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((0.0, 3.396337, 0.0), 
    ), ((-4.968044, 6.84442, 2.635), ), ((2.97642, 8.836044, 2.635), ), ((
    2.97642, -8.836044, 0.0), ), ((-4.968044, -6.84442, 0.0), ), ), name=
    'Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName='Fiber', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].Set(cells=
    mdb.models['Model-1'].parts['Part-1'].cells.findAt(((-3.754823, 3.032969, 
    0.0), ), ), name='Set-2')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-2'], sectionName='Matrix', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-Gamma13', 
    previous='Initial')
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'E', 'U', 'IVOL'))
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.59, -9.138, 1.756667), ), ((-2.936667, -9.138, 1.756667), ), ((2.936667, 
    -9.138, 0.878333), ), ), name='Set-1')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName=
    'Step-Gamma13', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='ysupp', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-1'], u1=UNSET, u2=0.0, u3=0.0, 
    ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    -0.59, 9.138, 1.756667), ), ((2.936667, 9.138, 1.756667), ), ((-2.936667, 
    9.138, 0.878333), ), ), name='Set-2')
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName=
    'Step-Gamma13', distributionType=UNIFORM, fieldName='', fixed=OFF, 
    localCsys=None, name='ydisp', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-2'], u1=UNSET, u2=UNSET, u3=
    18.276, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].rootAssembly.Set(faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    -5.27, 6.804667, 1.756667), ), ((5.27, 1.879333, 1.756667), ), ((5.27, 
    -6.804667, 1.756667), ), ((-5.27, 1.879333, 0.878333), ), ((-5.27, 
    -6.804667, 0.878333), ), ((5.27, 6.804667, 0.878333), ), ), name='Set-3')
mdb.models['Model-1'].XsymmBC(createStepName='Step-Gamma13', localCsys=None, 
    name='xsymm', region=mdb.models['Model-1'].rootAssembly.sets['Set-3'])
mdb.models['Model-1'].rootAssembly.Surface(name='m_Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    3.754823, 3.032969, 2.635), ), ((4.968044, -6.84442, 2.635), ), ((-2.97642, 
    -8.836044, 2.635), ), ((-4.968044, 6.84442, 2.635), ), ((2.97642, 8.836044, 
    2.635), ), ((0.0, 3.396337, 2.635), ), ))
mdb.models['Model-1'].rootAssembly.Surface(name='s_Surf-1', side1Faces=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    0.0, 3.396337, 0.0), ), ((-3.754823, 3.032969, 0.0), ), ((-2.97642, 
    8.836044, 0.0), ), ((4.968044, 6.84442, 0.0), ), ((2.97642, -8.836044, 
    0.0), ), ((-4.968044, -6.84442, 0.0), ), ))
mdb.models['Model-1'].Tie(adjust=OFF, master=
    mdb.models['Model-1'].rootAssembly.surfaces['m_Surf-1'], name=
    'Constraint-1', positionTolerance=2.635, positionToleranceMethod=SPECIFIED, 
    slave=mdb.models['Model-1'].rootAssembly.surfaces['s_Surf-1'], thickness=ON
    , tieRotations=OFF)
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    minSizeFactor=0.1, regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=0.5)
mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=C3D8R, elemLibrary=STANDARD, secondOrderAccuracy=OFF, 
    kinematicSplit=AVERAGE_STRAIN, hourglassControl=DEFAULT, 
    distortionControl=DEFAULT), ElemType(elemCode=C3D6, elemLibrary=STANDARD), 
    ElemType(elemCode=C3D4, elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].cells.findAt(((
    0.0, 3.396337, 0.0), ), ((-3.754823, 3.032969, 0.0), ), ((-4.968044, 
    6.84442, 2.635), ), ((2.97642, 8.836044, 2.635), ), ((2.97642, -8.836044, 
    0.0), ), ((-4.968044, -6.84442, 0.0), ), ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)
