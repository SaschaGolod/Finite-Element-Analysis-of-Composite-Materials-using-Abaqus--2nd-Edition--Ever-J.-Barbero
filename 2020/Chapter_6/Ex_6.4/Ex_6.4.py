""" Example 6.4 using Constraint Equations CE, 2D Geometry """
# import modules
mdb.close()
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
# recoverGeometry for easy parameterization
session.journalOptions.setValues(recoverGeometry=COORDINATE)
# session colors
session.viewports['Viewport: 1'].viewportAnnotationOptions.setValues(title=OFF)
session.graphicsOptions.setValues(backgroundStyle=SOLID, 
    backgroundColor='#FFFFFF', translucencyMode=2)

# Geometry
rf = 3.5
a2 = 5.270
a3 = 9.128 
a1 = a2/4.
# Materials
Ef, nuf = 0.241, 0.2  # TPa
Em, num = 0.00312, 0.38
# Load
strain = [0.002, 0.0, 0.001]    # epsilon_11, epsilon_22, gamma_12
# Seed spacing
MeshingSize = 0.4

# define Part-1
mdb.models['Model-1'].ConstrainedSketch(name='__profile__', sheetSize=20.0)
mdb.models['Model-1'].sketches['__profile__'].rectangle(point1=(-a2, -a3), 
    point2=(a2, a3))
mdb.models['Model-1'].Part(dimensionality=TWO_D_PLANAR, name='Part-1', type=
    DEFORMABLE_BODY)

# sketch
mdb.models['Model-1'].parts['Part-1'].BaseShell(sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']
mdb.models['Model-1'].ConstrainedSketch(gridSpacing=1.0, name='__profile__', 
    sheetSize=40, transform=
    mdb.models['Model-1'].parts['Part-1'].MakeSketchTransform(
    sketchPlane=mdb.models['Model-1'].parts['Part-1'].faces.findAt((0., 
    0., 0.0), (0.0, 0.0, 1.0)), sketchPlaneSide=SIDE1, 
    sketchOrientation=RIGHT, origin=(0.0, 0.0, 0.0)))
mdb.models['Model-1'].parts['Part-1'].projectReferencesOntoSketch(filter=
    COPLANAR_EDGES, sketch=mdb.models['Model-1'].sketches['__profile__'])
mdb.models['Model-1'].sketches['__profile__'].CircleByCenterPerimeter(center=(
    0.0, 0.0), point1=(0.0, rf))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(center=(-a2, 
    a3), direction=CLOCKWISE, point1=(-(a2-rf), a3), point2=(-a2, a3-rf))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(center=(a2, 
    a3), direction=COUNTERCLOCKWISE, point1=(a2-rf, a3), point2=(a2, 
    a3-rf))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(center=(-a2, 
    -a3), direction=COUNTERCLOCKWISE, point1=(-(a2-rf), -a3), point2=(-a2, 
    -(a3-rf)))
mdb.models['Model-1'].sketches['__profile__'].ArcByCenterEnds(center=(a2, 
    -a3), direction=CLOCKWISE, point1=(a2-rf, -a3), point2=(a2, -(a3-rf)))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(0.0, a3), point2=
    (0.0, -a3))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-a2, 0.0), point2=
    (a2, 0.0))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-a2, a3/2.), 
    point2=(a2, a3/2.))
mdb.models['Model-1'].sketches['__profile__'].Line(point1=(-a2, -a3/2.), 
    point2=(a2, -a3/2.))
mdb.models['Model-1'].parts['Part-1'].PartitionFaceBySketch(faces=
    mdb.models['Model-1'].parts['Part-1'].faces.findAt(((0.0, 0.0, 
    0.0), (0.0, 0.0, 1.0)), ), sketch=
    mdb.models['Model-1'].sketches['__profile__'])
del mdb.models['Model-1'].sketches['__profile__']

# Materials
mdb.models['Model-1'].Material(name='fiber')
mdb.models['Model-1'].materials['fiber'].Elastic(table=((Ef, nuf), ))
mdb.models['Model-1'].Material(name='matrix')
mdb.models['Model-1'].materials['matrix'].Elastic(table=((Em, num), ))

# Sections
mdb.models['Model-1'].HomogeneousSolidSection(material='fiber', name=
    'fiber-sec', thickness=None)
mdb.models['Model-1'].HomogeneousSolidSection(material='matrix', name=
    'matrix-sec', thickness=None)
    
# Section Assigment
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((2.0**0.5/2.*rf, 
    2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 1.0)), ((-2.0**0.5/2.*rf, 2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 
    1.0)), ((-2.0**0.5/2.*rf, -2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 1.0)), ((2.0**0.5/2.*rf, -2.0**0.5/2.*rf, 
    0.0), (0.0, 0.0, 1.0)), ((a2-2.0**0.5/4.*rf, a3-2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)), ((
    -a2+2.0**0.5/4.*rf, a3-2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)), ((-a2+2.0**0.5/4.*rf, -a3+2.0**0.5/4.*rf, 0.0), (
    0.0, 0.0, 1.0)), ((a2-2.0**0.5/4.*rf, -a3+2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)), )), 
    sectionName='fiber-sec', thicknessAssignment=FROM_SECTION)
mdb.models['Model-1'].parts['Part-1'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=Region(
    faces=mdb.models['Model-1'].parts['Part-1'].faces.findAt(((-(a2-rf)/2., 
    a3-a3/4.0, 0.0), (0.0, 0.0, 1.0)), (((a2-rf)/2., a3-a3/4.0, 0.0), (0.0, 0.0, 
    1.0)), ((-a2+(a2-rf)/2., a3/4., 0.0), (0.0, 0.0, 1.0)), ((-(-a2+(a2-rf)/2.), a3/4.0, 
    0.0), (0.0, 0.0, 1.0)), ((-(a2-rf)/2., -(a3-a3/4.0), 0.0), (0.0, 0.0, 1.0)), (
    ((a2-rf)/2., -(a3-a3/4.0), 0.0), (0.0, 0.0, 1.0)), ((-a2+(a2-rf)/2., -a3/4., 0.0), 
    (0.0, 0.0, 1.0)), ((-(-a2+(a2-rf)/2.), -a3/4.0,0.0), (0.0, 0.0, 1.0)), )), 
    sectionName='matrix-sec', thicknessAssignment=FROM_SECTION)
    
# Create Sets:  Face1, Face2, Face3, Face4, Vertex1, Vertex2, Vertex3, Vertex4
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt(((a2, a3-(rf/2.0), 0.0), ), 
    ((a2, a3-rf-(a3/2.-rf)/2., 0.0), ), ((a2, a3/4., 0.0), ), ((a2,-a3/4., 0.0), ), ((
    a2, -(a3-rf-(a3/2.-rf)/2.), 0.0), ), ((a2, -(a3-(rf/2.0)), 0.0), ), ), name='Face1')
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt(((a2-rf/2., a3, 0.0), ), 
    ((-(a2-rf)/2., a3, 0.0), ), (((a2-rf)/2, a3, 0.0), ), ((-(a2-rf/2.), a3, 0.0), 
    ), ), name='Face2')    
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt(((-a2, a3-(rf/2.0), 0.0), ), 
    ((-a2, a3-rf-(a3/2.-rf)/2., 0.0), ), ((-a2, a3/4., 0.0), ), ((-a2,-a3/4., 0.0), ), ((
    -a2, -(a3-rf-(a3/2.-rf)/2.), 0.0), ), ((-a2, -(a3-(rf/2.0)), 0.0), ), ), name='Face3')
mdb.models['Model-1'].parts['Part-1'].Set(edges=
    mdb.models['Model-1'].parts['Part-1'].edges.findAt(((a2-rf/2., -a3, 0.0), ), 
    ((-(a2-rf)/2., -a3, 0.0), ), (((a2-rf)/2, -a3, 0.0), ), ((-(a2-rf/2.), -a3, 0.0), 
    ), ), name='Face4') 
mdb.models['Model-1'].parts['Part-1'].Set(name='Vertex1', vertices=
    mdb.models['Model-1'].parts['Part-1'].vertices.findAt(((a2, a3, 0.0), 
    ), ))
mdb.models['Model-1'].parts['Part-1'].Set(name='Vertex2', vertices=
    mdb.models['Model-1'].parts['Part-1'].vertices.findAt(((-a2, a3, 0.0), 
    ), ))
mdb.models['Model-1'].parts['Part-1'].Set(name='Vertex3', vertices=
    mdb.models['Model-1'].parts['Part-1'].vertices.findAt(((-a2, -a3, 0.0), 
    ), ))
mdb.models['Model-1'].parts['Part-1'].Set(name='Vertex4', vertices=
    mdb.models['Model-1'].parts['Part-1'].vertices.findAt(((a2, -a3, 0.0), 
    ), ))    

# Instance    
mdb.models['Model-1'].rootAssembly.DatumCsysByDefault(CARTESIAN)
mdb.models['Model-1'].rootAssembly.Instance(dependent=ON, name='Part-1-1', 
    part=mdb.models['Model-1'].parts['Part-1'])

# Mesh of plane strain elements CPE4
mdb.models['Model-1'].parts['Part-1'].seedPart(deviationFactor=0.1, size=MeshingSize)
mdb.models['Model-1'].parts['Part-1'].setElementType(elemTypes=(ElemType(
    elemCode=CPE4, elemLibrary=STANDARD), ElemType(elemCode=CPE3, 
    elemLibrary=STANDARD)), regions=(
    mdb.models['Model-1'].parts['Part-1'].faces.findAt(((2.0**0.5/2.*rf, 
    2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 1.0)), ((-2.0**0.5/2.*rf, 2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 
    1.0)), ((-2.0**0.5/2.*rf, -2.0**0.5/2.*rf, 0.0), (0.0, 0.0, 1.0)), ((2.0**0.5/2.*rf, -2.0**0.5/2.*rf, 
    0.0), (0.0, 0.0, 1.0)), ((a2-2.0**0.5/4.*rf, a3-2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)), ((
    -a2+2.0**0.5/4.*rf, a3-2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)), ((-a2+2.0**0.5/4.*rf, -a3+2.0**0.5/4.*rf, 0.0), (
    0.0, 0.0, 1.0)), ((a2-2.0**0.5/4.*rf, -a3+2.0**0.5/4.*rf, 0.0), (0.0, 0.0, 1.0)),((-(a2-rf)/2., 
    a3-a3/4.0, 0.0), (0.0, 0.0, 1.0)), (((a2-rf)/2., a3-a3/4.0, 0.0), (0.0, 0.0, 
    1.0)), ((-a2+(a2-rf)/2., a3/4., 0.0), (0.0, 0.0, 1.0)), ((-(-a2+(a2-rf)/2.), a3/4.0, 
    0.0), (0.0, 0.0, 1.0)), ((-(a2-rf)/2., -(a3-a3/4.0), 0.0), (0.0, 0.0, 1.0)), (
    ((a2-rf)/2., -(a3-a3/4.0), 0.0), (0.0, 0.0, 1.0)), ((-a2+(a2-rf)/2., -a3/4., 0.0), 
    (0.0, 0.0, 1.0)), ((-(-a2+(a2-rf)/2.), -a3/4.0,0.0), (0.0, 0.0, 1.0)),), ))
mdb.models['Model-1'].parts['Part-1'].generateMesh()
    
# Step
mdb.models['Model-1'].StaticLinearPerturbationStep(
    name='Step-1', previous='Initial')

# Field Output Request
mdb.models['Model-1'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'LE', 'U', 'RF', 'CF', 'IVOL', 'STH'))
# Save the .mdb and .cae
mdb.saveAs(pathName='Ex_6.4.cae')

# Constraint equations
execfile('PBC_2D.py') 

# Job
mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='Model-1', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='Job-1', nodalOutputPrecision=SINGLE, 
    numCpus=1, queue=None, scratch='', type=ANALYSIS, userSubroutine='', 
    waitHours=0, waitMinutes=0)
mdb.jobs['Job-1'].setValues(numCpus=8, numDomains=8)
mdb.jobs['Job-1'].submit(consistencyChecking=OFF)   
mdb.jobs['Job-1'].waitForCompletion()

# Calculate Average Stresses and Strains
execfile('srecover2D.py')

# visualize
o3 = session.openOdb(name='Job-1.odb')
session.viewports['Viewport: 1'].setValues(displayedObject=o3)
