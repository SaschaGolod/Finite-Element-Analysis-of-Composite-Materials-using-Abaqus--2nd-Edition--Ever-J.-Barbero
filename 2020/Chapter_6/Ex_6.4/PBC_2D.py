"""
Created on Mon Sep 12 16:24:14 2011
'#############################################'
'# Periodic boundary conditions - 2D         #'
'#       Created by:                         #'
'#       Ever J. Barbero, PhD.               #'
'#       Fritz Andres Campo Schickler, PhD.  #'
'#       West Virginia University - 2011     #'
'#############################################'
@author: fritz.campo

This code creates the required equation constrains in Abacus to replicate Periodic Boundary
Conditions.

Based on: 
    Ever J. Barbero. Finite Element Analysis of Composite Materials, 
    CRC Press, Boca Raton, FL, 2007. ISBN: 1-4200-5433-3.
    
1) The function requires a single part, named 'Part-1' subdivided, if desired (Partitioned).  
2) The part has to have predefined (as Geometry) the following sets:
    Face1:  This is the right face
    Face2:  This is the top face
    Face3:  This is the left face
    Face4:  This is the bottom face
    Vertex1:  This is the vertex intersection between Face1 and Face2
    Vertex2:  This is the vertex intersection between Face 2 and Face3
    Vertex3:  This is the vertex intersection between Face 3 and Face4
    Vertex4:  This is the vertex intersection between Face 4 and Face1

3) The part MUST be meshed with equal number of nodes at equivalent Faces.

4) Afterwards,  Create a 'Job-1'
5) Run 'srecover2D.py' to find the effective strains/stresses
"""

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

session.journalOptions.setValues(recoverGeometry = COORDINATE)
# next line commented for Ex_6.4 and Ex_7.8-py
# strain = [0.0, 0.0, 1.0/2.0]

Part = mdb.models['Model-1'].parts['Part-1']
Face1 = Part.sets['Face1']
Face2 = Part.sets['Face2']
Face3 = Part.sets['Face3']
Face4 = Part.sets['Face4']
Vertex1 = Part.sets['Vertex1']
Vertex2 = Part.sets['Vertex2']
Vertex3 = Part.sets['Vertex3']
Vertex4 = Part.sets['Vertex4']

# RP, to write the CE's 
Part.ReferencePoint(point=(0.0, 0.0, 0.0))
MasterIndex = mdb.models['Model-1'].parts['Part-1'].features['RP']
Part.Set(name='MasterNode', referencePoints=(
    Part.referencePoints[MasterIndex.id], ))

# U1=1, to write the CE's
mdb.models['Model-1'].DisplacementBC(amplitude=UNSET, createStepName='Step-1', 
    distributionType=UNIFORM, fieldName='', fixed=OFF, localCsys=None, name=
    'BC-1', region=Region(referencePoints=(
    mdb.models['Model-1'].rootAssembly.instances['Part-1-1'].referencePoints[MasterIndex.id], 
    )), u1=1.0, u2=UNSET, ur3=UNSET)    
    
def TakeVertexOut(face):
    face.pop(0)
    face.pop(-1)
    return face

def SortListOfNodes(face,coordinate):
    newlist = []
    oldlist = []
    for ii in range(len(face.nodes)):
        oldlist.append( face.nodes[ii].coordinates[coordinate])
    
    orderedlist = sorted(oldlist)
    for ii in range(len(oldlist)):
        vecindex = oldlist.index(orderedlist[ii])
        #newlist.append(oldlist[vecindex])
        newlist.append(face.nodes[vecindex].label-1)
    
    return newlist

# Construction Pairs of nodes
# Face 1 and 3 (right-left)
ParingFaces13 = []
ParingFaces13.append(TakeVertexOut(SortListOfNodes(Face1,1)))
ParingFaces13.append(TakeVertexOut(SortListOfNodes(Face3,1)))
# Face 2 and 4 (top-bottom)
ParingFaces24 = []
ParingFaces24.append(TakeVertexOut(SortListOfNodes(Face2,0)))
ParingFaces24.append(TakeVertexOut(SortListOfNodes(Face4,0)))

# Writting Constrain equations 
# For the Vertices

# Master V1 (Contained in 1 and 3)
mdb.models['Model-1'].Equation(name='ConstraintV1-V3-1', terms=((1.0, 
    'Part-1-1.Vertex1', 1),  (-1.0, 'Part-1-1.Vertex3', 1),
    (-strain[0]*(Vertex1.nodes[-1].coordinates[0]-Vertex3.nodes[-1].coordinates[0]) + 
    -strain[2]/2.*(Vertex1.nodes[-1].coordinates[1]-Vertex3.nodes[-1].coordinates[1]),
    'Part-1-1.MasterNode', 1)))
mdb.models['Model-1'].Equation(name='ConstraintV1-V3-2', terms=((1.0, 
    'Part-1-1.Vertex1', 2),(-1.0, 'Part-1-1.Vertex3', 2), 
    (-strain[2]/2.*(Vertex1.nodes[-1].coordinates[0]-Vertex3.nodes[-1].coordinates[0]) + 
    -strain[1]*(Vertex1.nodes[-1].coordinates[1]-Vertex3.nodes[-1].coordinates[1]),
    'Part-1-1.MasterNode', 1)))
# Master V2 (Contained in 2 and 4)
mdb.models['Model-1'].Equation(name='ConstraintV2-V4-1', terms=((1.0, 
    'Part-1-1.Vertex2', 1), (-1.0, 'Part-1-1.Vertex4', 1), 
    (strain[2]/2.*(Vertex4.nodes[-1].coordinates[1]-Vertex2.nodes[-1].coordinates[1]) + 
    strain[0]*(Vertex4.nodes[-1].coordinates[0]-Vertex2.nodes[-1].coordinates[0]),
    'Part-1-1.MasterNode', 1)))
mdb.models['Model-1'].Equation(name='ConstraintV2-V4-2', terms=((1.0, 
    'Part-1-1.Vertex2', 2), (-1.0, 'Part-1-1.Vertex4', 2), 
    (-strain[1]*(Vertex2.nodes[-1].coordinates[1]-Vertex4.nodes[-1].coordinates[1])  
    -strain[2]/2.*(Vertex2.nodes[-1].coordinates[0]-Vertex4.nodes[-1].coordinates[0]),
    'Part-1-1.MasterNode', 1)))
    
# For the Edges (Between pairs of nodes)
for ii in range(len(ParingFaces13[0])):
    mdb.models['Model-1'].parts['Part-1'].Set(name='MasterFace13-'+str(ii), nodes=(
        mdb.models['Model-1'].parts['Part-1'].nodes[ParingFaces13[0][ii]:ParingFaces13[0][ii]+1],))
    mdb.models['Model-1'].parts['Part-1'].Set(name='SlaveFace13-'+str(ii), nodes=(
        mdb.models['Model-1'].parts['Part-1'].nodes[ParingFaces13[1][ii]:ParingFaces13[1][ii]+1],))   
    # (6.13, i=1)
    mdb.models['Model-1'].Equation(name='Constraint13-1-'+str(ii), terms=((1.0, 
        'Part-1-1.MasterFace13-'+str(ii), 1), (-1.0, 'Part-1-1.SlaveFace13-'+str(ii), 1), (-strain[0]*
        (Part.nodes[ParingFaces13[0][ii]].coordinates[0]-Part.nodes[ParingFaces13[1][ii]].coordinates[0]), 
        'Part-1-1.MasterNode', 1)))
    # (6.13, i=2)
    mdb.models['Model-1'].Equation(name='Constraint13-2-'+str(ii), terms=((1.0, 
        'Part-1-1.MasterFace13-'+str(ii), 2), (-1.0, 'Part-1-1.SlaveFace13-'+str(ii), 2), (-strain[2]/2.*
        (Part.nodes[ParingFaces13[0][ii]].coordinates[0]-Part.nodes[ParingFaces13[1][ii]].coordinates[0]), 
        'Part-1-1.MasterNode', 1)))

for ii in range(len(ParingFaces24[0])):
    mdb.models['Model-1'].parts['Part-1'].Set(name='MasterFace24-'+str(ii), nodes=(
        mdb.models['Model-1'].parts['Part-1'].nodes[ParingFaces24[0][ii]:ParingFaces24[0][ii]+1],))
    mdb.models['Model-1'].parts['Part-1'].Set(name='SlaveFace24-'+str(ii), nodes=(
        mdb.models['Model-1'].parts['Part-1'].nodes[ParingFaces24[1][ii]:ParingFaces24[1][ii]+1],))    
    # (6.14, i=1)
    mdb.models['Model-1'].Equation(name='Constraint24-1-'+str(ii), terms=((1.0, 
        'Part-1-1.MasterFace24-'+str(ii), 1), (-1.0, 'Part-1-1.SlaveFace24-'+str(ii), 1), (-strain[2]/2.*
        (Part.nodes[ParingFaces24[0][ii]].coordinates[1]-Part.nodes[ParingFaces24[1][ii]].coordinates[1]), 
        'Part-1-1.MasterNode', 1)))
    # (6.14, i=2)
    mdb.models['Model-1'].Equation(name='Constraint24-2-'+str(ii), terms=((1.0, 
        'Part-1-1.MasterFace24-'+str(ii), 2), (-1.0, 'Part-1-1.SlaveFace24-'+str(ii), 2), (-strain[1]*
        (Part.nodes[ParingFaces24[0][ii]].coordinates[1]-Part.nodes[ParingFaces24[1][ii]].coordinates[1]), 
        'Part-1-1.MasterNode', 1)))        

mdb.models['Model-1'].rootAssembly.regenerate()
