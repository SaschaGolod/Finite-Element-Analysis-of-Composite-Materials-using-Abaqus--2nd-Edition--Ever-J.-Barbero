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
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=500.0)
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-152.4, -146.05), 
    point2=(152.4, -146.05))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 
    -146.05), ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-152.4, 146.05), 
    point2=(152.4, 146.05))
mdb.models['Model-1'].sketches['__profile__'].HorizontalConstraint(
    addUndoState=False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 
    146.05), ))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, -146.05), 
    point2=(0.0, 146.05))
mdb.models['Model-1'].sketches['__profile__'].VerticalConstraint(addUndoState=
    False, entity=
    mdb.models['Model-1'].sketches['__profile__'].geometry.findAt((0.0, 0.0), 
    ))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseShellExtrude(depth=908.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].GeneralStiffnessSection(applyThermalStress=0, name=
    'flange', poissonDefinition=DEFAULT, referenceTemperature=None, 
    stiffnessMatrix=(335053.0, 47658.0, 146155.0, 0.0, 0.0, 49984.0, -29251.0, 
    -1154.0, 0.0, 4261183.0, -1154.0, -5262.0, 0.0, 686071.0, 2023742.0, 0.0, 
    0.0, -2274.0, 0.0, 0.0, 677544.0), useDensity=OFF)
mdb.models['Model-1'].sections['flange'].TransverseShearShell(k11=34216.0, k12=
    0.0, k22=31190.0)
mdb.models['Model-1'].GeneralStiffnessSection(applyThermalStress=0, name='web', 
    poissonDefinition=DEFAULT, referenceTemperature=None, stiffnessMatrix=(
    338016.0, 44127.0, 143646.0, 0.0, 0.0, 49997.0, -6088.0, -14698.0, 0.0, 
    4769538.0, -14698.0, -6088.0, 0.0, 650127.0, 2155470.0, 0.0, 0.0, 0.0, 0.0, 
    0.0, 739467.0), useDensity=OFF)
mdb.models['Model-1'].sections['web'].TransverseShearShell(k11=34654.0, k12=0.0
    , k22=31623.0)
mdb.models['Model-1'].parts['Part-1'].Set(faces=
    mdb.models['Model-1'].parts['Part-1'].faces.findAt(((50.799998, -146.05, 
    302.666667), (0.0, -1.0, 0.0)), ((-50.799998, -146.05, 605.333333), (0.0, 
    -1.0, 0.0)), ((50.799998, 146.05, 302.666667), (0.0, -1.0, 0.0)), ((
    -50.799998, 146.05, 605.333333), (0.0, -1.0, 0.0)), ), name='Set-1')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-1'], sectionName='flange', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].Set(faces=
    mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, 48.683334, 
    605.333333), (1.0, 0.0, 0.0)), ), name='Set-2')
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['Model-1'].parts['Part-1'].sets['Set-2'], sectionName='web', 
    thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].DatumCsysByTwoLines(CARTESIAN, line1=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((0.0, 146.05, 227.0), ), 
    line2=mdb.models['Model-1'].parts['Part-1'].edges.findAt((0.0, -73.025, 
    0.0), ), name='web-csys')
mdb.models['Model-1'].parts['Part-1'].DatumCsysByTwoLines(CARTESIAN, line1=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt((0.0, 146.05, 227.0), ), 
    line2=mdb.models['Model-1'].parts['Part-1'].edges.findAt((38.1, 146.05, 
    0.0), ), name='flange-csys')
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[4], orientationType=SYSTEM, 
    region=Region(faces=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((
    0.0, 48.683334, 605.333333), (1.0, 0.0, 0.0)), )))
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_NONE, angle=0.0
    , axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[5], orientationType=SYSTEM, 
    region=Region(faces=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((
    50.799998, -146.05, 302.666667), (0.0, -1.0, 0.0)), ((-50.799998, -146.05, 
    605.333333), (0.0, -1.0, 0.0)), ((50.799998, 146.05, 302.666667), (0.0, 
    -1.0, 0.0)), ((-50.799998, 146.05, 605.333333), (0.0, -1.0, 0.0)), )))
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
mdb.models['Model-1'].StaticStep(name='Step-1', previous='Initial')
mdb.models['Model-1'].rootAssembly.ReferencePoint(point=(0.0, 0.0, 0.0))
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    38.1, -146.05, 0.0), ), ((-114.3, -146.05, 0.0), ), ((38.1, 146.05, 0.0), 
    ), ((-114.3, 146.05, 0.0), ), ((0.0, -73.025, 0.0), ), ), name='t_Set-1')
mdb.models['Model-1'].RigidBody(name='Constraint-1', refPointRegion=Region(
    referencePoints=(mdb.models['Model-1'].rootAssembly.referencePoints[4], )), 
    tieRegion=mdb.models['Model-1'].rootAssembly.sets['t_Set-1'])
mdb.models['Model-1'].rootAssembly.Set(name='Set-3', referencePoints=(
    mdb.models['Model-1'].rootAssembly.referencePoints[4], ))
mdb.models['Model-1'].ConcentratedForce(cf3=11452.0, createStepName='Step-1', 
    distributionType=UNIFORM, field='', localCsys=None, name='Load-1', region=
    mdb.models['Model-1'].rootAssembly.sets['Set-3'])
mdb.models['Model-1'].rootAssembly.Set(edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    114.3, -146.05, 908.0), ), ((-38.1, -146.05, 908.0), ), ((114.3, 146.05, 
    908.0), ), ((-38.1, 146.05, 908.0), ), ((0.0, 73.025, 908.0), ), ), name=
    'Set-4')
mdb.models['Model-1'].ZsymmBC(createStepName='Initial', localCsys=None, name=
    'BC-1', region=mdb.models['Model-1'].rootAssembly.sets['Set-4'])
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    0.0, -146.05, 227.0), ), ((152.4, -146.05, 227.0), ), ((-152.4, -146.05, 
    227.0), ), ((0.0, 146.05, 227.0), ), ((152.4, 146.05, 227.0), ), ((-152.4, 
    146.05, 227.0), ), ), number=10)
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    38.1, -146.05, 0.0), ), ((114.3, -146.05, 908.0), ), ((-38.1, -146.05, 
    908.0), ), ((-114.3, -146.05, 0.0), ), ((38.1, 146.05, 0.0), ), ((114.3, 
    146.05, 908.0), ), ((-38.1, 146.05, 908.0), ), ((-114.3, 146.05, 0.0), ), )
    , number=3)
mdb.models['Model-1'].rootAssembly.seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].edges.findAt(((
    0.0, 73.025, 908.0), ), ((0.0, -73.025, 0.0), ), ), number=4)
mdb.models['Model-1'].rootAssembly.setMeshControls(regions=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    50.799998, -146.05, 302.666667), (0.0, -1.0, 0.0)), ((-50.799998, -146.05, 
    605.333333), (0.0, -1.0, 0.0)), ((50.799998, 146.05, 302.666667), (0.0, 
    -1.0, 0.0)), ((-50.799998, 146.05, 605.333333), (0.0, -1.0, 0.0)), ((0.0, 
    48.683334, 605.333333), (1.0, 0.0, 0.0)), ), technique=STRUCTURED)
mdb.models['Model-1'].rootAssembly.setElementType(elemTypes=(ElemType(
    elemCode=S8R, elemLibrary=STANDARD), ElemType(elemCode=STRI65, 
    elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces.findAt(((
    50.799998, -146.05, 302.666667), (0.0, -1.0, 0.0)), ((-50.799998, -146.05, 
    605.333333), (0.0, -1.0, 0.0)), ((50.799998, 146.05, 302.666667), (0.0, 
    -1.0, 0.0)), ((-50.799998, 146.05, 605.333333), (0.0, -1.0, 0.0)), ((0.0, 
    48.683334, 605.333333), (1.0, 0.0, 0.0)), ), ))
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
mdb.models['Model-1'].rootAssembly.Set(name='Cpoint', nodes=
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].nodes[83:84])
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Initial', 
    distributionType=UNIFORM, fieldName='', localCsys=None, name='BC-2', 
    region=mdb.models['Model-1'].rootAssembly.sets['Cpoint'], u1=SET, u2=SET, 
    u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=SET)
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, numGPUs=0, queue=None, resultsFormat=ODB, scratch='', type=
    ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)