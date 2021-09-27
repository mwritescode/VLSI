import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import numpy as np


COLORS = {
    'red': '\033[31m',
    'green': '\033[32m',
    'endc': '\033[m'
}

def show_output(sol, show=True, file=None):
    _, ax = plt.subplots()
    print_grid(ax, sol['width'], sol['height'])
    circuits_info = sol['circuits_w'], sol['circuits_h'], sol['circuits_x'], sol['circuits_y']
    print_colored_circuits(ax, circuits_info, sol['num_circuits'])
    ax.set_title(sol['msg'])
    if show:
        plt.show()
    else:
        plt.savefig(file)

def print_colored_circuits(ax, circuits_info, num_circuits):
    circuits_w, circuits_h, circuits_x, circuits_y = circuits_info
    colors = plt.cm.get_cmap(name='hsv', lut=num_circuits+1)
    indexes = [i/num_circuits for i in range(num_circuits)]
    for w, h, x, y, i in zip(circuits_w, 
                        circuits_h, 
                        circuits_x, 
                        circuits_y,
                        indexes):
        circuit = Rectangle((x,y), w, h, 
                            facecolor=colors(i), 
                            edgecolor='black', 
                            linestyle='solid', 
                            linewidth=1.5)
        ax.plot(x, y, color='black', marker='o', clip_on=False)
        ax.add_patch(circuit)

def print_grid(ax, width, height):
    ax.set(xlim=(0, width), ylim=(0, height))
    ax.set_aspect('equal')
    ticks_x = np.arange(0, width+1, 1)
    ticks_y = np.arange(0, height+1, 1)
    ax.set_xticks(ticks_x)
    ax.set_yticks(ticks_y)
    ax.grid(color='black', linewidth=1, linestyle='--')
    ax.tick_params(left=False,
                bottom=False,
                labelleft=False,
                labelbottom=False)

def read_circuits_info(filename, num_circuits):
    circuits_w, circuits_h, circuits_x, circuits_y = [], [], [], []
    for _ in range(num_circuits):
        w, h, x, y = filename.readline().strip().split(' ')
        circuits_w.append(int(w))
        circuits_h.append(int(h))
        circuits_x.append(int(x))
        circuits_y.append(int(y))
    return circuits_w, circuits_h, circuits_x, circuits_y

def read_instance(filename):
    with open(filename, 'r') as instance:
        width = int(instance.readline().strip())
        num_circuits = int(instance.readline().strip())
        circuits_w, circuits_h = read_circuits_info(instance, num_circuits)
    return width, num_circuits, circuits_w, circuits_h

def read_circuits_info(filename, num_circuits):
    circuits_w, circuits_h = [], []
    for _ in range(num_circuits):
        w, h = filename.readline().strip().split(' ')
        circuits_w.append(int(w))
        circuits_h.append(int(h))
    return circuits_w, circuits_h

def write_output(filename, sol):
    with open(filename, 'w') as out:
        out.write(str(sol['width']) + ' ' + str(sol['height']) + '\n')
        out.write(str(sol['num_circuits']) + '\n')
        for w, h, x, y in zip(sol['circuits_w'],
                            sol['circuits_h'],
                            sol['circuits_x'],
                            sol['circuits_y']):
            out.write(str(w) + ' ' + str(h) + ' ' + str(x) + ' ' + str(y) + '\n') 