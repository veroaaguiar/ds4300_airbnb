import pandas as pd
import plotly.graph_objects as go

def agg_data(df, src, targ, n):
    '''Aggregates source and target column in the df'''

    df1 = df.groupby([src, targ]).size().sort_values(ascending=False).reset_index(name='count')
    df1 = df1[df1['count'] >= n]

    return df1


def code_mapping(df, src, targ):
    ''' Map labels in src and targ columns to integers'''

    labels = list(df[src]) + list(df[targ])
 
    labels = sorted(list(set(labels)))
    

    codes = list(range(len(labels)))

    lcmap = dict(zip(labels, codes))

    df = df.replace({src: lcmap, targ: lcmap})

    return df, labels


def make_sankey(df, src, targ, vals=None, **kwargs):
    '''Creates Sankey Diagram based on inputted params (for 2 columns)'''

    df, labels = code_mapping(df, src, targ)

    if vals:
        value = df[vals]
    else:
        value = [1] * df.shape[0]

    link = {'source': df[src], 'target': df[targ], 'value': value}

    pad = kwargs.get('pad', 100)
    thickness = kwargs.get('thickness', 10)
    line_color = kwargs.get('line_color', 'black')
    width = kwargs.get('width', 2)

    node = {'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': width}, 'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()


def make_sankey_extracredit(df1, df2, src, targ1, targ2, vals=None, **kwargs):
    '''Creates Sankey Diagram based on inputted params (for 3 columns)'''

    df1.rename(columns={src: 'source', targ1: 'target'}, inplace=True)
    df2.rename(columns={targ1: 'source', targ2: 'target'}, inplace=True)

    # Concatenate the two dfs together on the src column
    df = pd.concat([df1, df2])

    df, labels = code_mapping(df, 'source', 'target')

    if vals:
        value = df[vals]
    else:
        value = [1] * df.shape[0]

    link = {'source': df['source'], 'target': df['target'], 'value': value}

    pad = kwargs.get('pad', 100)
    thickness = kwargs.get('thickness', 10)
    line_color = kwargs.get('line_color', 'black')
    width = kwargs.get('width', 2)

    node = {'pad': pad, 'thickness': thickness, 'line': {'color': line_color, 'width': width}, 'label': labels}

    sk = go.Sankey(link=link, node=node)
    fig = go.Figure(sk)
    fig.show()