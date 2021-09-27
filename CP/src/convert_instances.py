import os
import sys
sys.path.append("../..")


from common.utils import read_instance
import numpy as np

def convert_instance_to_dzn(filename):
    outfile = filename.replace('../../instances', '../datafiles').replace('.txt', '.dzn')
    width, num_circuits, circuits_h, circuits_w = read_instance(filename)
    with open(outfile, 'w') as out:
        out.write(f"num_circuits={num_circuits};\n")
        out.write(f"width={width};\n")
        out.write(f"circuits_w={circuits_w};\n")
        out.write(f"circuits_h={circuits_h};\n")
    return outfile
