import config
import mod

config.outputFileName = "freq_6fixed.log"


mod.setN()
N_Freeze = mod.setN_Freeze()

import IFProc
import OFProc


print OFProc.temperature2()

print OFProc.getLog_q(1)

print OFProc.getLog_q(2)

print OFProc.getLog_q(3)

print OFProc.getLog_q(4)

print OFProc.getFreeE()

print OFProc.nearzerovib(6)

print OFProc.removeFixedRotAndTrans_q()



