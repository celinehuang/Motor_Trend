import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

# making a dataframe from the tsv file, start reading data at line 5
df = pd.read_csv('./mtcars.tsv', delimiter='\t', encoding='utf-8', header=3)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


markdown_text = '''**The data was extracted from the 1974 *Motor Trend* US magazine, and comprises fuel 
consumption and 10 aspects of automobile design and performance for 32 automobiles (1973–74 models).**'''

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

index_page = html.Div([
    dcc.Link('Click here to View All Automobile Design and Performance',
             href='/models-design-and-performance'),
    html.Br(),
    dcc.Link('Click here to Compare Automobile Models',
             href='/compare-models'),
])


def generate_table(dataframe, max_rows=100):
    return html.Table(
        # Header
        [html.Tr([html.Th(col) for col in dataframe.columns])] +

        # Body
        [html.Tr([
            html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
        ]) for i in range(min(len(dataframe), max_rows))]
    )


view_all_layout = html.Div(children=[
    html.H4(children='Automobile Design and Performance'),
    generate_table(df),
    html.Div(id='page-1-content'),
    html.Br(),
    dcc.Link('Compare Automobile Models', href='/compare-models'),
    html.Br(),
    dcc.Link('Go back to home', href='/'),
])

compare_models_layout = html.Div(children=[
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
    # html.Div([
    #     html.Label(),
    #     dcc.RadioItems(
    #     options=[
    #         {'label': 'See All Models'}
    #     ],
    # )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'}),
    html.Div([html.Div([], id='graph', style={'float': 'left'})]),
    html.Div([dcc.Markdown(
        className='absolute',
        children=markdown_text
    )]),
    html.Div(id='page-2-content'),
    html.Br(),
    dcc.Link('View All Automobile Design and Performance', href='/models-design-and-performance'),
    html.Br(),
    dcc.Link('Go back to home', href='/')
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
                                x=['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt',
                                    'qsec', 'vs', 'am', 'gear', 'carb'],
                                y=[car_df.iloc[0]['mpg'], car_df.iloc[0]['cyl'], car_df.iloc[0]['disp'],
                                   car_df.iloc[0]['hp'], car_df.iloc[0]['drat'], car_df.iloc[0]['wt'],
                                   car_df.iloc[0]['qsec'], car_df.iloc[0]['vs'], car_df.iloc[0]['am'],
                                    car_df.iloc[0]['gear'], car_df.iloc[0]['carb']],
                                name=selected_car,
                                marker=go.bar.Marker(
                                    color='rgb(196, 152, 255)'
                                )
                            ),
                            go.Bar(
                                x=['mpg', 'cyl', 'disp', 'hp', 'drat', 'wt',
                                   'qsec', 'vs', 'am', 'gear', 'carb'],
                                y=[compare_df.iloc[0]['mpg'], compare_df.iloc[0]['cyl'], compare_df.iloc[0]['disp'],
                                   compare_df.iloc[0]['hp'], compare_df.iloc[0]['drat'], compare_df.iloc[0]['wt'],
                                   compare_df.iloc[0]['qsec'], compare_df.iloc[0]['vs'], compare_df.iloc[0]['am'],
                                   compare_df.iloc[0]['gear'], compare_df.iloc[0]['carb']],
                                name=selected_compare,
                                marker=go.bar.Marker(
                                    color='rgb(245, 184, 240)'
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

# Update the index
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/models-design-and-performance':
        return view_all_layout
    elif pathname == '/Compare Automobile Models':
        return compare_models_layout
    else:
        return index_page


if __name__ == '__main__':
    app.run_server(debug=True)
