import pandas as pd

def standardize_plot(fig):
    fig.update_layout(
        template="simple_white",
        font_family="Inter",
        legend_font_size=28/3,
    )
    fig.update_yaxes(
        minor_ticks="outside", 
        title_font_family="Inter", 
        title_font_size=28/3, 
        tickfont_size=28/3, 
    )
    fig.update_xaxes(
        minor_ticks="outside", 
        title_font_family="Inter", 
        title_font_size=28/3, 
        tickfont_size=28/3, 
    )
    fig.for_each_annotation(lambda a: a.update(
        font_size=28/3,
        font_family="Inter",
    ))
    return fig



def read_breakage_data(filepaths):
    dfs = []

    for exp, filepath in filepaths.items():
        df_breaks = pd.read_csv(f'{filepath}/analysis/local.breakmetrics.csv')
        df_breaks = df_breaks[df_breaks['category'] == 'mapped_high']
        df_lengths = pd.read_csv(f'{filepath}/analysis/local.readmetrics.csv')
        df_lengths = df_lengths[df_lengths['category'] == 'mapped_high']
        df = pd.merge(df_breaks, df_lengths, on=['read_id', 'ref_id', 'read_direction', 'read_number', 'category'])
        df['exp'] = exp
        dfs.append(df)

    return pd.concat(dfs)