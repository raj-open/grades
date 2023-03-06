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
    path_output: Optional[str],
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
) -> tuple[Figure, Axes]:
    N = len(data);
    grouped = data.groupby('grade');
    # ensure groups are sorted as in schema (if provided):
    if grade_schema is not None:
        labels = [ s.grade for s in grade_schema ];
        grouped = sorted(grouped, key = lambda x: (labels + [x[0]]).index(x[0]));
    grouped = [ (str(label), group) for label, group in grouped ];

    fig, axs = mplot.subplots(1, 1, constrained_layout=True);
    mplot.title(title.format(N=N), loc='center', fontdict={'size': 18, 'family': 'Calibri'});
    mplot.margins(x=0, y=0);
    match plot_orientation:
        case PLOTORIENTATION.vertical:
            mplot.yticks(rotation=45, ha='right');
        # case PLOTORIENTATION.horizontal:
        case _:
            mplot.xticks(rotation=-45, ha='left');

    # plot groups
    # NOTE: (currently) need to plot twice in order to make alpha of face + edge colours different.
    objects: dict[str, tuple[int, np.ndarray, float]] = dict();
    for label, group in grouped:
        n = len(group);
        if as_grades:
            points = [ label ];
            weights = [ n/N if relative else n ];
            h = 0.5;
            match plot_orientation:
                case PLOTORIENTATION.vertical:
                    container = axs.bar(
                        points, weights, label = label, width = [ h ],
                        align = 'center',
                        alpha = 0.5, edgecolor = None,
                    );
                    axs.bar(
                        points, weights, width = [ h ],
                        align = 'center',
                        facecolor = "None", edgecolor = (0,0,0,1),
                    );
                    object: Rectangle = container[0];
                    (x, y) = object.get_xy();
                    dx = object.get_width();
                    dy = object.get_height();
                    objects[label] = (n, np.asarray([x, x+dx]), y + dy);
                # case PLOTORIENTATION.horizontal:
                case _:
                    container = axs.barh(
                        points, weights, label = label, height = [ h ],
                        align = 'center',
                        alpha = 0.5, edgecolor = None,
                    );
                    axs.barh(
                        points, weights, height = [ h ],
                        align = 'center',
                        facecolor = "None", edgecolor = (0,0,0,1),
                    );
                    object: Rectangle = container[0];
                    (x, y) = object.get_xy();
                    dx = object.get_width();
                    dy = object.get_height();
                    objects[label] = (n, np.asarray([y, y + dy]), x + dx);
        else:
            points = group['points'];
            weights = ([1./N] if relative else [1]) * n;
            orientation = 'vertical' if plot_orientation == PLOTORIENTATION.vertical else 'horizontal';
            _, bins, _ = axs.hist(
                points, weights = weights, label = label, orientation = orientation,
                cumulative = 1, histtype = 'stepfilled', density = False, align = 'mid',
                alpha = 0.5, edgecolor = None,
            );
            axs.hist(
                points, weights = weights, orientation = orientation,
                cumulative = 1, histtype = 'stepfilled', density = False, align = 'mid',
                facecolor = "None", edgecolor = (0,0,0,1), linewidth = 0.5,
            );
            objects[label] = (n, bins, None);

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

    frequency_range = frequency_range \
        or (axs.get_ylim() if plot_orientation == PLOTORIENTATION.vertical else axs.get_xlim());

    count_positions = [ pos**2 for _, _, pos in objects.values() if pos is not None ];
    rel = np.sqrt(np.mean(count_positions)) if len(count_positions) > 0 else 0;
    for label, (n, category_positions, count_position) in objects.items():
        category_position = np.mean(category_positions);
        count_position = count_position or (frequency_range[0]*0.95 + frequency_range[1]*0.05);
        count_position = count_position + 0.05 * rel;
        (x, y) = (category_position, count_position) \
            if plot_orientation == PLOTORIENTATION.vertical \
            else (count_position, category_position);
        axs.annotate(
            text = f'{n}', xy = (x, y),
            ha = 'center' if plot_orientation == PLOTORIENTATION.vertical else 'left',
            va = 'bottom' if plot_orientation == PLOTORIENTATION.vertical else 'center',
        );
        # axs.text(x=x, y=y, s=f'{n}', fontdict={'size': 12, 'family': 'Consolas'}, );

    if relative:
        match plot_orientation:
            case PLOTORIENTATION.vertical:
                axs.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2, symbol='%'));
            # case PLOTORIENTATION.horizontal:
            case _:
                axs.xaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=2, symbol='%'));

    axs.legend(title=label_grades, loc='upper left', bbox_to_anchor=(1, 1));
    fig = axs.get_figure();
    if path_output is not None:
        fig.savefig(path_output, bbox_inches='tight');
    return fig, axs;
