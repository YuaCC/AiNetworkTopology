import os
import re
import glob
r = re.compile(r',\d+\s+')
for file in glob.glob('data/*'):
    filename  = file.split('\\')[-1]
    with open(os.path.join('data',filename),'r') as in_file:
        with open(os.path.join('data2',filename),'w') as out_file:
            lines = in_file.readlines()
            for i,line in enumerate(lines):
                line = r.sub(',',line)
                out_file.write(line)
