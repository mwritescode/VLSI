# SMT solution to the VLSI problem
The folders 'out' and 'out-imgs' respectively contain the .txt solution files and the .png visual interpretation for the instances solved by the iterative version of the model without rotation. Similarly, the folders 'out-rot' and 'out-imgs-rot' contain .txt solutions and graphical interpretations for the instances solved by the iterative model with rotation. Finally, 'out-opt' and 'out-imgs-opt' store the results obtained by the optimization model without rotation for our 40 instances. 
Note that, in this case only the optimal solutions are shown.

To reproduce this results you should simply run the python commands from the SMT/src directory:
```
# For the iterative model without rotation
python iterative_solve_smt.py

# For the iterative model with rotation
python iterative_solve_smt.py --rotation True

# For the optimization model without rotation
python solve_smt.py

```
The only required library that is not part of the python standard library is matplotlib.

Note that there are other arguments that you can pass to `solve_smt.py`\`iterative_solve_smt.py`, which allow you to customize the output folders and the name of the report file. A brief description of all the available arguments can be accessed through `python solve_smt.py -h`\`python iterative_solve_smt.py -h`.

```
usage: solve_smt.py [-h] [--show-sols SHOW_SOLS] [--output-folder OUTPUT_FOLDER] [--output-imgs-folder OUTPUT_IMGS_FOLDER] [--rotation ROTATION] [--report-file REPORT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --show-sols SHOW_SOLS
                        Whether to show each instance solution (optimal if found, otherwise sub-optimal) at the end of the execution or simply store them.
  --output-folder OUTPUT_FOLDER
                        Path were the solutions .txt files should be stored.
  --output-imgs-folder OUTPUT_IMGS_FOLDER
                        Path were to store the graphical representation of each solution.
  --rotation ROTATION   Whether the SMT model to be executed should allow rotation or not.
  --report-file REPORT_FILE
                        File path were to save a summary of the solved instances and the relative timing information
```

The only thing which must not be moved is the 'instances' folder where the instances to solve are store, which has to remain inside 'common'.
