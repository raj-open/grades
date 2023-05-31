#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from .thirdparty.db import *;
from .thirdparty.plots import *;
from .thirdparty.types import *;

from .models.generated.user import *;
from .steps import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'prepare_data',
    'represent_data',
    'run',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def run(
    case: Case,
    show_stats: bool = True,
) -> tuple[pd.DataFrame, Figure, Axes]:
    '''
    Runs all the steps to prepare and represent the data.

    NOTE: If one wants to perform final adjustments to the data before creating plots,
    one can do the following:

    ```py
    data = prepare_data(case=case);
    # ... perform intermediate steps on data ...
    represent_data(case=case, data=data);
    ```
    '''
    data = prepare_data(case=case);
    fig, axs = represent_data(case=case, data=data, show_stats=show_stats);
    return data, fig, axs;

def prepare_data(case: Case) -> pd.DataFrame:
    '''
    Reads in the data, formats, sorts, fills in the columns.
    '''
    case_as_dict = case_to_kwargs(case);
    data = read_data(**case_as_dict);
    data = format_data(data=data, **case_as_dict);
    return data;

def represent_data(
    case: Case,
    data: pd.DataFrame,
    show_stats: bool = True,
) -> tuple[Figure, Axes]:
    '''
    Assumes data has been prepared.
    Displays data as plots and statistics.
    '''
    case_as_dict = case_to_kwargs(case);
    fig, axs = output_plot(data=data, **case_as_dict);

    if show_stats:
        output_stats(data=data, **case_as_dict);
    return fig, axs;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# AUXILIARY METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def case_to_kwargs(case: Case) -> dict[str, Any]:
    # # deep copy:
    # return case.dict(by_alias=False);
    # shallow copy:
    return dict(case);
