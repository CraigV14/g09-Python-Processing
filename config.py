import re
# Input file name
inputFileName = 'something obviously wrong'

# Output file name
outputFileName = 'something obviously wrong'

# Number of frozen atoms
N_Freeze = 0

# Get N. Kind of wonky because I/O files need to be set first
def	setN():
	lookup =" NAtoms"
	with open(outputFileName) as f:
		for num, line in enumerate(f, 1):
			if lookup in line:
				location = num
				break
		f.seek(0)
		Nlist = f.readlines()[location-1]
	nums = re.findall(r'\d+', Nlist)
	N = int(nums[0])
	return N