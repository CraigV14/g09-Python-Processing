import config
import re

# Set the number of atoms
def setN():
	lookup =" NAtoms"
	with open(config.outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		f.seek(0)
		Nlist = f.readlines()[location-1]
	nums = re.findall(r'\d+', Nlist)
	N = int(nums[0])
	return N
# Set number of frozen atoms
def setN_Freeze():
    import OFProc
    N_Freeze = OFProc.setNoFrozen()
    config.N_Freeze = N_Freeze