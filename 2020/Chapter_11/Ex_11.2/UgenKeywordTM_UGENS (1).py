def UgenKeywordTM_UGENS(ModelParameters):
    # Function to define the UGENS keywords to insert in the .inp file from within CAE
    # Thickness of the whole laminate is already defined in Ex-9-2-TM
    # Second and successive lines: 45+2*NL properties, in this order:
    # E1a, E1b, E1c, E2a, E2b, E2c, G12a, G12b, ...
    # G12c, Nu12a, Nu12b, Nu12c, Nu23a, Nu23b, Nu23b, CTE1a, ...
    # CTE1b, CTE1c, CTE1d, CTE2a, CTE2b, CTE2c, CTE2d, GIcA, ...
    # GIcB, GIcC, TGImax, TGImin, GIIcA, GIIcB, GIIcC, TGIImax, ...
    # TGIImin, SFT, Temax, Temin, Ttmax, Ttmin, F1t, F1c, ...
    # F2c, mWeibull, BetaGIc, BetaGIIc, Cycles, ... fill with: Angle (lamina 1), Thickness (lamina 1),...
    # ...., Thickness (lamina n)
    # IMPORTANT: 8 floats per line !!!!!
    
    NL = len(ModelParameters['Lss'])
    # note: 45 + 2*NL material properties 
    PROPERTIES = 45 + 2*NL  
    # note: (3 state variables + 3 damages + 3 stresses + 3 Energies) per layer
    # There VARIABLES per lamina are:
    #  LAMINA 1:
    #  VAR(1) = CrackDensity Lamina 1
    #  VAR(2) = tensile hardening threshold g1t Lamina 1
    #  VAR(3) = compression hardening threshold g1c Lamina 1
    #  VAR(4) = D1 Lamina 1
    #  VAR(5) = D2 Lamina 1
    #  VAR(6) = D6 Lamina 1
    #  VAR(7) = sigma_1 Lamina 1
    #  VAR(8) = sigma_2 Lamina 1
    #  VAR(9) = sigma_6 Lamina 1
    #  VAR(10) = g(lambda) Lamina 1
    #  VAR(11) = GI(lambda,epsilon) Lamina 1
    #  VAR(12) = GII(lambda,epsilon) Lamina 1
    #  LAMINA 2:
    #  VAR(13) = CrackDensity Lamina 2
    #  VAR(14) = tensile hardening threshold g1t Lamina 2
    #  VAR(15) = compression hardening threshold g1c Lamina 2
    #  ......
    #  ......
    VARIABLES = 12*NL

    WholeLaminateThickness = 2.*sum([x[1] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])
    # LSS (angle, thickness) ordered
    Sequence = [0 for x in range(2*NL)]
    for i in range(NL):
        L = ModelParameters['Lss'][i]
        Sequence[2*i  ]  = L[0]
        Sequence[2*i+1]  = float(ModelParameters['tk'])*L[1]
    
    # Elastic properties
    Out = str(ModelParameters['E1a'])+','\
        +str(ModelParameters['E1b'])+','\
        +str(ModelParameters['E1c'])+','\
        +str(ModelParameters['E2a'])+','\
        +str(ModelParameters['E2b'])+','\
        +str(ModelParameters['E2c'])+','\
        +str(ModelParameters['G12a'])+','\
        +str(ModelParameters['G12b'])+'\n'      
    Out += str(ModelParameters['G12c'])+','\
        +str(ModelParameters['Nu12a'])+','\
        +str(ModelParameters['Nu12b'])+','\
        +str(ModelParameters['Nu12c'])+','\
        +str(ModelParameters['Nu23a'])+','\
        +str(ModelParameters['Nu23b'])+','\
        +str(ModelParameters['Nu23c'])+','\
        +str(ModelParameters['CTE1a'])+'\n'
    Out += str(ModelParameters['CTE1b'])+','\
        +str(ModelParameters['CTE1c'])+','\
        +str(ModelParameters['CTE1d'])+','\
        +str(ModelParameters['CTE2a'])+','\
        +str(ModelParameters['CTE2b'])+','\
        +str(ModelParameters['CTE2c'])+','\
        +str(ModelParameters['CTE2d'])+','\
        +str(ModelParameters['GIcA'])+'\n'
    Out += str(ModelParameters['GIcB'])+','\
        +str(ModelParameters['GIcC'])+','\
        +str(ModelParameters['TGImax'])+','\
        +str(ModelParameters['TGImin'])+','\
        +str(ModelParameters['GIIcA'])+','\
        +str(ModelParameters['GIIcB'])+','\
        +str(ModelParameters['GIIcC'])+','\
        +str(ModelParameters['TGIImax'])+'\n'
    Out += str(ModelParameters['TGIImin'])+','\
        +str(ModelParameters['SFT'])+','\
        +str(ModelParameters['Temax'])+','\
        +str(ModelParameters['Temin'])+','\
        +str(ModelParameters['Ttmax'])+','\
        +str(ModelParameters['Ttmin'])+','\
        +str(ModelParameters['F1t'])+','\
        +str(ModelParameters['F1c'])+'\n'
    Out += str(ModelParameters['F2c'])+','\
        +str(ModelParameters['mWeibull'])+','\
        +str(ModelParameters['BetaGIc'])+','\
        +str(ModelParameters['BetaGIIc'])+','\
        +str(ModelParameters['Cycles'])+','\

    # more floats 
    ### THIS NUMBER MUST BE EQUAL TO THE TOTAL str 
    # from last Out += ... In this case 5 TIMES 
    # !!!!!!!!!!! IMPORTANT !!!!!!!!!!!
    # DO NOT TOUCH nWritten unless the previous 
    # code has been modified
    nWritten = 5    # number of output before Out

    # Organize the Line vector to fill with angle, 
    # lamina in INPUT file of Abaqus
    j = 2*NL
    array = 8 - nWritten 
    if (j <= array):
        Line1=[]
        for i in range(j):
            Line1.append(Sequence[i])
    elif (j > array and j < (array+8)): 
        Line1=[]
        Line2=[]
        for i in range(j):
            if ( i < array):
                Line1.append(Sequence[i]) 
            else: 
                Line2.append(Sequence[i])
    else:
        Line1=[]
        Line2=[]
        Line3=[]
        for i in range(j):
            if ( i < array):
                Line1.append(Sequence[i]) 
            elif ( i > array and i < (array + 9)): 
                Line2.append(Sequence[i])
            else:
                Line3.append(Sequence[i]) 
    #        Out += '\n'
    
    #Write the LSS in input file
    if (j <= array): 
        Out += str(Line1)[1:-1]
    elif (j > array and j < (array+8)): 
        Out += str(Line1)[1:-1] + '\n'
        Out += str(Line2)[1:-1]
    else:
        Out += str(Line1)[1:-1] + '\n'
        Out += str(Line2)[1:-1] + '\n'
        Out += str(Line3)[1:-1]
    
    return Out

def InitialConditionsKeyword(ModelParameters):
    # Function to define the Initial Conditions keywords for the UGENS
    # to insert in the .inp file from within CAE
    # INITIAL STATE VALUES (VARIABLES)=10*(Number of laminas in the lower part)
    # CrackDensity
    # g1t
    # g2t
    # D1
    # D2
    # D3
    # sigma_1
    # sigma_2
    # sigma_3
    # g function
    # GI
    # GII
    # 8 floats per line !!!!!
    
    NL = len(ModelParameters['Lss'])
    
    WholeLaminateThickness = 2.*sum([x[1] for x in ModelParameters['Lss']])*float(ModelParameters['tk'])
    
    Out  = '*Initial Conditions, type=SOLUTION'+'\n'+'Laminate-1.WholeLaminate,'
    
    Sequence = [0 for x in range(10*NL+1)]
    
    for i in range(NL):
        L = ModelParameters['Lss'][i]
        Sequence[10*i  ] = ModelParameters['InitialCrackDensity']
        Sequence[10*i+1] = '0'
        Sequence[10*i+2] = '0'
        Sequence[10*i+3] = '0'
        Sequence[10*i+4] = '0'
        Sequence[10*i+5] = '0'
        Sequence[10*i+6] = '0'
        Sequence[10*i+7] = '0'
        Sequence[10*i+8] = '0'
        Sequence[10*i+9] = '0'
        Sequence[10*i+10] = '0'
        Sequence[10*i+11] = '0'
        Sequence[10*i+12] = '0'
    
    for i in range(10*NL):
        if ((i+1) % 8 == 0):
            Out += '\n'
        Out += str(Sequence[i])+','
    
    Out  = Out[:-1]
    Out += '\n'
    
    return Out
