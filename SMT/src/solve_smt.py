import os
import sys
sys.path.append("../..")

import time
import argparse
from z3 import *

from common.utils import show_output, read_instance, write_output, COLORS
from iterative_solve_smt import write_report


def vlsi_smt(width, num_circuits, w, h, rotation=False):
    start = time.time()
    circuits_x = [Int(f"x_{i}") for i in range(num_circuits)]
    circuits_y = [Int(f"y_{i}") for i in range(num_circuits)]

    circuits_w = [Int(f"w_{i}") for i in range(num_circuits)]
    circuits_h = [Int(f"h_{i}") for i in range(num_circuits)]

    height = Int("height")
    max_height = sum(h)
    area_min = sum([circuits_h[i]*circuits_w[i] for i in range(num_circuits)])
    min_height = area_min/width

    opt = Optimize()
    opt.set(timeout=300000)
    if rotation:
        opt.add([Or(And(circuits_w[i] == w[i], circuits_h[i] == h[i]), And(circuits_w[i] == h[i], circuits_h[i] == w[i])) for i in range(num_circuits)])
    else:
        opt.add([And(circuits_w[i] == w[i], circuits_h[i] == h[i]) for i in range(num_circuits)]) 
    opt.add(And(height <= max_height, height >= min_height))
    
    non_overlap = [Or(circuits_x[i] + circuits_w[i] <= circuits_x[j],
                    circuits_x[i] >= circuits_x[j] + circuits_w[j],
                    circuits_y[i] + circuits_h[i] <= circuits_y[j],
                    circuits_y[i] >= circuits_y[j] + circuits_h[j]
                    ) for i in range(num_circuits-1) for j in range(i+1, num_circuits)]
    
    in_limits = [And(circuits_x[i] + circuits_w[i] <= width,
                circuits_y[i] + circuits_h[i] <= height, 
                circuits_x[i] >= 0, 
                circuits_y[i] >= 0) for i in range(num_circuits)]

    opt.add(non_overlap + in_limits)

    # Implied constraint on the sum of the circuits' height at position x_thr
    for x_thr in range(width):
        opt.add(Sum([If(And(circuits_x[j] <= x_thr, (circuits_x[j] + circuits_w[j]) > x_thr), circuits_h[j], 0) for j in range(num_circuits)]) <= height)
    
    # Implied constraint on the sum of the circuits' width at position y_thr
    for y_thr in range(max_height):
        opt.add(Sum([If(And(circuits_y[j] <= y_thr, (circuits_y[j] + circuits_h[j]) > y_thr), circuits_w[j], 0) for j in range(num_circuits)]) <= width)
    
    # Symmetry breaking constraints
    lex_x = lex_lesseq(circuits_x, flip(circuits_x, circuits_w, width))
    lex_y = lex_lesseq(circuits_y, flip(circuits_y, circuits_h, height))
    
    #same_y = [If(
    #    And(Or(circuits_h[i] == circuits_h[j], circuits_w[i] == circuits_w[j]), circuits_y[i] == circuits_y[j]), 
    #    Or(circuits_x[i] < circuits_x[j], circuits_x[j] < circuits_x[i]), 
    #    True) for i in range(num_circuits-1) for j in range(i+1,num_circuits)]
    #same_x = [If(
    #    And(Or(circuits_w[i] == circuits_w[j], circuits_h[i] == circuits_h[j]), circuits_x[i] == circuits_x[j]), 
    #    Or(circuits_y[i] < circuits_y[j], circuits_y[j] < circuits_y[i]), 
    #    True) for i in range(num_circuits-1) for j in range(i+1, num_circuits)]
    
    opt.add([lex_x, lex_y])
   
    opt.minimize(height)

    if str(opt.check()) == 'sat':
        model = opt.model()
        sol = {
        'width': width,
        'height': int(model[height].as_string()),
        'num_circuits': num_circuits,
        'circuits_w': [int(model.evaluate(circuits_w[i]).as_string()) for i in range(num_circuits)],
        'circuits_h': [int(model.evaluate(circuits_h[i]).as_string()) for i in range(num_circuits)],
        'circuits_x': [int(model.evaluate(circuits_x[i]).as_string()) for i in range(num_circuits)],
        'circuits_y': [int(model.evaluate(circuits_y[i]).as_string()) for i in range(num_circuits)],
        'msg': 'Optimal solution found in {0:.2f} seconds'.format(time.time() - start)
        }
    else:
        sol = 'No solution could be found!'
    
    return sol

def flip(arr, lenghts, max):
    return [max - arr[i] - lenghts[i] for i in range(len(lenghts))]

def lex_lesseq(list_xy, flipped_xy):    
    if len(list_xy) == 0:
        return True
    return Or(list_xy[0] <= flipped_xy[0], And(lex_lesseq(list_xy[1:], flipped_xy[1:]), list_xy[0] == flipped_xy[0]))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--show-sols', default=False, help='Whether to show each instance solution (optimal if found, otherwise sub-optimal) at the end of the execution or simply store them.')
    parser.add_argument('--output-folder', default='../out/', help='Path were the solutions .txt files should be stored.')
    parser.add_argument('--output-imgs-folder', default='../out-imgs/', help='Path were to store the graphical representation of each solution.')
    parser.add_argument('--rotation', default=False, help='Whether the SMT model to be executed should allow rotation or not.')
    parser.add_argument('--report-file', default='report.csv', help='File path were to save a summary of the solved instances and the relative timing information')

    args = parser.parse_args()

    if not os.path.isdir(args.output_folder):
        os.mkdir(args.output_folder)
    
    if not args.show_sols and not os.path.isdir(args.output_imgs_folder):
        os.mkdir(args.output_imgs_folder)

    instances_path = '../../common/instances/'
    out_path = args.output_folder
    out_img_path = args.output_imgs_folder
    report_file = args.report_file
    show_sol = args.show_sols
    for instance_file in os.listdir(instances_path):
        print(COLORS['green'], f'Starting to solve {instance_file}...', COLORS['endc'])
        width, num_circuits, circuits_w, circuits_h = read_instance(instances_path + instance_file)
        sol = vlsi_smt(width, num_circuits, circuits_w, circuits_h, rotation=False)
        if isinstance(sol, str):
            print(COLORS['red'], f'No solution found for {instance_file}...', COLORS['endc'])
        else:
            out_name = instance_file.replace('ins', 'out')
            write_output(out_path + out_name, sol)
            write_report(out_name, sol, report_file)
            show_output(sol, show_sol, out_img_path + out_name.replace('txt', 'png'))