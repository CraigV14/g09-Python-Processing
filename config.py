import re
# Input file name
inputFileName = 'SiF3Oopt.gjf'

# Output file name
outPutFileName = 'SiF3Oopt.log'

# Go and find N

#String to find
lookup =" NAtoms"
with open(outPutFileName) as f:
	for num, line in enumerate(f, 1):
		if lookup in line:
			location = num
			break
	f.seek(0)
	Nlist = f.readlines()[location-1]
nums = re.findall(r'\d+', Nlist)
N = int(nums[0])