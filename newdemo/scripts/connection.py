import os, sys
try:
  pdir = os.getenv('MODIM_HOME')
  sys.path.append(pdir + '/src/GUI')
except:
  print("Please set MODIM_HOME env var to MODIM folder")
  sys.exit(1)

from ws_client import *
import ws_client


mws = ModimWSClient()
mws.setDemoPathAuto(__file__)
