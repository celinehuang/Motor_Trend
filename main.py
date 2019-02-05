import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd

# making a dataframe from the tsv file, start reading data at line 5
df = pd.read_csv('./mtcars.tsv', delimiter='\t', encoding='utf-8',header=3)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

markdown_text = '''**The data was extracted from the 1974 *Motor Trend* US magazine, and comprises fuel 
consumption and 10 aspects of automobile design and performance for 32 automobiles (1973–74 models).**'''

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
        html.Div([html.Div([], id='graph', style={'float': 'left'})]),
        html.Div([dcc.Markdown(
            className='absolute',
            children=markdown_text
            )])
])

# Callback to update the graph based on selected model of automobile
@app.callback(
    dash.dependencies.Output('graph', 'children'),
    [dash.dependencies.Input('car-dropdown', 'value')])
def callback_a(selected_car):
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



if __name__ == '__main__':
    app.run_server(debug=True)