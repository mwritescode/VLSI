# CP solution to the VLSI problem
The folders 'out' and 'out-imgs' respectively contain the .txt solution files and the .png visual interpretation for the 40 given instances solved by the model without rotation. Similarly, the folders 'out-rot' and 'out-imgs-rot' contain .txt solutions and graphical interpretations for the model with rotation. Note that not only the optimal solution are shown; in case optimality could not be reached in the fixed 5 minutes time interval, MiniZinc can return the best solution found so far, so we showed them too.

To reproduce this results you can just run the python commands from the directory CP/src:
```
# For the model without rotation
python solve_cp.py

# For the model with rotation
python solve_cp.py --rotation True
```
The only required library that is not part of the python standard library is matplotlib.

Note that there are other arguments that you can pass to `solve_cp.py`, which allow you to customize the output folders and the name of the report file. A brief description of all the available arguments can be accessed through `python solve_cp.py -h`.
```
usage: solve_cp.py [-h] [--test TEST] [--show-sols SHOW_SOLS] [--output-folder OUTPUT_FOLDER] [--output-imgs-folder OUTPUT_IMGS_FOLDER] [--rotation ROTATION] [--report-file REPORT_FILE]

optional arguments:
  -h, --help            show this help message and exit
  --test TEST           Whether to execute the CP model only on the selected 10 test instance or not.
  --show-sols SHOW_SOLS
                        Whether to show each instance solution (optimal if found, otherwise sub-optimal) at the end of the execution or simply store them.
  --output-folder OUTPUT_FOLDER
                        Path were the solutions .txt files should be stored.
  --output-imgs-folder OUTPUT_IMGS_FOLDER
                        Path were to store the graphical representation of each solution.
  --rotation ROTATION   Whether the CP model to be executed should allow rotation or not.
  --report-file REPORT_FILE
                        File path were to save a summary of the solved instances and the relative timing information
```

It is extremely important for the program to work correctly that the 'instances' folder remains placed in common. If the folder 'datafiles' is not inside CP/src, then it will be created using the original instances .txt.
