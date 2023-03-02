#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ..thirdparty.db import *;
from ..thirdparty.maths import *;
from ..thirdparty.render import *;

from ..models.generated.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'output_stats',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def output_stats(
    data: pd.DataFrame,
    title: str,
    grade_schema: Optional[list[Grade]],
    **_
):
    points = data['points'];
    mu = np.mean(points);
    sigma = np.std(points);
    q25 = np.quantile(points, q=0.25);
    q50 = np.quantile(points, q=0.50);
    q75 = np.quantile(points, q=0.75);
    stats_points = ('points', f'{mu:.2f}', f'{sigma:.4f}', f'{q25:.2f}', f'{q50:.2f}', f'{q75:.2f}');

    stats_grades = ('grades', '—', '—', '?', '?', '?');
    if grade_schema is not None:
        grades = [
            ([ i for i, s in enumerate(grade_schema) if s.grade == grade ] + [np.NAN])[0]
            for grade in data['grade']
        ];
        # NOTE: gardes are in reverse order!
        q25 = int(np.quantile(grades, q=1-0.25, method='closest_observation'));
        q50 = int(np.quantile(grades, q=1-0.50, method='closest_observation'));
        q75 = int(np.quantile(grades, q=1-0.75, method='closest_observation'));
        try:
            q25 = grade_schema[q25].grade;
            q50 = grade_schema[q50].grade;
            q75 = grade_schema[q75].grade;
            stats_grades = ('grades', '—', '—', q25, q50, q75);
        except:
            pass;

    table = tabulate(
        [
            stats_points,
            stats_grades,
        ],
        headers = ['', 'mean', 'sd', '25% quantile', 'median', '75% quantile'],
        colalign = [ 'left', 'center', 'center', 'center', 'center', 'center' ],
        tablefmt = 'rst',
    );

    print(title.format(N=len(data)));
    print(table);

    return;
