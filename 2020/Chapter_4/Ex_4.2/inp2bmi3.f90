    program inp2bmi3

    implicit none
    integer NNodesDim, NElementsDim, NNsetsDim, NBoundariesDim
    parameter (NNodesDim=1000, NElementsDim=1000, NNsetsDim=100, NBoundariesDim=100)

    integer inp/1/, out/6/, dat/3/, abq/7/
    integer i, j, k, k1, step, targetvalue, loc, DofVector(6) 
    integer ElemConnect(NElementsDim,9), Nset(NNsetsDim,NNodesDim), NsetNumber, NsetNumberMax, CloadNumber
    character*80 rec, auxrec, rectmp, NsetName(NNsetsDim), CloadName(NNsetsDim), NsetNameLocal
    integer NodeXyz(NNodesDim,3), NsetLength(NNsetsDim)
    real*8 K11, K12, K22, ABD(6,6), iLoad
    integer BoundaryNumber, idof, jdof, NNOdes, NElements
    character*80 BoundaryName(NBoundariesDim)
    integer Node, iel, inod
    real*8 x,y,z
    integer PertMode/0/, PertNode/0/, PertDof/0/
    integer NumberOfMaterials/1/, MaterialPerElement(NElementsDim)
    CHARACTER*4 NAME/"BMI3"/

    MaterialPerElement = 1  !for now restricted to one material only

    open(unit=inp,file="Job-1.inp",status="old",mode="read",err=901)    !Abaqus/CAE generated file
    open(unit=out,file=NAME//".inp",status="unknown",mode="write",err=902)!cannot import this file to CAE
    open(unit=dat,file=NAME//".dat",status="unknown",mode="write",err=902)!material properties for BMI3
    open(unit=abq,file="ABQ.inp",status="unknown",mode="write",err=902) !can import this file to CAE
    
    do  !find Heading
        read(inp,"(A)",end=903) rec
        if(rec(1:8).eq."*Heading") exit
    enddo
    write(out,"(80A)") "*HEADING";     write(abq,"(80A)") "*HEADING"
    read(inp,"(A)",end=903) rec
    write(out,"(80A)") rec;     write(abq,"(80A)") rec

    rewind(inp)
    do  !find Nodes
        read(inp,"(A)",end=903) rec
        if(rec(1:5).eq."*Node") exit
    enddo
    write(out,"(80A)") "*NODE, SYSTEM=R";       write(abq,"(80A)") "*NODE, SYSTEM=R"
    
    type *, "assuming: Node list uninterrupted by any other *card"
    type *, "assuming: Abaqus/CAE gives the nodes ordered and no one missing"
    NNodes = 0
    do  !read nodes
        read(inp,"(A)",end=903) rec
        if(rec(1:1).eq."*") exit
        NNodes = NNodes + 1
        read(rec,*) inod, NodeXyz(inod,:)
        write(out,"(3(I5,','),I5)") inod, NodeXyz(inod,:)
        write(abq,"(3(I5,','),I5)") inod, NodeXyz(inod,:)
    enddo
    if (inod.ne.NNodes) pause "error: missing or unordered nodes detected"; 

    backspace(inp)
    do  !find Elements
        read(inp,"(A)",end=903) rec
        if(rec(1:8).eq."*Element") exit
        pause "error: expected keyword not found. aborting execution."; 
    enddo
    rectmp = rec    !hold writing until the 9th nodes are generated and written    
    
    type *, "assuming: Element list uninterrupted by any other *card"
    type *, "assuming: Abaqus/CAE gives the elements ordered and no one missing"
    NElements = 0
    do  !read elements
        read(inp,"(A)",end=903) rec
        if(rec(1:1).eq."*") exit
        NElements = NElements + 1
        read(rec,*) iel, ElemConnect(iel,1:8)
        !generate the 9th node
	    NNodes = NNodes + 1
	    x = 0
	    y = 0
	    z = 0
	    do j = 1,4
	      Node = ElemConnect(iel,j)
	      x = x + NodeXyz(Node,1)
	      y = y + NodeXyz(Node,2)
	      z = z + NodeXyz(Node,3)
	    enddo
	    x = x/4
	    y = y/4
	    z = z/4
	    NodeXyz(NNodes,1) = x
	    NodeXyz(NNodes,2) = y
	    NodeXyz(NNodes,3) = z
	    ElemConnect(iel,9) = NNodes
        write(out,"(3(I5,','),I5)") NNodes, NodeXyz(NNodes,:)
        write(abq,"(3(I5,','),I5)") NNodes, NodeXyz(NNodes,:)
    enddo
    if (iel.ne.NElements) pause "error: missing or unordered elements detected"; 

    !now that all the nodes are written, write the element connectivity
    write(out,"(80A)") "*ELEMENT, TYPE=S8R5, ELSET=BMI3"
    write(abq,"(80A)") "*ELEMENT, TYPE=S8R5, ELSET=BMI3"
    do iel = 1, NElements
        write(out,"(9(I5',')I5)") iel, ElemConnect(iel,:)
        write(abq,"(8(I5',')I5)") iel, ElemConnect(iel,1:8)
    enddo
    
    rewind(inp) !2020 !find Nsets and rewrite them
    do          !2020 discard Nsets and Elsets defined inside the Instance, we want only those used for BCs
        read(inp,"(A)",end=903) rec
        if(rec(1:13).eq."*End Instance") exit
    enddo
    NsetNumber = 0
    do  !find them all
        do  !find Nset
            read(inp,"(A)",end=801) rec
            if(rec(1:5).eq."*Nset") exit !found one
        enddo
        NsetNumber = NsetNumber + 1 !count it
        auxrec = rec(index(rec,"nset=")+5:) 
        NsetName(NsetNumber) = auxrec(index(auxrec,"_")+1:index(auxrec,",")-1) !eliminate underscore, but there is no underscore in 2020?
        !write(out,"(80A)") "*NSET, NSET=",NsetName(NsetNumber) !not needed by Job based on input file
        !write(abq,"(80A)") "*NSET, NSET=",NsetName(NsetNumber) !only needs sets for BCs
        
        if(index(rec,"generate").ne.0) then !generate. 3 numbers expected
            read(inp,*,end=904) i, j, step
            k1 = 0
            do k = i,j,step
                k1 = k1 + 1
                Nset(NsetNumber,k1) = k
            enddo
            NsetLength(NsetNumber) = k1
        else    !not generate. list of nodes expected
            Nset(NsetNumber,:) = 0  !initialize to zero
            i = 0
            do  !read Nset until non numeric character is found (*)
                read(inp,*,err=81,end=81) (Nset(NsetNumber,i+j),j=1,16)
                i = i + 16
            enddo
     81     continue        
            backspace(inp) !before line read in error
            NsetLength(NsetNumber) = i+j-1
        endif
        !write(out,"(15(I5',')I5)") Nset(NsetNumber,1:NsetLength(NsetNumber))
        !write(abq,"(15(I5',')I5)") Nset(NsetNumber,1:NsetLength(NsetNumber))
    enddo
801 continue
    NsetNumberMax = NsetNumber
        
    rewind(inp)
    do  !find Shell General Section
        read(inp,"(A)",end=903) rec
        if(rec(1:22).eq."*Shell General Section") exit
    enddo
    write(out,"(80A)")  "*SHELL GENERAL SECTION, ELSET=BMI3"
    write(abq,"(80A)")  "*SHELL GENERAL SECTION, ELSET=BMI3"
    
    write(out,"(A)")    "** A11, A12, A22, A16, A26, A66, B11, B12"                         
    write(out,"(A)")    "** B16, D11, B12, B22, B26, D12, D22, B16"                         
    write(out,"(A)")    "** B26, B66, D16, D26, D66"                                                 

    read(inp,*,end=903) ABD(1,1), ABD(1,2), ABD(2,2), ABD(1,3), ABD(2,3), ABD(3,3), ABD(1,4), ABD(2,4)
    read(inp,*,end=903) ABD(3,4), ABD(4,4), ABD(1,5), ABD(2,5), ABD(3,5), ABD(4,5), ABD(5,5), ABD(1,6)
    read(inp,*,end=903) ABD(2,6), ABD(3,6), ABD(4,6), ABD(5,6), ABD(6,6)
    
    write(out,1001) ABD(1,1), ABD(1,2), ABD(2,2), ABD(1,3), ABD(2,3), ABD(3,3), ABD(1,4), ABD(2,4)
    write(out,1001) ABD(3,4), ABD(4,4), ABD(1,5), ABD(2,5), ABD(3,5), ABD(4,5), ABD(5,5), ABD(1,6)
    write(out,1001) ABD(2,6), ABD(3,6), ABD(4,6), ABD(5,6), ABD(6,6)
    
    read(inp,"(A)",end=903) rec; 
    write(out,1003) "*TRANSVERSE SHEAR STIFFNESS","** H44, H55, H45"
    read(inp,*,end=903) K11, K22, K12
    write(out,1002) K11, K22, K12

    write(abq,1001) ABD(1,1), ABD(1,2), ABD(2,2), ABD(1,3), ABD(2,3), ABD(3,3), ABD(1,4), ABD(2,4)
    write(abq,1001) ABD(3,4), ABD(4,4), ABD(1,5), ABD(2,5), ABD(3,5), ABD(4,5), ABD(5,5), ABD(1,6)
    write(abq,1001) ABD(2,6), ABD(3,6), ABD(4,6), ABD(5,6), ABD(6,6)
    
    write(abq,1003) "*TRANSVERSE SHEAR STIFFNESS","** H44, H55, H45"
    write(abq,1002) K11, K22, K12

    rewind(inp)
    print *, "assuming: the Step is defined in just 3 lines" 
    do  !find Step
        read(inp,"(A)",end=903) rec
        if(rec(1:5).eq."*Step") exit !found one
    enddo
    write(out,"(80A)") rec
    write(abq,"(80A)") rec
    read(inp,"(A)",end=903) rec
    write(out,"(80A)") rec
    write(abq,"(80A)") rec
    read(inp,"(A)",end=903) rec
    write(out,"(80A)") rec
    write(abq,"(80A)") rec

    rewind(inp)
    BoundaryNumber = 0
    do
        do  !find Boundary
            read(inp,"(A)",end=802) rec
            if(rec(1:9).eq."*Boundary") exit !found one
        enddo
        BoundaryNumber = BoundaryNumber + 1 !count it
        read(inp,"(A)",end=802) rec
        NsetNameLocal = rec(1:index(rec,",")-1)
        if (index(rec,"PINNED").ne.0) then
            DofVector = (/1,1,1,0,0,0/)
        elseif (index(rec,"ENCASTRE").ne.0) then
            DofVector = (/1,1,1,1,1,1/)
        elseif (index(rec,"XSYMM").ne.0) then
            DofVector = (/1,0,0,0,1,1/) !per Abaqus
        elseif (index(rec,"YSYMM").ne.0) then
            DofVector = (/0,1,0,1,0,1/) !per Abaqus
        elseif (index(rec,"ZSYMM").ne.0) then
            DofVector = (/0,0,1,1,1,0/) !per Abaqus
        elseif (index(rec,"XASYMM").ne.0) then
            DofVector = (/0,1,1,1,0,0/) !per Abaqus
        elseif (index(rec,"YASYMM").ne.0) then
            DofVector = (/1,0,1,0,1,0/) !per Abaqus
        elseif (index(rec,"ZASYMM").ne.0) then
            DofVector = (/1,1,0,0,0,1/) !per Abaqus
        else
            read(rec,*,end=903) NsetNameLocal, idof, jdof
            DofVector = 0
            do j = idof, jdof
                DofVector(j) = 1
            enddo
        endif        
        BoundaryName(BoundaryNumber) = NsetNameLocal(index(NsetNameLocal,"_")+1:)   !eliminate underscore
        if (BoundaryNumber.eq.1) write(out,"(80A)") "*BOUNDARY";     
        write(abq,"(80A)") "*BOUNDARY";
        write(out,"(80A)") "**NSET=", BoundaryName(BoundaryNumber)
        write(abq,"(80A)") "**NSET=", BoundaryName(BoundaryNumber)
        !generate bcs
        k = 1; 
        do 
            if (index(NsetName(k),BoundaryName(BoundaryNumber)).ne.0) exit
            k = k + 1
        enddo
        do i = 1, NsetLength(k)
            do j =1,6
                if (DofVector(j).eq.1) then
                    write(abq,"(I5','I5',,'1PG10.3)") Nset(k,i),j,0.0   !Abaqus
                    !swap dof 4 and 5 for bmi3.f convention. see Raftoyiannis Ph.D. 
                    if (j.eq.4) then
                        write(out,"(I5','I5',,'1PG10.3)") Nset(k,i),5,0.0
                    elseif (j.eq.5) then
                        write(out,"(I5','I5',,'1PG10.3)") Nset(k,i),4,0.0
                    else
                        write(out,"(I5','I5',,'1PG10.3)") Nset(k,i),j,0.0
                    endif
                endif
            enddo
        enddo
     enddo
802 continue

    rewind(inp)
    CloadNumber = 0
    do
        do  !find Cload
            read(inp,"(A)",end=803) rec
            if(rec(1:6).eq."*Cload") exit !found one
        enddo
        CloadNumber = CloadNumber + 1 !count it
        read(inp,*,end=903) auxrec, idof, iLoad
        CloadName(CloadNumber) = auxrec(index(auxrec,"_")+1:) !eliminate underscore
        if (CloadNumber.eq.1) write(out,"(80A)") "*CLOAD";        
        write(out,"(80A)") "**NSET=", CloadName(CloadNumber)
        write(abq,"(80A)") "*CLOAD";        
        write(abq,"(80A)") "**NSET=", CloadName(CloadNumber)
        !generate Cloads
        k = 1; 
        do 
            if (index(NsetName(k),CloadName(CloadNumber)).ne.0) exit
            k = k + 1
        enddo
        do i = 1, NsetLength(k)
            write(out,"(I5','I5','1PG10.3)") Nset(k,i), idof, - iLoad   !reversed for bmi3.f
            write(abq,"(I5','I5','1PG10.3)") Nset(k,i), idof,   iLoad
        enddo
    enddo
803 if (CloadNumber.eq.0) pause "error: no *Cload found";

    write(out,"(80A)") rec  !should always print *Nstep
    write(abq,"(80A)") rec  !should always print *Nstep
    
    !write dat file
    write(dat,1004) NumberOfMaterials
    write(dat,1004) MaterialPerElement(1:NElements)
    do i=1,6; do j=i,6; ABD(j,i) = ABD(i,j); enddo; enddo;  !fill symmetric
    do i=1,6; write(dat,1005) (ABD(i,j),j=1,6), 0., 0., 0.; enddo;
    write(dat,1005) 0., 0., 0., 0., 0., 0., K11, K12, 0.
    write(dat,1005) 0., 0., 0., 0., 0., 0., K12, K22, 0.
    write(dat,1005) 0., 0., 0., 0., 0., 0.,  0.,  0., (K11+K22)/200 !ref: raftoyiannis Ph.D. 
    !perturbation on mode, node, dof
    !default 0,0,0, picks Dof of node with max. disp. mode 1
    write(dat,1004) PertMode, PertNode, PertDof 

    rewind(inp)
    do  !find *Orientation
        read(inp,"(A)",end=804) rec
        if(rec(1:7).eq."*Dsload") pause "error: BMI3 cannot handle *Dsload."
    enddo
804 continue

    rewind(inp)
    do  !find *Orientation
        read(inp,"(A)",end=805) rec
        if(rec(1:12).eq."*Orientation") pause "error: BMI3 cannot handle *Orientation."
    enddo
805 continue

    pause "Take note of any errors or messages above. OK to continue?"
    close(inp); close(out); stop

901 pause "error: opening input file"; stop
902 pause "error: opening output file"; stop
903 pause "error: unexpected end of file reached"; stop
904 pause "error: 3 numbers expected on generate Nset"; stop

1001    format (7(1pG10.3,',')1pG10.3)
1002    format (2(1pG10.3,',')1pG10.3)
1003    format (A)
1004    format (12I5)
1005    format (9(1pG13.6))

    end
