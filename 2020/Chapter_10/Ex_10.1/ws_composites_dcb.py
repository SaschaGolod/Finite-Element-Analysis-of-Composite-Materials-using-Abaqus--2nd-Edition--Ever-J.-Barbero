#
#    Analysis of Composite Materials with Abaqus
#    Double Cantilever Beam Problem
#
from abaqus import *
from abaqusConstants import *
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
Mdb()

mdb.models.changeKey(fromName='Model-1', toName='coh-els')

session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['coh-els'].ConstrainedSketch(name='__profile__', sheetSize=0.5)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(
    point1=(0.0, 0.0),
    point2=(0.1, 0.0015))
p = mdb.models['coh-els'].Part(
    name='beam',
    dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['coh-els'].parts['beam']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['coh-els'].sketches['__profile__']

p = mdb.models['coh-els'].parts['beam']
c, f, e, v, d  = p.cells, p.faces, p.edges, p.vertices, p.datums

s1 = mdb.models['coh-els'].ConstrainedSketch(name='__profile__', sheetSize=0.5)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(
    point1=(0.0, 0.0),
    point2=(0.07, 0.001))
p = mdb.models['coh-els'].Part(
    name='adhesive',
    dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['coh-els'].parts['adhesive']
p.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['coh-els'].sketches['__profile__']

p = mdb.models['coh-els'].parts['adhesive']
c, f, e, v, d  = p.cells, p.faces, p.edges, p.vertices, p.datums

### End Part Creation

#Create bulk material

mdb.models['coh-els'].Material(name='bulk')
mdb.models['coh-els'].materials['bulk'].Elastic(
    type=ENGINEERING_CONSTANTS, 
    table=((1.353e11, 9e9, 9e9, 0.24, 0.24, 0.46, 4.5e9, 3.3e9, 4.5e9), ))

#Create and Assign Bulk Section
mdb.models['coh-els'].HomogeneousSolidSection(
    name='bulk',
    material='bulk', 
    thickness=0.02)
p = mdb.models['coh-els'].parts['beam']
f = p.faces
faces = f
region = regionToolset.Region(faces=faces)
p.SectionAssignment(
    region=region,
    sectionName='bulk')

p.DatumCsysByThreePoints(
    name='Datum csys-1',
    coordSysType=CARTESIAN,
    origin=(0.0, 0.0, 0.0),
    line1=(1.0, 0.0, 0.0),
    line2=(0.0, 1.0, 0.0))
region = regionToolset.Region(faces=faces)
orientation = mdb.models['coh-els'].parts['beam'].datums[3]
mdb.models['coh-els'].parts['beam'].MaterialOrientation(
    region=region, 
    orientationType=SYSTEM,
    localCsys=orientation,
    axis=AXIS_3, 
    additionalRotationType=ROTATION_NONE,
    angle=0.0)

##Begin Assembly


a = mdb.models['coh-els'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)

p = mdb.models['coh-els'].parts['beam']
a.Instance(name='beam-1', part=p, dependent=ON)

p = mdb.models['coh-els'].parts['beam']
a.Instance(name='beam-2', part=p, dependent=ON)

p1 = a.instances['beam-2']
p1.translate(vector=(0.0, -0.0015, 0.0))

p = mdb.models['coh-els'].parts['adhesive']
a.Instance(name='adhesive-1', part=p, dependent=ON)

p1 = a.instances['adhesive-1']
p1.translate(vector=(0.030, -0.0005, 0.0))

v1 = a.instances['beam-1'].vertices
verts1 = v1.findAt(((0.0, 0.0015, 0.0), ))
a.Set(vertices=verts1, name='top')

v1 = a.instances['beam-2'].vertices
verts1 = v1.findAt(((0.0, -0.0015, 0.0), ))
a.Set(vertices=verts1, name='bot')

s1 = a.instances['beam-1'].edges
side1Edges1 = s1.findAt(((0.075, 0.0, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='top')

s1 = a.instances['beam-2'].edges
side1Edges1 = s1.findAt(((0.075, 0.0, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='bot')

s1 = a.instances['adhesive-1'].edges
side1Edges1 = s1.findAt(((0.0475, 0.0005, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='coh-top')

s1 = a.instances['adhesive-1'].edges
side1Edges1 = s1.findAt(((0.0475, -0.0005, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='coh-bot')


mdb.Model(name='vcct-xpl-shell')

session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['vcct-xpl-shell'].ConstrainedSketch(
    name='__profile__', 
    sheetSize=1.0)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.Line(
    point1=(0.0, 0.0),
    point2=(0.1, 0.0))
s.HorizontalConstraint(entity=g.findAt((0.05, 0.0)))
p = mdb.models['vcct-xpl-shell'].Part(
    name='beam',
    dimensionality=THREE_D, 
    type=DEFORMABLE_BODY)
p = mdb.models['vcct-xpl-shell'].parts['beam']
p.BaseShellExtrude(
    sketch=s,
    depth=0.02)
s.unsetPrimaryObject()
del mdb.models['vcct-xpl-shell'].sketches['__profile__']

p = mdb.models['vcct-xpl-shell'].parts['beam']
session.viewports['Viewport: 1'].setValues(displayedObject=p)

c, f, e, v, d  = p.cells, p.faces, p.edges, p.vertices, p.datums

pickedEdges = e.findAt(((0.075, 0.0, 0.02), ))
p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.7)
pickedEdges = e.findAt(((0.025, 0.0, 0.0), ))
p.PartitionEdgeByParam(edges=pickedEdges, parameter=0.3)

c, f, e, v, d  = p.cells, p.faces, p.edges, p.vertices, p.datums

pickedFaces = f.findAt(((0.066667, 0.0, 0.013333), ))
p.PartitionFaceByShortestPath(
    point1=v.findAt(coordinates=(0.03, 0.0, 0.02)), 
    point2=v.findAt(coordinates=(0.03, 0.0, 0.0)),
    faces=pickedFaces)

c, f, e, v, d  = p.cells, p.faces, p.edges, p.vertices, p.datums

side1Faces = f
p.Surface(side1Faces=side1Faces, name='contact')

edges = e.findAt(((0.0, 0.0, 0.005), ))
p.Set(edges=edges, name='pull')

edges = e.findAt(
    ((0.0475, 0.0, 0.0), ),
    ((0.0825, 0.0, 0.02), ),
    ((0.0225, 0.0, 0.02), ),
    ((0.0075, 0.0, 0.0), ))
p.Set(edges=edges, name='symm')

pickedEdges = e.findAt(((0.0225, 0.0, 0.02), ))
p.seedEdgeByNumber(edges=pickedEdges, number=24)

pickedEdges = e.findAt(((0.0825, 0.0, 0.02), ))
p.seedEdgeByNumber(edges=pickedEdges, number=56)

pickedEdges = e.findAt(((0.0475, 0.0, 0.0), ))
p.seedEdgeByNumber(edges=pickedEdges, number=56)

pickedEdges = e.findAt(((0.0075, 0.0, 0.0), ))
p.seedEdgeByNumber(edges=pickedEdges, number=24)

p.seedPart(size=0.005, deviationFactor=0.1)

f = p.faces
pickedRegions = f.findAt(
    ((0.053333, 0.0, 0.006667), ),
    ((0.02, 0.0, 0.013333), ))
p.setMeshControls(regions=pickedRegions, allowMapped=True)


p.generateMesh()

elemType1 = mesh.ElemType(
    elemCode=S4,
    elemLibrary=EXPLICIT, 
    secondOrderAccuracy=OFF,
    hourglassControl=DEFAULT)
elemType2 = mesh.ElemType(
    elemCode=S3R,
    elemLibrary=EXPLICIT)

faces = f
pickedRegions =(faces, )
p.setElementType(regions=pickedRegions, elemTypes=(elemType1, elemType2))

mdb.models['vcct-xpl-shell'].Material(name='bulk')
mdb.models['vcct-xpl-shell'].materials['bulk'].Elastic(type=LAMINA, 
    table=((1.353e11, 9.e9, 0.24, 4.5e9, 3.3e9, 4.5e9), ))
mdb.models['vcct-xpl-shell'].materials['bulk'].Density(table=((0.01, ), ))

mdb.saveAs('dcb')
