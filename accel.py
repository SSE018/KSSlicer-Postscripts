import sys
import re

srch = []
cmd = []

## Set search strings and commands for insert.
#Perimeters
cmd.append('SET_VELOCITY_LIMIT ACCEL=3000 SQUARE_CORNER_VELOCITY=10')
#Loops
cmd.append('SET_VELOCITY_LIMIT ACCEL=3500 SQUARE_CORNER_VELOCITY=10')
#Sparse infill
cmd.append('SET_VELOCITY_LIMIT ACCEL=6000 SQUARE_CORNER_VELOCITY=20')
#Solid infill
cmd.append('SET_VELOCITY_LIMIT ACCEL=4000 SQUARE_CORNER_VELOCITY=15')
#Crown
cmd.append('SET_VELOCITY_LIMIT ACCEL=3500 SQUARE_CORNER_VELOCITY=10')
#Travel
cmd.append('SET_VELOCITY_LIMIT ACCEL=7000')

file = sys.argv[1]
print('Reading file...')
with open(file,'r') as f:
    gcode = f.read()

print('Starting Main Process')
if re.search('; add_comments = 1',gcode):
    if re.search('; add_m101_g10 = 2',gcode):
        srch.append(re.compile(r'(\n; \'Perimeter.*?G11\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Loop.*?G11\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'(Stacked Sparse|Sparse Infill).*?G11\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Solid.*?G11\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Crown.*?G11\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Destring.*?G1 .*?\n;\n)',flags=(re.DOTALL)))
        
    elif re.search('; add_m101_g10 = 0',gcode):
        srch.append(re.compile(r'(\n; \'Perimeter.*?\n;.*?\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Loop.*?\n;.*?\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'(Stacked Sparse|Sparse Infill).*?\n;.*?\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Solid.*?\n;.*?\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Crown.*?\n;.*?\n)',flags=(re.DOTALL)))
        srch.append(re.compile(r'(\n; \'Destring.*?G1 .*?\n;\n)',flags=(re.DOTALL)))
 
if len(srch) > 0:
    for i in range(len(srch)):
        gcode = re.subn(srch[i], r'\1' + cmd[i] + r'\n',gcode)[0]

## end  setting ##

print('Writing file...')
with open(file,'w') as o:
    o.write(gcode)
