"""Helper functions for visualization our data in Jupyter notebooks.
"""
from IPython.display import display
import seaborn as sns


VIRIDIS = sns.color_palette('viridis', n_colors=256)


def phase_background(values):
    alpha = 0.1
    if 'level2' in values:
        alpha = values.level2 * 0.1
    attr = 'background-color: rgba(0, 0, 0, {alpha});'.format(alpha=alpha)
    return [attr for v in values]

def viridis_background(value, vmin, vmax, reverse=False):
    norm_value = (value - vmin) / (vmax - vmin)
    if reverse:
        norm_value = 1 - norm_value
    max_index = len(VIRIDIS) - 1
    soft_index = norm_value * max_index
    index = max(0, min(max_index, int(soft_index)))
    color = (int(255*c) for c in VIRIDIS[index])
    return 'background-color: rgba({0}, {1}, {2}, 0.6);'.format(*color)


def percentage_background(value):
    return viridis_background(value, vmin=0, vmax=1)


def time_background(value):
    return viridis_background(value, vmin=0, vmax=300, reverse=True)


def style_level(df, order_by='order'):
    df = df.sort_values(by=order_by)
    styled_df = (
        df.style
        .set_table_styles(
            [{'selector': 'tr',
              'props': [('background-color', 'white')]},
             # Workaround to hide the index column:
             {'selector': '.row_heading, .blank',
              'props': [('display', 'none;')]},
            ])
        #.bar(subset=['n_attempts'], align='mid', color='#d65f5f')
        .apply(phase_background, axis=1)
        .applymap(percentage_background, subset=['success'])
        .applymap(time_background, subset=['time'])
        .format({
            'success': '{:.0%}'.format,
            'time': '{:.0f}s'.format,
        }))
    return styled_df


def display_level_overview(df, order_by):
    styled = style_level(df, order_by=order_by)
    display(styled)
