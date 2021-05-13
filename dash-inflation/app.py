import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
import plotly.graph_objects as go


# Initialise the app
app = dash.Dash(__name__)

df = pd.read_csv(r'C:\git\bls\dash-inflation\bls_joined_data.csv', parse_dates=True, low_memory=False)
df["date"] = pd.to_datetime(df["date"])
# df.set_index(['date'], inplace=True)

# Define the app

def get_options(list_stocks):
    dict_list = []
    for i in list_stocks:
        dict_list.append({'label': i, 'value': i})

    return dict_list

app.layout = html.Div(
    children=[
        html.Div(className='row',
                 children=[
                    html.Div(className='four columns div-user-controls',
                             children=[
                                 html.H2('DASH - STOCK PRICES'),
                                 html.P('Visualising time series with Plotly - Dash.'),
                                 html.P('Pick one or more stocks from the dropdown below.'),
                                 html.Div(
                                     className='div-for-dropdown',
                                     children=[
                                         dcc.Dropdown(id='stockselector', options=get_options(df['item_name'].unique()),
                                                      multi=True, value=[df['item_name'].sort_values()[0]],
                                                      style={'backgroundColor': '#1E1E1E'},
                                                      className='stockselector'
                                                      ),
                                     ],
                                     style={'color': '#1E1E1E'})
                                ]
                             ),
                    html.Div(className='eight columns div-for-charts bg-grey',
                             children=[
                                 dcc.Graph(id='timeseries', config={'displayModeBar': False}, animate=True)
                             ])
                              ])
        ]

)
children = [
    html.H2('Dash - Inflation Prices'),
    html.P('''Visualising time series with Plotly - Dash'''),
    html.P('''Pick one or more stocks from the dropdown below.''')
]

dcc.Graph(id='timeseries',
          config={'displayModeBar': False},
          animate=True,
          figure=px.line(df,
                         x='date',
                         y='value',
                         color='item_name',
                         template='plotly_dark').update_layout(
                                   {'plot_bgcolor': 'rgba(0, 0, 0, 0)',
                                    'paper_bgcolor': 'rgba(0, 0, 0, 0)'})
          )
# Callback for timeseries price
@app.callback(Output('timeseries', 'figure'),
              [Input('stockselector', 'value')])
def update_graph(selected_dropdown_value):
    trace1 = []
    # Can cache this.
    df_sub = df.sort_values(by=["date"])
    count = 0
    compare = None # stores first value to normalize
    for j in selected_dropdown_value:
        first_date = df_sub[df_sub['item_name'] == j]['date'].min()  # could do any aggregate
        base_line = df[(df_sub['date'] == first_date) & (df_sub['item_name'] == j)]['value'].min()
        if count == 0:
            compare = base_line # could do any aggregate
            count += 1
        else:
            if base_line < compare:
                df_sub.loc[df_sub['item_name'] == j,"value"] = df[(df_sub['item_name'] == j)]['value'] + abs(base_line-compare)
            else:
                df_sub.loc[df_sub['item_name'] == j,"value"] = df[(df_sub['item_name'] == j)]['value'] - abs(
                    base_line - compare)

    for stock in selected_dropdown_value:
        trace1.append(go.Scatter(x=df_sub[df_sub['item_name'] == stock]['date'],
                                 y=df_sub[df_sub['item_name'] == stock]['value'],
                                 mode='lines',
                                 opacity=0.7,
                                 name=stock,
                                 textposition='bottom center'))
    traces = [trace1]
    data = [val for sublist in traces
                    for val in sublist]
    figure = {'data': data,
              'layout': go.Layout(
                  colorway=["#5E0DAC", '#FF4F00', '#375CB1', '#FF7400', '#FFF400', '#FF0056'],
                  template='presentation',
                  paper_bgcolor='rgba(0, 0, 0, 0)',
                  plot_bgcolor='rgba(0, 0, 0, 0)',
                  margin={'b': 15},
                  hovermode='x',
                  autosize=True,
                  title={'text': 'Stock Prices', 'font': {'color': 'white'}, 'x': 0.5},
                  xaxis={'range': [df_sub['date'].min(), df_sub['date'].max()]},
              ),

              }

    return figure


# Run the app
if __name__ == '__main__':
    app.run_server(debug=False,port=8052)
