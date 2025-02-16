""" Script to generate Example 6.5 """

# make sure the Work Directory is OK
import os
os.chdir(r'C:\Simulia\User\Chapter_6\Ex_6.5')

# -*- coding: mbcs -*-
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *

# save .mdb in the correct work directory
mdb.saveAs(pathName='C:/Simulia/User/Chapter_6/Ex_6.5/Ex_6.5.cae')

# create part
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=10.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(0.0, 0.0), 
    point2=(1.0, 1.0))
mdb.models['Model-1'].Part(dimensionality=THREE_D, name='Part-1', type=
    DEFORMABLE_BODY)
mdb.models['Model-1'].parts['Part-1'].BaseSolidExtrude(depth=5.0, sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# create datum planes to later partition
mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=1.25, 
    principalPlane=XYPLANE)
mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=2.5, 
    principalPlane=XYPLANE)
mdb.models['Model-1'].parts['Part-1'].DatumPlaneByPrincipalPlane(offset=3.75, 
    principalPlane=XYPLANE)
    
# partition
mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
    mdb.models['Model-1'].parts['Part-1'].cells[0:1], datumPlane=
    mdb.models['Model-1'].parts['Part-1'].datums[2])
mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
    mdb.models['Model-1'].parts['Part-1'].cells[0:1], datumPlane=
    mdb.models['Model-1'].parts['Part-1'].datums[3])
mdb.models['Model-1'].parts['Part-1'].PartitionCellByDatumPlane(cells=
    mdb.models['Model-1'].parts['Part-1'].cells[1:2], datumPlane=
    mdb.models['Model-1'].parts['Part-1'].datums[4])
    
# create material
mdb.models['Model-1'].Material(name='Material-1')
mdb.models['Model-1'].materials['Material-1'].Elastic(table=((139000.0, 
    14500.0, 14500.0, 0.21, 0.21, 0.38, 5860.0, 5860.0, 2930.0), ), type=
    ENGINEERING_CONSTANTS)
    
# create datum coordinate system
mdb.models['Model-1'].parts['Part-1'].DatumCsysByTwoLines(CARTESIAN, line1=
    mdb.models['Model-1'].parts['Part-1'].edges[21], line2=
    mdb.models['Model-1'].parts['Part-1'].edges[17], name='Datum csys-1')
    
# define material orientations
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_ANGLE, angle=
    0.0, axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[8], orientationType=SYSTEM, 
    region=Region(cells=mdb.models['Model-1'].parts['Part-1'].cells[0:1]), 
    stackDirection=STACK_3)
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_ANGLE, angle=
    90.0, axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[8], orientationType=SYSTEM, 
    region=Region(cells=mdb.models['Model-1'].parts['Part-1'].cells[2:3]), 
    stackDirection=STACK_3)
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_ANGLE, angle=
    -45.0, axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[8], orientationType=SYSTEM, 
    region=Region(cells=mdb.models['Model-1'].parts['Part-1'].cells[1:2]), 
    stackDirection=STACK_3)
mdb.models['Model-1'].parts['Part-1'].MaterialOrientation(
    additionalRotationField='', additionalRotationType=ROTATION_ANGLE, angle=
    45.0, axis=AXIS_3, fieldName='', localCsys=
    mdb.models['Model-1'].parts['Part-1'].datums[8], orientationType=SYSTEM, 
    region=Region(cells=mdb.models['Model-1'].parts['Part-1'].cells[3:4]), 
    stackDirection=STACK_3)
    
# section create
mdb.models['Model-1'].HomogeneousSolidSection(material='Material-1', name=
    'Section-1', thickness=None)
    
# assign sections
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    cells=mdb.models['Model-1'].parts['Part-1'].cells[0:4]), sectionName=
    'Section-1', thicknessAssignment=FROM_SECTION)
    
# assembly instance create
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=OFF, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])
    
# step
mdb.models['Model-1'].StaticLinearPerturbationStep(name='Step-1', previous=
    'Initial')
    
# output requests
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'E', 'S', 'U', 'IVOL'))
    
# boundary conditions
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[2:3]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[8:9]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[11:12]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[18:19]), u1=
    0.0, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-2', region=Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[3:4]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[7:8]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[13:14]+\
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[16:17]), u1=
    1.0, u2=0.0, u3=UNSET, ur1=UNSET, ur2=UNSET, ur3=UNSET)
mdb.models['Model-1'].ZsymmBC(createStepName='Step-1', name='BC-3', region=
    Region(
    faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].faces[20:21]))
    
# tie constraints
mdb.models['Model-1'].Tie(adjust=OFF, master=Region(
    side1Faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1']
    .faces.getSequenceFromMask(
    mask=('[#c050 ]', ), )), name='Constraint-1', positionTolerance=1.0, 
    positionToleranceMethod=SPECIFIED, slave=Region(
    side1Faces=mdb.models['Model-1'].rootAssembly.instances['Part-1-1']
    .faces.getSequenceFromMask(
    mask=('[#21202 ]', ), )), thickness=ON, tieRotations=ON)
    
# seed and mesh
mdb.models['Model-1'].rootAssembly.seedPartInstance(deviationFactor=0.1, 
    regions=(mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ), size=
    1.25)
mdb.models['Model-1'].rootAssembly.generateMesh(regions=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'], ))
    
# Job
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)

# Wait for Job to finish
mdb.jobs['Job-1'].waitForCompletion()
