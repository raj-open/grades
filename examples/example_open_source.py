#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# OPEN SOURCE EXAMPLE
# Uses repository as open source code directly.
#
# NOTE: !! first install requirements (see examples/README.md) !!
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(__file__), '..'));
sys.path.insert(0, os.getcwd());

# ensure that this is installed from the source code and not the pip libraries:
from src.r_open_grades import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    # create a case
    case = Case(
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # INPUT/OUTPUT OPTIONS
        path_input = 'examples/data/example-data.csv',
        path_output = 'examples/out/example-scores.png',
        # optional configuration of input table:
        # NOTE: Ensure consistent usage of , or . for decimal in file!
        table_config = TableConfig(
            sep     = ';',
            decimal = ',',
            offset  = 0,
            columns = ColumnsConfig(
                points = 'Score',
                grade = 'Note',
                # Default is `True` (= all unnecessary columns are removed).
                dump_columns = True,
            ),
        ),
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # GRADE OPTIONS
        # NOTE: Sort from highest to lowest grade!
        grade_schema = [
            Grade(grade='A*', min=54.0, max=60.0, include_min=True, include_max=True),
            Grade(grade='A',  min=48.0, max=54.0, include_min=True, include_max=False),
            Grade(grade='B',  min=42.0, max=48.0, include_min=True, include_max=False),
            Grade(grade='C',  min=36.0, max=42.0, include_min=True, include_max=False),
            Grade(grade='D',  min=30.0, max=36.0, include_min=True, include_max=False),
            Grade(grade='E',  min=24.0, max=30.0, include_min=True, include_max=False),
            Grade(grade='U',  min=0.0,  max=24.0, include_min=True, include_max=False),
        ],
        fail_grades = [ 'E', 'U' ],
        remove_fail = False,
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # PLOT OPTIONS
        # NOTE: labels are optional
        title = 'Microeconomic Principles I, 2023\ncohort size: {N}',
        label_frequency          = 'Number of students',
        label_frequency_relative = 'Percentage of students',
        label_grades             = 'Grade',
        label_points             = 'Total score',
        plot_orientation = PLOTORIENTATION.horizontal, # alternative: PLOTORIENTATION.vertical
        as_grades = False, # whether to present histogram in terms of grades or points
        relative  = True,
        # NOTE:
        # if `relative == True`, state frequency range in terms of probabilities.
        # otherwise state frequency irange in terms of values absolute counts:
        frequency_range = [0, 0.35],
    );
    # run the main proceedure on the case
    print('\nRun example on case 1:');
    run(case);

    # reuse case and change a few options:
    case.as_grades = True;
    case.path_output = 'examples/out/example-grades.png';
    case.table_config.columns.dump_columns = False;
    print('\nRun example on case 2:');
    # NOTE:
    # If `dump_columns = False` is used above,
    # user can perform intermediate operations on `data` before plotting.
    # To do this, instead of `run` call
    #    1. `prepare_data`
    #    2. `represent_data`
    data = prepare_data(case=case);
    data = data[data['Group'] != 'BEGINNER'];
    fig, axs = represent_data(case=case, data=data);
