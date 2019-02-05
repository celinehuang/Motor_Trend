import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import pandas as pd

# making a dataframe from the tsv file, start reading data at line 5
df = pd.read_csv('./mtcars.tsv', delimiter='\t', encoding='utf-8',header=3)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)


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
        )], style={'width': '15%', 'float': 'left', 'display': 'inline-block', 'margin': '5px'})
])





if __name__ == '__main__':
    app.run_server(debug=True)