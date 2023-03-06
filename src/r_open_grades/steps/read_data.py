#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ..thirdparty.db import *;

from ..models.generated.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'read_data',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def read_data(
    path_input: str,
    table_config: Optional[TableConfig],
    **_
) -> pd.DataFrame:
    if table_config is None:
        table_config = TableConfig(columns=ColumnsConfig());

    # get data from csv:
    with open(path_input, 'r') as fp:
        data = pd.read_csv(
            fp,
            sep=table_config.sep,
            decimal=table_config.decimal,
            header=table_config.offset
        );

    # handle cases of missing columns:
    colnames = data.columns.to_list();
    colname_grade = table_config.columns.grade;
    colname_points = table_config.columns.points;
    match (colname_points in colnames, colname_grade in colnames):
        case (True, True):
            data[colname_points] = pd.to_numeric(data[colname_points], errors='coerce');
        case (True, False):
            data[colname_points] = pd.to_numeric(data[colname_points], errors='coerce');
            data[colname_grade] = pd.NA;
        case (False, True):
            data[colname_points] = pd.NA;
        case (False, False):
            raise Exception(f'Table must contain at least one of the columns \x1b[1m[{colname_points}, {colname_grade}]\x1b[0m.');
        case _:
            pass;

    if table_config.columns.dump_columns:
        data = data[[colname_points, colname_grade]];

    # rename columns:
    data.rename(columns={colname_points: 'points', colname_grade: 'grade'}, inplace=True);
    return data;
