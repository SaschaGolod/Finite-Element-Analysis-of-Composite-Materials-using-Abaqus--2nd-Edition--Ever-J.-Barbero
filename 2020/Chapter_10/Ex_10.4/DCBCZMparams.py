# DCB CZM Parameters (c) 2022 Ever Barbero
# select LINEAR, EXPONENTIAL, OR TABULAR at line ~221
# Select H/L data at line ~364
import time
start_time = time.time()
import os

# ***** Units [N, m] *****
L1 = 180.;# [mm] 2*L in ENFdimensions.png
t1 = 2.0;# [mm] Substrate thickness, each
a0 = 20.0# initial crack length, re-read as state[0]
La = L1-a0;# adhesive length, re-calculate below
ta = 1.0;# adhesive thickness
B = 25.0;# [mm] specimen width (vcct_width)
u2target = 1.546;# [mm] COD, total opening, FEA calculates 1/2 of this
# Substrate properties
E1 = 200.0E3; E2 = E1; E3 = E1 #Steel
Nu12 = 0.33; Nu13 = Nu12; Nu23 = Nu12
G12 = E1/2/(1+Nu12); G13 = G12; G23 = G12;
# Adhesive moduli
Ea = 1590.0 # MPa
nua = 0.35  # 
Ess = Ea/2.0/(1.0+nua); Ett = Ess #[N/mm^2] shear
# Calculate penalty stiffness here, do not let Abaqus calculate it
Kn = Ea/ta; Ks = Ess/ta; Kt = Ett/ta; # re-read Kn from state below
# Adhesive strengths 
tno = 22.6 #[N/mm^2] adhesive strength, re-read from state below
tso = tno; tto = tno;#[N/mm^2] 
# Fracture energies 
Gnc = 1.56 #[N/mm], normal mode, re-read from state below
Gsc = Gnc; Gtc = Gnc;#[N/mm] 
# BKpower = 0.284 #BK exponent
Vc1 = 0.1       # DamageStabilizationCohesive has NO effect
Vc2 = 0.0002    # DAMPING_FACTOR
Vc3 = 0.0500    #adaptiveDampingRatio=max.0.05 else spurious results
initialInc=0.01; maxNumInc=2000; minInc=1e-09; maxInc=0.01;

# Read the current state x from file
import numpy
state = numpy.loadtxt("state.txt") # read state
a0  = state[0]# if adjusting a0, La = L1-a0 calculated below
Kn  = state[1]
tno = state[2]
Gnc = state[3]
u2target = state[4] # [mm} 
u2target = u2target/2# 1/2 up, 1/2 down in the simulation 
print state

# LINEAR and EXPONENTIAL use tno, Gnc, Kn. 
# For TABULAR, calculate tabular delta & D from Fig. (c)2021 Ever Barbero
# see line 236 for usage D[0], delta[0], etc.
delta = [0,0,0]# book notation [delta0, delta1, delta2]
delta[0] = tno/Kn# slope Kn linear region, D=0, tno=Kn*delta[1]
delta[1] = Gnc/tno# right and left triangles have same area
delta[2] = delta[1] + delta[0]# equal triangles
D = [0,0,0]# book notation
D[0] = 0.;# damage=0 from {0,0} to {delta[0],tno} 
D[1] = 1.-tno/(Kn*delta[1]);# slope=tno/delta[1]=(1-D[1])*Kn
D[2] = 1.;# at {delta[1],0} damage reaches 1
print "before shift ", delta, D
# Abaqus table origin is at coordinates {delta[0],tno}, must shift
shift = delta[0]# shift this much
delta[0]=delta[0]-shift;# = 0
delta[1]=delta[1]-shift;
delta[2]=delta[2]-shift;
print "after shift ", delta, D

# Meshing (c) 2021 Ever Barbero
position_tolerance = 1.1*ta/2 # mm for interaction to occur
# Calculate element size (esize), number of elements neL1, neLa
t1Seeds = 2# number of elements thru thickness
t1Bias  = 1# bias, best is no bias
factor  = 4# multiplies L1 to get neX
neL1 = int(factor*L1)# elements over specimen length, L1 in [mm]
esize = L1/neL1# real value, element size along X
nea0 = int(a0/esize)# number of elements in the initial-crack
a0 = nea0*esize# recalculate a0 to fit exactly nea0 elements
La = L1-a0;# re-calculate the adhesive length
neLa = neL1 - nea0# number of elements in the adhesive
print ('nea0=%g neLa=%g neY=%g \n' % (nea0, neLa, t1Seeds))
# end properties input

# Parameterized modeling script starts here
from abaqus import *
from abaqusConstants import *
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
# from driverUtils import executeOnCaeStartup
# executeOnCaeStartup()
Mdb()
mdb.models.changeKey(fromName='Model-1', toName='coh-els')
# Parameterize ws_composites_dcb.py (c) 2022 Ever Barbero
# Module: Part
session.viewports['Viewport: 1'].setValues(displayedObject=None)
s = mdb.models['coh-els'].ConstrainedSketch(name='__profile__', sheetSize=0.5)
g, v, d, c = s.geometry, s.vertices, s.dimensions, s.constraints
s.setPrimaryObject(option=STANDALONE)
s.rectangle(
    point1=(0.0, 0.0),
    point2=(L1, t1))    
p = mdb.models['coh-els'].Part(
    name='beam',
    dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['coh-els'].parts['beam']
p.BaseShell(sketch=s)
s.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['coh-els'].sketches['__profile__']

s1 = mdb.models['coh-els'].ConstrainedSketch(name='__profile__', sheetSize=0.5)
g, v, d, c = s1.geometry, s1.vertices, s1.dimensions, s1.constraints
s1.setPrimaryObject(option=STANDALONE)
s1.rectangle(
    point1=(0.0, 0.0),
    point2=(La, ta))    
p = mdb.models['coh-els'].Part(
    name='adhesive',
    dimensionality=TWO_D_PLANAR, 
    type=DEFORMABLE_BODY)
p = mdb.models['coh-els'].parts['adhesive']
p.BaseShell(sketch=s1)
s1.unsetPrimaryObject()
session.viewports['Viewport: 1'].setValues(displayedObject=p)
del mdb.models['coh-els'].sketches['__profile__']

#Create bulk material [MPa, mm]
mdb.models['coh-els'].Material(name='bulk')
mdb.models['coh-els'].materials['bulk'].Elastic(
    type=ENGINEERING_CONSTANTS, 
    table= ((E1, E2, E3, Nu12, Nu13, Nu23, G12, G13, G23), ))

#Create and Assign Bulk Section
mdb.models['coh-els'].HomogeneousSolidSection(
    name='bulk',
    material='bulk', 
    thickness=B)
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

#Begin Assembly
a = mdb.models['coh-els'].rootAssembly
a.DatumCsysByDefault(CARTESIAN)
p = mdb.models['coh-els'].parts['beam']
a.Instance(name='beam-1', part=p, dependent=ON)
p = mdb.models['coh-els'].parts['beam']
a.Instance(name='beam-2', part=p, dependent=ON)
p1 = a.instances['beam-2']
p1.translate(vector=(0.0, -t1, 0.0))
p = mdb.models['coh-els'].parts['adhesive']
a.Instance(name='adhesive-1', part=p, dependent=ON)
p1 = a.instances['adhesive-1']
p1.translate(vector=(a0, -ta/2, 0.0))
v1 = a.instances['beam-1'].vertices
verts1 = v1.findAt(((0.0, t1, 0.0), ))
a.Set(vertices=verts1, name='top')
v1 = a.instances['beam-2'].vertices
verts1 = v1.findAt(((0.0, -t1, 0.0), ))
a.Set(vertices=verts1, name='bot')
s1 = a.instances['beam-1'].edges
side1Edges1 = s1.findAt(((L1/2, 0.0, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='top')
s1 = a.instances['beam-2'].edges
side1Edges1 = s1.findAt(((L1/2, 0.0, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='bot')
# All entities use same c.s., origing at left-end of crack. 
s1 = a.instances['adhesive-1'].edges
side1Edges1 = s1.findAt(((a0+1, ta/2, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='coh-top')
s1 = a.instances['adhesive-1'].edges
side1Edges1 = s1.findAt(((a0+1, -ta/2, 0.0), ))
a.Surface(side1Edges=side1Edges1, name='coh-bot')
mdb.saveAs('DCBCZMparams.cae')   
#parameterized ws_composites_dcb.py ends here

# New script (c) 2021 Ever Barbero, not available in ws_composites_dcb.py 
from part import *
from material import *
from section import *
from assembly import *
from step import *
from interaction import *
from load import *
from mesh import *
from optimization import *
from job import *
from sketch import *
from visualization import *
from connectorBehavior import *
# Module: Property
mdb.models['coh-els'].Material(name='cohesive')
mdb.models['coh-els'].materials['cohesive'].Elastic(table=((Kn, Ks,
    Kt), ), type=TRACTION)# see (*1) below 
mdb.models['coh-els'].materials['cohesive'].QuadsDamageInitiation(table=((tno, 
    tso, tto), ))#damage initiation stress tno, tso, tto
mdb.models['coh-els'].materials['cohesive'].quadsDamageInitiation.DamageStabilizationCohesive(
    cohesiveCoeff=Vc1)#stabilization coefficient

# LINEAR SOFTENING (TRIANGULAR), default:MODE_INDEPENDENT 
# mdb.models['coh-els'].materials['cohesive'].quadsDamageInitiation.\
    # DamageEvolution(
    # softening=LINEAR, table=((Gnc, ), ), type=ENERGY, 
    # mixedModeBehavior=MODE_INDEPENDENT)

# EXPONENTIAL SOFTENING, default:MODE_INDEPENDENT 
# mdb.models['coh-els'].materials['cohesive'].quadsDamageInitiation.\
    # DamageEvolution(
    # softening=EXPONENTIAL, table=((Gnc, ), ), type=ENERGY,
    # mixedModeBehavior=MODE_INDEPENDENT)

# TABULAR SOFTENING (TRAPEZOIDAL), default:MODE_INDEPENDENT, book notation 
mdb.models['coh-els'].materials['cohesive'].quadsDamageInitiation.\
    DamageEvolution(softening=TABULAR, 
    table=((D[0], delta[0]), (D[1], delta[1]), (D[2], delta[2])), 
    type=DISPLACEMENT, mixedModeBehavior=MODE_INDEPENDENT)

# Menu: Section, Manager, works for linear, tabular, exponential. 
# (*1) CAE section traction separation initial thick "analysis default" use Kn,Ks,Kt as calculated above 
mdb.models['coh-els'].CohesiveSection(material='cohesive', name='cohesive', 
    outOfPlaneThickness=B, response=TRACTION_SEPARATION)# takes Kn as penalty stiffness
# (*2) CAE section traction separation initial thick "specify" = ta, 
#       requires above Elastic(table=((Ea, Ess,Ett), 
#       confusing because LINEAR and TABULAR diagrams 
#       use Kn,Ks,Kt, not Ea,Ess,Ett
# mdb.models['coh-els'].CohesiveSection(initialThickness=ta, 
    # initialThicknessType=SPECIFY, material='cohesive', name='cohesive', 
    # outOfPlaneThickness=B, response=TRACTION_SEPARATION)

# Menu: Assign, Section
mdb.models['coh-els'].parts['adhesive'].Set(faces=
    mdb.models['coh-els'].parts['adhesive'].faces.findAt(((La/2, ta/3, 
    0.0), (0.0, 0.0, 1.0)), ), name='Set-1')
mdb.models['coh-els'].parts['adhesive'].SectionAssignment(offset=0.0, 
    offsetField='', offsetType=MIDDLE_SURFACE, region=
    mdb.models['coh-els'].parts['adhesive'].sets['Set-1'], sectionName=
    'cohesive', thicknessAssignment=FROM_SECTION)
# Module: Step
mdb.models['coh-els'].rootAssembly.regenerate()
# Create Set to apply the load
mdb.models['coh-els'].rootAssembly.Set(name='topLoad', vertices=
    mdb.models['coh-els'].rootAssembly.instances['beam-1'].vertices.findAt(((
    0.0, t1, 0.0), ), ))#new top
# define Step
mdb.models['coh-els'].StaticStep(initialInc=initialInc, maxNumInc=maxNumInc, minInc=minInc, 
    maxInc=maxInc, name='Step-1', nlgeom=ON, previous='Initial', adaptiveDampingRatio=Vc3, 
    continueDampingFactors=False, stabilizationMagnitude=Vc2,
    stabilizationMethod=DAMPING_FACTOR)
mdb.models['coh-els'].fieldOutputRequests['F-Output-1'].setValues(variables=(
    'S', 'LE', 'U', 'RF', 'STATUS'))
mdb.models['coh-els'].HistoryOutputRequest(createStepName='Step-1', name=
    'H-Output-2', rebar=EXCLUDE, region=
    mdb.models['coh-els'].rootAssembly.sets['topLoad'], sectionPoints=DEFAULT, 
    variables=('U2', 'RF2'))
# Module: Mesh
# Part: beam
mdb.models['coh-els'].parts['beam'].setMeshControls(elemShape=QUAD, regions=
    mdb.models['coh-els'].parts['beam'].faces.findAt(((L1/3, t1/4, 0.0), (
    0.0, 0.0, 1.0)), ), technique=STRUCTURED)
# plane stress
mdb.models['coh-els'].parts['beam'].setElementType(elemTypes=(ElemType(
    elemCode=CPS4I, elemLibrary=STANDARD), ElemType(elemCode=CPS3, 
    elemLibrary=STANDARD)), regions=(
    mdb.models['coh-els'].parts['beam'].faces.findAt(((L1/3, t1/3, 0.0), (
    0.0, 0.0, 1.0)), ), ))
# seeds bulk
mdb.models['coh-els'].parts['beam'].seedEdgeByNumber(constraint=FINER, edges=
    mdb.models['coh-els'].parts['beam'].edges.findAt(((L1/4, t1, 0.0), ), ), 
    number=neL1)#neL1=400/100*L1 #w/L1 in [mm], L1 was 100 mm.
# mdb.models['coh-els'].parts['beam'].seedEdgeByNumber(constraint=FINER, edges=
    # mdb.models['coh-els'].parts['beam'].edges.findAt(((0.0, t1/4, 0.0), ), ), 
    # number=neY)# number of elements thru thickness
mdb.models['coh-els'].parts['beam'].seedEdgeByBias(biasMethod=SINGLE, 
    constraint=FINER, end1Edges=
    mdb.models['coh-els'].parts['beam'].edges.findAt(((0.0, t1/2, 0.0), ), ), 
    number=t1Seeds, ratio=t1Bias)# 0.65=>t1/2?
mdb.models['coh-els'].parts['beam'].generateMesh()
# Part: adhesive
mdb.models['coh-els'].parts['adhesive'].setMeshControls(elemShape=QUAD, 
    regions=mdb.models['coh-els'].parts['adhesive'].faces.findAt(((La/3, 
    ta/3, 0.0), (0.0, 0.0, 1.0)), ), technique=SWEEP)
mdb.models['coh-els'].parts['adhesive'].setSweepPath(edge=
    mdb.models['coh-els'].parts['adhesive'].edges.findAt((La, ta/2, 0.0), ),
    region=mdb.models['coh-els'].parts['adhesive'].faces.findAt((La/3, 
    ta/3, 0.0), (0.0, 0.0, 1.0)), sense=REVERSE)
mdb.models['coh-els'].parts['adhesive'].setElementType(elemTypes=(ElemType(
    elemCode=COH2D4, elemLibrary=STANDARD, viscosity=1.0E-05), ElemType(
    elemCode=UNKNOWN_TRI, elemLibrary=STANDARD)), regions=(
    mdb.models['coh-els'].parts['adhesive'].faces.findAt(((La/3, ta/3, 
    0.0), (0.0, 0.0, 1.0)), ), ))
# seeds adhesive
mdb.models['coh-els'].parts['adhesive'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['coh-els'].parts['adhesive'].edges.findAt(((La/2, ta, 
    0.0), ), ), number=neLa)#neLa=280/70*La #w/La in [mm], La was 70 mm.
mdb.models['coh-els'].parts['adhesive'].seedEdgeByNumber(constraint=FINER, 
    edges=mdb.models['coh-els'].parts['adhesive'].edges.findAt(((0.0, ta/4, 
    0.0), ), ), number=1)
mdb.models['coh-els'].parts['adhesive'].generateMesh()
# Module: Interaction
mdb.models['coh-els'].Tie(adjust=ON, master=
    mdb.models['coh-els'].rootAssembly.surfaces['top'], name='top', 
    positionTolerance=position_tolerance, positionToleranceMethod=SPECIFIED, slave=
    mdb.models['coh-els'].rootAssembly.surfaces['coh-top'], thickness=ON, 
    tieRotations=ON)
mdb.models['coh-els'].Tie(adjust=ON, master=
    mdb.models['coh-els'].rootAssembly.surfaces['bot'], name='bot', 
    positionTolerance=position_tolerance, positionToleranceMethod=SPECIFIED, slave=
    mdb.models['coh-els'].rootAssembly.surfaces['coh-bot'], thickness=ON, 
    tieRotations=ON)
# Module: Load
mdb.models['coh-els'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'topLoad', region=mdb.models['coh-els'].rootAssembly.sets['topLoad'], u1=0.0, u2=
    u2target, ur3=UNSET)#new top
mdb.models['coh-els'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'bot', region=mdb.models['coh-els'].rootAssembly.sets['bot'], u1=0.0, u2=
    -u2target, ur3=UNSET)# minus
# Module: Job
Job = mdb.Job(atTime=None, contactPrint=OFF, description='', echoPrint=OFF, 
    explicitPrecision=SINGLE, getMemoryFromAnalysis=True, historyPrint=OFF, 
    memory=90, memoryUnits=PERCENTAGE, model='coh-els', modelPrint=OFF, 
    multiprocessingMode=DEFAULT, name='DCBCZMparams', nodalOutputPrecision=SINGLE, 
    numCpus=8, numDomains=8, numGPUs=0, queue=None, resultsFormat=ODB, 
    scratch='', type=ANALYSIS, userSubroutine='', waitHours=0, waitMinutes=0)
mdb.saveAs('DCBCZMparams.cae')   #save the model

# execution starts here
Job.submit(consistencyChecking=OFF)
Job.waitForCompletion()

# Postprocessing starts here. (c) 2021 Ever Barbero
# calculate the error at experimental points, COD=2*u2
from odbAccess import *
import numpy
#
# Cabello's Araldite High
u2Exp=[0,0.099,0.28,0.493,0.757,1.086,1.431,1.546,1.711,1.859,2.072,2.336,2.484,2.615,2.796,2.993,3.125,3.257,3.437,3.651,3.832,4.046,4.26,4.408,4.638,4.852,5.066,5.247,5.493,5.707,5.954,6.217,6.431,6.743,7.023,7.27,7.533,7.796,8.125,8.372,8.651,8.914,9.194,9.474,9.786,9.942];# COD
p2Exp=[0,49.105,112.532,204.604,298.721,380.563,486.957,511.509,536.061,552.43,558.568,548.338,527.877,509.463,482.864,462.404,441.944,413.299,390.793,364.194,339.642,329.412,319.182,306.905,300.767,290.537,282.353,280.307,276.215,265.985,259.847,255.754,247.57,249.616,245.524,241.432,237.34,227.11,227.11,225.064,216.88,214.834,208.696,202.558,200.512,200.512];# P
# Cabello's Araldite Low (do not overwrite previous data)
u2Exp_low=[0,0.115,0.312,0.559,0.822,1.003,1.184,1.398,1.595,1.793,2.007,2.138,2.27,2.368,2.434,2.533,2.664,2.747,2.911,3.059,3.191,3.355,3.503,3.668,3.849,4.062,4.243,4.49,4.72,4.901,5.148,5.345,5.559,5.789,6.086,6.283,6.513,6.743,6.957,7.204,7.451,7.73,7.993,8.257,8.52,8.816,9.128,9.375,9.704,9.91];
p2Exp_low=[0,53.197,130.946,233.248,319.182,368.286,417.391,456.266,484.91,499.233,482.864,466.496,450.128,433.76,411.253,388.747,364.194,345.78,335.55,325.32,315.09,306.905,302.813,290.537,282.353,268.031,263.939,253.708,245.524,245.524,245.524,237.34,231.202,229.156,220.972,220.972,216.88,206.65,202.558,196.419,188.235,188.235,182.097,180.051,178.005,178.005,171.867,173.913,171.867,171.867];
# Select data to fit with Matlab fminsearch
# u2Exp = u2Exp_low
# p2Exp = p2Exp_low
#
# Calculate the error. All calculations done using COD=2*u2 from FEA
odb = openOdb(path='DCBCZMparams.odb',readOnly=True)
step = odb.steps['Step-1']
# find region name with ">>> print step.historyRegions"
region = step.historyRegions['Node BEAM-1.1443']# mesh dependent!
# store u2, rf2, to lists
u2Data = region.historyOutputs['U2'].data
rf2Data = region.historyOutputs['RF2'].data
# find the peak load
rf2max = 0  #initialize the max. load
u2 = []     #initialize a list
rf2 = []    #initialize a list
u2AtPeekLoad = []   #initialize a list
# build the simulation results array
for i in range(len(u2Data)):#loop over simulation points
    u2.append(2*u2Data[i][1])   # COD: u2 = 2*U2
    rf2.append(rf2Data[i][1])   # Load: rf2 = RF2
    # print i, u2[i], rf2[i]
    if rf2[i] > rf2max:
        imax = i
        rf2max = rf2[i] #peek load
        u2AtPeekLoad = u2[i]

print ('increment %g, u2AtPeekLoad %g, rf2max %g, sim pts %g'%(imax, u2AtPeekLoad, rf2max, len(rf2Data)-1))
# Calculate area under experimental curve
areaExp = 0
for i in range(len(u2Exp)):# loop over experimental points
    if i == 0:
        continue # skip i=0
    if u2Exp[i] > 2*u2target:
        break # skip everything
    deltau2 = u2Exp[i] - u2Exp[i-1] # current minus previous u2Exp
    # experimental area
    areaExp = areaExp + deltau2 * (p2Exp[i-1] + p2Exp[i])/2 

# Calculate area under simulation curve
areaSim = 0
for i in range(len(u2)):# loop over simulation points
    if i == 0:
        continue # skip i=0
    if u2[i] > 2*u2target:
        break # skip everything
    deltau2 = u2[i] - u2[i-1] # current minus previous u2
    # simulation area
    areaSim = areaSim + deltau2 * (rf2[i-1] + rf2[i])/2 

# calculate error
error = 100*abs(areaSim-areaExp)/areaExp
print "areaExp=",areaExp, "areaSim=",areaSim, " %error=",error
#
simulation_data = open('simulation_data.txt','w')
for i in range(len(rf2Data)):#loop over simulation points
    simulation_data.write('%g %g\n' % (u2[i], rf2[i]))# COD, rf2

simulation_data.close()# to plot later
cost = open('cost.txt','w')# overwrite
cost.write('%10.4e \n' % error)# to be read by Matlab
cost.close()
log = open('log.txt','a+')
minutes = (time.time()-start_time)/60
log.write("Kn={} tno={} Gnc={} a0={} rangeCOD={}\n".format(Kn, tno, Gnc, a0, 2*u2target))
log.write("u2(p2max)={} p2max={} error={} time={}\n".format(u2AtPeekLoad, rf2max, error, minutes))
log.close()# useful info
odb.close()
# end
