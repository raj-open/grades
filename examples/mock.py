#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# MOCKDATA
# Use this to create mockdata
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

import os;
import sys;

os.chdir(os.path.join(os.path.dirname(__file__), '..'));
sys.path.insert(0, os.getcwd());

import numpy as np;
import pandas as pd;
import shortuuid;

# ensure that this is installed from the source code and not the pip libraries:
from src.r_open_grades import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# CONSTANTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

PATH_DATA = 'examples/data/example-data.csv';
COLUMN_ID = 'Id';
COLUMN_POINTS = 'Score';
COLUMN_GRADE = 'Note';
N = 100;
grade_schema = [
    Grade(grade='A*', min=54.0, max=60.0, include_min=True, include_max=True),
    Grade(grade='A',  min=48.0, max=54.0, include_min=True, include_max=False),
    Grade(grade='B',  min=42.0, max=48.0, include_min=True, include_max=False),
    Grade(grade='C',  min=36.0, max=42.0, include_min=True, include_max=False),
    Grade(grade='D',  min=30.0, max=36.0, include_min=True, include_max=False),
    Grade(grade='E',  min=24.0, max=30.0, include_min=True, include_max=False),
    Grade(grade='U',  min=0.0,  max=24.0, include_min=True, include_max=False),
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def create_uuid(length: int) -> str:
    return shortuuid.ShortUUID().random(length=length);

def compute_grade(x: float, schema: list[Grade]) -> float:
    try:
        index = min([i for i, s in enumerate(schema) if x > s.min or (s.include_min and x >= s.min)]);
        return schema[index].grade;
    except:
        raise Exception(f'Cannot find grade for {x} in grade-schema! Check if grade-schema is complete and values are valid.');

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXECUTION
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

if __name__ == '__main__':
    # create made up scores:
    u = np.random.rand(N);
    points = (u < 0.15) * np.random.normal(55, scale=5, size=N) \
        + (0.15 <= u) * (u < 0.75) * np.random.normal(30, scale=7, size=N) \
        + (0.75 <= u) * np.random.normal(15, scale=7, size=N);
    points = np.minimum(points, 60);
    points = np.maximum(points, 0);
    points = np.round(4*points)/4;
    # attribute grades according to scheme:
    grades = np.asarray(list(map(lambda x: compute_grade(x, grade_schema), points)));
    # randomly make some data missing:
    u = np.random.rand(N);
    v = np.random.rand(N);
    points[u < 0.05] = np.NAN;
    grades[u < 0.025] = '';
    grades[v < 0.25] = '';
    # create data frame:
    data = pd.DataFrame({
        COLUMN_ID: [ create_uuid(length=8).upper() for _ in range(N) ],
        COLUMN_POINTS: points,
        COLUMN_GRADE: grades,
    });
    # write to csv:
    with open(PATH_DATA, 'w') as fp:
        data.to_csv(fp, sep=';', decimal=',', index=False, na_rep='');
