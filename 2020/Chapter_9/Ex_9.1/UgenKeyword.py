def UgenKeyword(ModelParameters):
    # for original DDM
    # Function to define the UGENS keywords to insert in the .inp file from within CAE
    # PROPERTIES=3+9*(Number of laminas in the lower part)
    # VARIABLES =3*(Number of laminas in the lower part)
    # First line: thickness of the whole laminate
    # Second and successive lines: the properties, in this order:
    # GIc, GIIc, dummy, E1 (lamina 1), E2 (lamina 1), G12 (lamina 1), nu12 (lamina 1), nu23 (lamina 1),
    # CTE1 (lamina 1), CTE2 (lamina 1), Angle (lamina 1), Thickness (lamina 1), E1 (lamina 2), E2 (lamina 2), G12 (lamina 2), nu12 (lamina 2),
    # nu23 (lamina 2), CTE1 (lamina 2), CTE2 (lamina 2), Angle (lamina 2), Thickness (lamina 2), ...,
    # ..., Thickness (lamina n)
    # 8 floats per line
    
    NL = len(ModelParameters['Lss'])
    
    WholeLaminateThickness = 2.*sum([x[0] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])
    
    Out  = '*Shell General Section, elset=WholeLaminate, USER, PROPERTIES='+str(3+9*NL)+', VARIABLES='+str(3*NL)+'\n'
    Out += str(WholeLaminateThickness)+'\n'
    Out += str(ModelParameters['GIc'])+','+str(ModelParameters['GIIc'])+','+str(ModelParameters['dummy'])+','
    
    Sequence = [0 for x in range(9*NL)]
    for i in range(NL):
        L = ModelParameters['Lss'][i]
        
        Sequence[9*i  ] = ModelParameters['E1'  ]
        Sequence[9*i+1] = ModelParameters['E2'  ]
        Sequence[9*i+2] = ModelParameters['G12' ]
        Sequence[9*i+3] = ModelParameters['Nu12']
        Sequence[9*i+4] = ModelParameters['Nu23']
        Sequence[9*i+5] = ModelParameters['Cte1']
        Sequence[9*i+6] = ModelParameters['Cte2']
        Sequence[9*i+7] = L[1]
        Sequence[9*i+8] = float(ModelParameters['tk'])*L[0]
    
    for i in range(9*NL):
        if ((i+3) % 8 == 0):
            Out += '\n'
        Out += str(Sequence[i])+','
    
    Out  = Out[:-1]
    Out += '\n'
    Out += '*Transverse Shear Stiffness\n'# add 'Stiffness' in Abaqus 2020
    # H matrix H44, H55, H45
    Out += '1,1,0'
    
    return Out

def InitialConditionsKeyword(ModelParameters):
    # Function to define the Initial Conditions keywords for the UGENS
    # to insert in the .inp file from within CAE
    # INITIAL STATE VALUES (VARIABLES)=3*(Number of laminas in the lower part)
    # 8 floats per line
    
    NL = len(ModelParameters['Lss'])
    
    WholeLaminateThickness = 2.*sum([x[0] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])
    
    Out  = '*Initial Conditions, type=SOLUTION'+'\n'+'Laminate-1.WholeLaminate,'
    
    Sequence = [0 for x in range(3*NL+1)]
    
    for i in range(NL):
        L = ModelParameters['Lss'][i]
        Sequence[3*i  ] = ModelParameters['InitialCrackDensity']
        Sequence[3*i+1] = '0'
        Sequence[3*i+2] = '0'
    
    for i in range(3*NL):
        if ((i+1) % 8 == 0):
            Out += '\n'
        Out += str(Sequence[i])+','
    
    Out  = Out[:-1]
    Out += '\n'
    
    return Out