import os
import sys
sys.path.append("../..")

import argparse

from common.utils import write_output, show_output, COLORS
from convert_instances import convert_instance_to_dzn
from convert_output import process_output


TEST_INSTANCES = ['ins-5.dzn', 'ins-11.dzn', 'ins-14.dzn', 'ins-18.dzn', 'ins-22.dzn', 
                'ins-25.dzn', 'ins-30.dzn', 'ins-34.dzn', 'ins-38.dzn' , 'ins-40.dzn']


def create_datafiles(instances_path):
    data_files = []
    instances = os.listdir(instances_path)
    for instance in instances:
        infile = instances_path + instance
        outfile = convert_instance_to_dzn(infile)
        data_files.append(outfile)
    return data_files

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--test', default=False, help='Whether to execute the CP model only on the selected 10 test instance or not.')
    parser.add_argument('--show-sols', default=False, help='Whether to show each instance solution (optimal if found, otherwise sub-optimal) at the end of the execution or simply store them.')
    parser.add_argument('--output-folder', default='../out/', help='Path were the solutions .txt files should be stored.')
    parser.add_argument('--output-imgs-folder', default='../out-imgs/', help='Path were to store the graphical representation of each solution.')
    parser.add_argument('--rotation', default=False, help='Whether the CP model to be executed should allow rotation or not.')
    parser.add_argument('--report-file', default='report.csv', help='File path were to save a summary of the solved instances and the relative timing information')

    args = parser.parse_args()

    instances_path = '../../common/instances/'
    if not os.path.isdir('../datafiles/'):
        os.mkdir('../datafiles/')
    if not os.path.isdir(args.output_folder):
        os.mkdir(args.output_folder)
    data_files = os.listdir('../datafiles/')
    if not data_files:
        data_files = create_datafiles(instances_path)
    test = args.test
    show = args.show_sols
    if not show and not os.path.isdir(args.output_imgs_folder):
        os.mkdir(args.output_imgs_folder)
    if not args.rotation:
        model = 'model.mzn'
    else:
        model = 'model_rotation.mzn'


    solutions_found = 0
    if test:
        data_files = TEST_INSTANCES

    out_paths = []
    for data_file in data_files:
        if data_file == 'ins-11.dzn':
            datafile_path = '../datafiles/' + data_file
            out_path = args.output_folder + data_file.replace('.dzn', '.txt').replace('ins', 'out')
            out_paths.append(out_path)
            try:
                # The time-limit paramtere goes in milliseconds, 300000 ms = 5 mins
                os.system(f"minizinc --solver Chuffed -f --solver-time-limit 300000 --all-solutions --output-time {model} {datafile_path} --output-to-file {out_path}")
                solutions_found += 1
                print(COLORS['green'], f"Found solutions for instance {out_path.split('/')[-1]}", COLORS['endc'])
            except KeyboardInterrupt:
                print(COLORS['red'], f"Could not find a solution for instance {out_path.split('/')[-1]}", COLORS['endc'])
    print(COLORS['green'], f'Found solutions for {solutions_found} instances out of {len(data_files)}', COLORS['endc'])
    print('Now elaborating outputs..')
    for out_file in out_paths:
        sol = process_output(out_file, args.report_file)
        write_output(out_file, sol)
        show_output(sol, show, file=args.output_imgs_folder + out_file.split('/')[-1].replace('.txt', '.png'))