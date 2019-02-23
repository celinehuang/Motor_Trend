import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# making a dataframe from the tsv file, start reading data at line 5
df = pd.read_csv('./mtcars.tsv', delimiter='\t', encoding='utf-8',header=3)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''**The data was extracted from the 1974 *Motor Trend* US magazine, and comprises fuel 
consumption and 10 aspects of automobile design and performance for 32 automobiles (1973–74 models).**'''

colors = {
    'background': '#bbadef',
    'text': '#7FDBFF'
}

app.layout = html.Div(children=[
    html.Div([html.H1( 
        className='app-header',
        id="title",
        children='Motor Trend 1974'), 
        ]),
    html.Div([
        html.Label('Automobile Models'),
        # Car dropdown
        dcc.Dropdown(
            id='car-dropdown',
            options=[
                {'label': i, 'value': i} for i in df['model']
            ],
            value="Mazda RX4"
        )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'}),
        html.Div([
        html.Label('Compare Models'),
        # Compare dropdown
        dcc.Dropdown(
            id='compare-dropdown',
            options=[
                {'label': i, 'value': i} for i in df['model']
            ],
            value="Mazda RX4"
        )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'}),
        html.Div([html.Div([], id='graph', style={'float': 'left'})]),
        html.Div([dcc.Markdown(
            className='absolute',
            children=markdown_text
            )])
])

# Callback to update the graph based on selected model of automobile
@app.callback(
    dash.dependencies.Output('graph', 'children'),
    [dash.dependencies.Input('car-dropdown', 'value'),
    dash.dependencies.Input('compare-dropdown', 'value')])
def callback_a(selected_car, selected_compare):
    if (selected_compare is None):
        car_df = df[df.model == selected_car]
        return html.Div([
                html.Div([dcc.Graph(
                        id='road-tests-data-visualization',
                        figure={
                        'data': [
                            {'x': ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'], 
                            'y': [car_df.iloc[0]['mpg'], car_df.iloc[0]['cyl'], car_df.iloc[0]['disp'], 
                            car_df.iloc[0]['hp'], car_df.iloc[0]['drat'], car_df.iloc[0]['wt'], 
                            car_df.iloc[0]['qsec'], car_df.iloc[0]['vs'], car_df.iloc[0]['am'], 
                            car_df.iloc[0]['gear'], car_df.iloc[0]['carb']], 'type': 'bar', 'name': ''},
                        ],
                        'layout': {
                            'title': 'Data Visualization - ' + selected_car
                        }
                    }
                )])
            ])
    else:
        car_df = df[df.model == selected_car]
        compare_df = df[df.model == selected_compare]
        return html.Div([
                html.Div([dcc.Graph(
                    figure=go.Figure(
                        data=[
                            go.Bar(
                            x=['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'],
                            y=[car_df.iloc[0]['mpg'], car_df.iloc[0]['cyl'], car_df.iloc[0]['disp'], 
                            car_df.iloc[0]['hp'], car_df.iloc[0]['drat'], car_df.iloc[0]['wt'], 
                            car_df.iloc[0]['qsec'], car_df.iloc[0]['vs'], car_df.iloc[0]['am'], 
                            car_df.iloc[0]['gear'], car_df.iloc[0]['carb']],
                            name=selected_car,
                            marker=go.bar.Marker(
                                color='rgb(55, 83, 109)'
                            )
                        ),
                        go.Bar(
                            x=['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'],
                            y=[compare_df.iloc[0]['mpg'], compare_df.iloc[0]['cyl'], compare_df.iloc[0]['disp'], 
                            compare_df.iloc[0]['hp'], compare_df.iloc[0]['drat'], compare_df.iloc[0]['wt'], 
                            compare_df.iloc[0]['qsec'], compare_df.iloc[0]['vs'], compare_df.iloc[0]['am'], 
                            compare_df.iloc[0]['gear'], compare_df.iloc[0]['carb']],
                            name=selected_compare,
                            marker=go.bar.Marker(
                                color='rgb(26, 118, 255)'
                            )
                        )
                    ],
                    layout=go.Layout(
                        title='Models Comparison',
                        showlegend=True,
                        legend=go.layout.Legend(
                            x=0,
                            y=1.0
                        ),
                        margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                    )
                ),
                id='my-graph'
                )
            ])
        ])
        
# id='compare-data-visualization',
#                         figure={
#                         'data': [
#                             {'x': ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'], 
#                             'y': [car_df.iloc[0]['mpg'], car_df.iloc[0]['cyl'], car_df.iloc[0]['disp'], 
#                             car_df.iloc[0]['hp'], car_df.iloc[0]['drat'], car_df.iloc[0]['wt'], 
#                             car_df.iloc[0]['qsec'], car_df.iloc[0]['vs'], car_df.iloc[0]['am'], 
#                             car_df.iloc[0]['gear'], car_df.iloc[0]['carb']], 'type': 'bar', 'name': selected_car},
#                             {'x': ['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt', 'qsec', 'vs', 'am', 'gear', 'carb'], 
#                             'y': [compare_df.iloc[0]['mpg'], compare_df.iloc[0]['cyl'], compare_df.iloc[0]['disp'], 
#                             compare_df.iloc[0]['hp'], compare_df.iloc[0]['drat'], compare_df.iloc[0]['wt'], 
#                             compare_df.iloc[0]['qsec'], compare_df.iloc[0]['vs'], compare_df.iloc[0]['am'], 
#                             compare_df.iloc[0]['gear'], compare_df.iloc[0]['carb']], 'type': 'bar', 'name': selected_compare},
#                         ],
#                         'layout': {
#                             'title': 'Comparison Visualization',
#                             'marker'=dict(
#                                 color='rgb(158,202,225)',
#                                 line=dict(
#                                     color='rgb(8,48,107)',
#                                     width=1.5,
#                                 )
#                             ),
#                             'opacity'=0.6
#                         }
#                     },
#                     style={'color': '#bbadef'}
#                 )


if __name__ == '__main__':
    app.run_server(debug=True)