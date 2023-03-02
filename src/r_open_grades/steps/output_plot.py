#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# IMPORTS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

from ..thirdparty.db import *;
from ..thirdparty.maths import *;
from ..thirdparty.plots import *;

from ..models.generated.user import *;

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# EXPORT
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

__all__ = [
    'output_plot',
];

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# METHODS
# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

def output_plot(
    data: pd.DataFrame,
    path_output: str,
    title: str,
    label_frequency: str,
    label_frequency_relative: str,
    label_grades: str,
    label_points: str,
    as_grades: bool,
    relative: bool,
    plot_orientation: PLOTORIENTATION,
    frequency_range: Optional[list[float, float]],
    grade_schema: Optional[list[Grade]],
    **_
):
    N = len(data);
    grouped = data.groupby('grade');

    fig, axs = mplot.subplots(1, 1, constrained_layout=True);
    mplot.title(title.format(N=N), loc='center', fontdict={'size': 18, 'family': 'Calibri'});
    mplot.margins(x=0, y=0);

    values: dict[str, tuple[np.ndarray, int]] = dict();
    # ensure groups are sorted as in schema (if provided):
    if grade_schema is not None:
        labels = [ s.grade for s in grade_schema ];
        grouped = sorted(grouped, key = lambda x: (labels + [x[0]]).index(x[0]));
    grouped = [ (str(label), group) for label, group in grouped ];
    # plot groups:
    for label, group in grouped:
        n = len(group);
        if as_grades:
            match plot_orientation:
                case PLOTORIENTATION.vertical:
                    axs.bar(
                        [ label ],
                        [ n/N if relative else n ],
                        width = [ 0.5 ],
                        label = label,
                        alpha = 0.5,
                        align = 'center',
                    );
                # case PLOTORIENTATION.horizontal:
                case _:
                    axs.barh(
                        [ label ],
                        [ n/N if relative else n ],
                        height = [ 0.5 ],
                        label = label,
                        alpha = 0.5,
                        align = 'center',
                    );
        else:
            points = group['points'];
            _, bins, _ = axs.hist(
                # points[:-1],
                points,
                weights = ([1./N] if relative else [1])*n,
                label = label,
                orientation = 'vertical' if plot_orientation == PLOTORIENTATION.vertical else 'horizontal',
                cumulative = 1,
                alpha = 0.5,
                histtype = 'stepfilled',
                density = False,
                align = 'mid'
            );
            values[label] = (bins, n);

    label_counts = label_frequency_relative if relative else label_frequency;
    label_categories = label_grades if as_grades else label_points;
    value_range = [];
    if not as_grades:
        value_min = min(data['points']);
        value_max = max(data['points']);
        value_mid = abs(value_max + value_min)/2;
        eps = 0.1 * ((value_max - value_min) / 2 + value_mid);
        eps = eps if eps > 0.0 else 1.0;
        value_range = [max(value_min - eps, 0), round(value_max + eps)];

    match plot_orientation:
        case PLOTORIENTATION.vertical:
            mplot.ylabel(label_counts, loc='center', fontdict={'size': 16, 'family': 'Calibri'});
            mplot.xlabel(label_categories, loc='center', fontdict={'size': 16, 'family': 'Calibri'});

            if frequency_range is not None:
                mplot.ylim(*frequency_range);
            if as_grades:
                axs.invert_xaxis();
            else:
                mplot.xlim(*value_range);
        # case PLOTORIENTATION.horizontal:
        case _:
            mplot.ylabel(label_categories, loc='center', fontdict={'size': 16, 'family': 'Calibri'});
            mplot.xlabel(label_counts, loc='center', fontdict={'size': 16, 'family': 'Calibri'});

            if frequency_range is not None:
                mplot.xlim(*frequency_range);
            if as_grades:
                axs.invert_yaxis();
            else:
                mplot.ylim(*value_range);

    if not as_grades:
        for label, (bins, n) in values.items():
            frequency_range = frequency_range \
                or (axs.get_ylim() if plot_orientation == PLOTORIENTATION.vertical else axs.get_xlim());
            value = np.mean(bins);
            freq = frequency_range[0]*0.95 + frequency_range[1]*0.05
            (x, y) = (value, freq) if plot_orientation == PLOTORIENTATION.vertical else (freq, value);
            axs.text(x=x, y=y, s=f'{n}', fontdict={'size': 12, 'family': 'Consolas'});

    if relative:
        match plot_orientation:
            case PLOTORIENTATION.vertical:
                axs.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2, symbol='%'));
            # case PLOTORIENTATION.horizontal:
            case _:
                axs.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2, symbol='%'));

    axs.legend(loc='upper right', title=label_grades);
    fig = axs.get_figure();
    fig.savefig(path_output, bbox_inches='tight');
    return;
