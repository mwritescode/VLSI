import os

def process_output(filename, report_file):
    with open(filename, 'r') as out:
        solutions = out.read()
        solutions = solutions.split('----------')
        last_sol = solutions[-2]
        elapsed_time = last_sol.splitlines()[-1].split(' ')[-2]

        if solutions[-1] == '\n' or solutions[-1].splitlines()[1].strip() != '==========':
            # No optimal solution found, still print the best one
            msg = f"Non-optimal solution found in {elapsed_time} seconds"
        else:
            msg = f"Optimal solution found in {elapsed_time} seconds"
        store_timing_info(filename, report_file, last_sol, solutions[0], msg)
        sol = read_solution(last_sol)
        sol['msg'] = msg
        return sol

def read_solution(sol):
    lines = sol.splitlines()[1:-1]
    width, height = [int(val) for val in lines[0].strip().split(' ')]
    num_circuits = int(lines[1].strip().split(' ')[0])
    sol = {
        'width': width,
        'height': height,
        'num_circuits': num_circuits,
        'circuits_w': [],
        'circuits_h': [],
        'circuits_x': [],
        'circuits_y': []
        }
    for line in lines[2:num_circuits+3]:
        w, h, x, y = [int(val) for val in line.strip().split(' ')]
        sol['circuits_h'].append(h)
        sol['circuits_w'].append(w)
        sol['circuits_x'].append(x)
        sol['circuits_y'].append(y)
    return sol

def store_timing_info(instance_name, report_file, last_sol, first_sol, msg):
    last_sol_time = last_sol.splitlines()[-1].split(' ')[-2]
    first_sol_time = first_sol.splitlines()[-1].split(' ')[-2]
    optimal_found = 'Non' not in msg
    out = instance_name + '\t' + str(first_sol_time) + '\t'
    if optimal_found:
        out += str(last_sol_time) + '\n'
    else:
        out += '---\n'
    if os.path.isfile(report_file):
        with open(report_file, 'a') as file:
                file.write(out)
    else:
        with open(report_file, 'w') as file:
            file.write('Instance name \t First solution \t Optimal solution\n')
            file.write(out)
