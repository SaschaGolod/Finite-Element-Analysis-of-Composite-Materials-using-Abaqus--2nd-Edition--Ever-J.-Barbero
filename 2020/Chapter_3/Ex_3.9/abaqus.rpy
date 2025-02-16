# -*- coding: mbcs -*-
#
# Abaqus/CAE Release 2020 replay file
# Internal Version: 2019_09_13-13.49.31 163176
# Run by ejbarbero on Fri Aug 26 13:15:38 2022
#

# from driverUtils import executeOnCaeGraphicsStartup
# executeOnCaeGraphicsStartup()
#: Executing "onCaeGraphicsStartup()" in the site directory ...
from abaqus import *
from abaqusConstants import *
session.Viewport(name='Viewport: 1', origin=(0.0, 0.0), width=198.554702758789, 
    height=133.150466918945)
session.viewports['Viewport: 1'].makeCurrent()
session.viewports['Viewport: 1'].maximize()
from caeModules import *
from driverUtils import executeOnCaeStartup
executeOnCaeStartup()
openMdb('Ex_3.9.cae')
#: A new model database has been created.
#: The model "Model-1" has been created.
session.viewports['Viewport: 1'].setValues(displayedObject=None)
#* MdbError: incompatible release number, expected 2020, got 6.10-2
upgradeMdb(
    "C:/Users/ejbarbero/Google Drive/Web/cadec-online.com/barbero/feacm-abaqus/Examples/Chapter_3/Ex_3.9/2020/Ex_3.9-6.10-2.cae", 
    "C:/Users/ejbarbero/Google Drive/Web/cadec-online.com/barbero/feacm-abaqus/Examples/Chapter_3/Ex_3.9/2020/Ex_3.9.cae", 
    )
