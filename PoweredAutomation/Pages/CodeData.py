import base64
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc # Dash componetents
# from dash.dependencies import Input, Output, ALL, State, MATCH, ALLSMALLER
import pandas as pd

app = dash.Dash(
    # external_stylesheets=[dbc.themes.SOLAR]
    # #CSS External#
    external_stylesheets=[dbc.themes.MATERIA]
)
server = app.server

colors = {  # Not in use for chart
    "graphBackground": "#F5F5F5",
    "background": "#ffffff",
    "text": "#000000"
}

# url_bar_and_content_div = html.Div([
#     dcc.Location(id='url', refresh=False),
#     html.Div(id='output-data-upload')
# ])

#
# layout_page_2 = html.Div([
#     html.H2('Page 2'),
#
#     html.Div(id='page-2-display-value'),
#     html.Br(),
#     dcc.Link('Navigate to "/"', href='/'),
#
# ])

# app.layout = url_bar_and_content_div
#
# # "complete" layout
# app.validation_layout = html.Div([
#     url_bar_and_content_div,
#     layout_page_2,
# ])

def parse_data(contents, filename):  #CSV or Excel read and return DF
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+')
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return df





app.layout = html.Div([    # Layout render

dbc.Navbar(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [

                        dbc.Col( dbc.NavbarBrand( "Powered Automation", className="ml-2" ) ),
                    ],
                    align="center",
                    no_gutters=True,
                ),
                # href="https://plot.ly",
            ),
            # dbc.NavbarToggler( id="navbar-toggler" ),
            # dbc.Collapse( search_bar, id="navbar-collapse", navbar=True ),
        ],
        color="White",
        dark=False,
        fixed='top'
    ),


    dbc.Container(
        [
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(  ## H5 Header size H1, H2,H3
                                        "Import your Excel or CSV file for analytics",
                                        className="importfile",
                                        style={
                                            'margin': '10px' # 10px from all side
                                        }
                                    ),
                                    dcc.Upload( # Upload component
                                        id='upload-data', # Input for callback
                                        children=html.Div([
                                            'Drag and Drop or ',
                                            html.A('Select Files')# Attribute
                                        ]),

                                        style={
                                            'width': '100%',
                                            'height': '220px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '10px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },

                                        # Allow multiple files to be uploaded
                                        multiple=True


                                    ),

                                    dbc.Button("Goto Analytics Page", color="primary", className="ml-2",
                                               ),

                                ]
                            ),
                            style={'margin': '20px'}, # Cardbody style
                        )
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5(  ## H5 Header size H1, H2,H3
                                        "Connect with Database",
                                        className="dbfile",
                                        style={
                                            'margin': '10px'  # 10px from all side
                                        }
                                    ),
                                        dcc.Dropdown( id='dynamic-drop',

                                                        multi=False,
                                                        placeholder='Filter Column',

                                                        options=[
                                                               {'label': 'Postgres', 'value': 'all'},
                                                               {'label': 'MS Acess', 'value': 'ms'},
                                                               {'label': 'SQL Server', 'value': 'sqlser'},
                                                               # {'label': 'Median', 'value': 'median'}
                                                         ],
                                                        ),
                                        dbc.Input(type="search", placeholder="Database Name"),
                                        dbc.Input(type="search", placeholder="User Name"),
                                        dbc.Input(type="search", placeholder="Password"),







                                    dbc.Button( "Connect", color="primary", className="ml-2",
                                                style={'margin': '20px'}
                                                ),

                                ]
                            ),
                            style={'margin': '20px'},  # Cardbody style
                        )
                    )
                ],
                style={
                    'margin-top': "80px" # Row style
                }
            ),
            ]


    )
    ])




if __name__ == '__main__':
    app.run_server(debug=True)
