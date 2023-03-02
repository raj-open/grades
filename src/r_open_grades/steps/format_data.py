#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ..thirdparty.code import *;
from ..thirdparty.db import *;
from ..thirdparty.types import *;

from ..models.generated.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'format_data',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def format_data(
    data: pd.DataFrame,
    grade_schema: Optional[list[Grade]],
    fail_grades: list[int | float | str],
    remove_fail: bool,
    **_,
) -> pd.DataFrame:
    # filter out null values:
    data = data[data['points'].notnull()];
    data = data.reset_index(drop=True);

    # sort values by points:
    data.sort_values(
        by = ['points'],
        ascending = [True],
        inplace = True,
    );
    data = data.reset_index(drop=True);

    # if needed, compute grade from schema
    if grade_schema is not None:
        indexes_missing = data.index[data['grade'].isna()].to_list();
        data.loc[indexes_missing, 'grade'] = data.loc[indexes_missing, 'points'].map(partial(
            compute_grade,
            schema = grade_schema,
        ));

    # optionally remove fail grade/s:
    if remove_fail:
        data_passed = data[data['grade'].isin(fail_grades)];
        data = data_passed;
        data = data.reset_index(drop=True);

    return data;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def compute_grade(x: float, schema: list[Grade]) -> float:
    try:
        index = min([i for i, s in enumerate(schema) if x > s.min or (s.include_min and x >= s.min)]);
        return schema[index].grade;
    except:
        raise Exception(f'Cannot find grade for {x} in grade-schema! Check if grade-schema is complete and values are valid.');
