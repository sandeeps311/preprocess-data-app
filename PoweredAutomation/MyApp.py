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

# external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

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


SIDEBAR_STYLE = {     ### Powered Automation
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}  # Not in use

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}




sidebar = html.Div( # Not insue
    [
        html.H2("Sidebar", className="display-4"),
        html.Hr(),
        html.P(
            "A simple sidebar layout with navigation links", className="lead"
        ),
        dbc.Nav(
            [
                dbc.NavLink("Page 1", href="/page-1", id="page-1-link"),
                dbc.NavLink("Page 2", href="/page-2", id="page-2-link"),
                dbc.NavLink("Page 3", href="/page-3", id="page-3-link"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)
buturl="https://img.icons8.com/color/48/000000/search.png"
NewDF = None
search_bar = dbc.Row(
    [
        dbc.Col(dbc.Input(type="search", placeholder="Type a query to perform operations on data and change graph"),style={

                                            'margin-left': '120px'},),
        # dbc.Col(
        #     dbc.Button("Search", color="primary", className="ml-2",),
        #
        #     width="auto",
        # ),
        html.Img(src=buturl, height="40px")
    ],
    no_gutters=True,
    className="col-md-8",
    align="center",

)


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
            dbc.Collapse( search_bar, id="navbar-collapse", navbar=True ),
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
                                            'height': '60px',
                                            'lineHeight': '60px',
                                            'borderWidth': '1px',
                                            'borderStyle': 'dashed',
                                            'borderRadius': '5px',
                                            'textAlign': 'center',
                                            'margin': '10px'
                                        },
                                        # Allow multiple files to be uploaded
                                        multiple=True
                                    ),
                                ]
                            ),
                            style={'margin': '10px'}, # Cardbody style
                        )
                    )
                ],
                style={
                    'margin-top': "80px" # Row style
                }
            ),

            # dbc.Row(
            #     [
            #         dbc.Col(
            #             dbc.Card(
            #                 dbc.CardBody(
            #                     [
            #                         html.H5("Type a query to perform operations on data and change graph", className="typequery"),
            #
            #                     ]
            #                 ),
            #                 style={'margin': '10px'},
            #             )
            #         )
            #     ]
            # ),

            dbc.Row(
                [
                    dbc.Col(
                            dbc.Card(
                                  dbc.CardBody(
                                      [

                                          html.H5("Fill missing values using below options or select columns", className="fill_missing"),
                                          dbc.Row([
                                          dbc.Col(
                                                dcc.Dropdown( id='dynamic-reaplce',

                                                        multi=True,
                                                        placeholder='Filter Column',
                                                        ),

                                          ),
                                              dbc.Col(dbc.RadioItems(id="slct_year",
                                                         # className="radio-inline",
                                                         options=[
                                                               {'label': 'Show All', 'value': 'all'},
                                                               {'label': 'Mean', 'value': 'mean'},
                                                               {'label': 'Mode', 'value': 'mode'},
                                                               {'label': 'Median', 'value': 'median'}
                                                         ],
                                                         value='all',
                                                         labelStyle={'display': 'inline-block', 'text-align': 'justify'} # radio button with label
                                                         ),

                                              )
                                              ])
                                      ]
                                  ),
                                  style={
                                      'margin': '10px',
                                      'height' :'auto' # Automatic hieght increase
                                      },
                            ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [

                                    html.H5("Drop all null value rows or Drop duplicates using below buttons", className="drop_missing"),

                                    # html.Div(id='dynamic-choice'),
                                    dcc.Dropdown(id='dynamic-choice',
                                                multi = True,
                                                placeholder='Filter Column'),

                                    dbc.Button(
                                        "Drop All Null",
                                        color="info",
                                        className="mr-1",
                                        id="dropall",
                                        style={
                                            'margin-top': '10px'
                                        }
                                    ),
                                    dbc.Button(
                                        "Drop Duplicate",
                                        color="warning",
                                        className="mr-2",
                                        id="dropdup",
                                        style={
                                            'margin-top':'10px'
                                        }
                                    ),
                                ]
                            ),
                            style={
                                'margin': '10px',
                                'height' :'auto'
                            },
                        )
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Your Data having Null values", className="drop_missing"),
                                    html.Div(id="output"),
                                 ]
                            ),
                            style={'margin': '10px'},
                        )
                    )
                ]
            ),

            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                # html.H5("Custom CSS", className="card-title"),
                                html.Div(id='output-data-upload')
                                # dbc.Table(id='output-data-upload',
                                #           )
                            ),
                            style={'margin': '10px'},

                        )

                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                            dbc.Card(
                                  dbc.CardBody(
                                      [
                                          html.H5("Graph 1", className="fill_missing"),

                                      ]
                                  ),
                                  style={
                                      'margin': '10px',
                                      'height': '300px'
                                      },
                            ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Graph 2", className="drop_missing"),

                                ]
                            ),
                            style={
                                'margin': '10px',
                                'height' :'300px'
                            },
                        )
                    )
                ]
            ),
            dbc.Row(
                [
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Graph 3", className="fill_missing"),

                                ]
                            ),
                            style={
                                'margin': '10px',
                                'height': '300px'
                            },
                        ),
                    ),
                    dbc.Col(
                        dbc.Card(
                            dbc.CardBody(
                                [
                                    html.H5("Graph 4",
                                            className="drop_missing"),

                                ]
                            ),
                            style={
                                'margin': '10px',
                                'height': '300px'
                            },
                        )
                    )
                ]
            ),
        ]
    )

    # dcc.Location(id='url', refresh=False),
    # html.Div(id='output-data-upload')
])

@app.callback(
    Output("output", "children"), # Return Childern value
    [Input('upload-data', 'contents'),
    Input('upload-data', 'filename')],
)
def update_output(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        mis = df.columns[df.isnull().any()].tolist()
        mis = str(mis).replace('[', '').replace(']', '').replace("", '').replace(':', "").replace("'", '')

        if mis == "" or mis is None:
            return None
        else:
            return u'{}  Columns having missing values.'.format(mis)
    else:
        return None

# @app.callback(Output('Mygraph', 'figure'), [
#     Input('upload-data', 'contents'),
#     Input('upload-data', 'filename')
# ])
# def update_graph(contents, filename):
#
#     fig = {
#         'layout': go.Layout(
#             plot_bgcolor=colors["graphBackground"],
#             paper_bgcolor=colors["graphBackground"]
#         )
#     }
#
#     if contents:
#         contents = contents[0]
#         filename = filename[0]
#         df = parse_data(contents, filename)
#         df = df.set_index(df.columns[0])
#         fig['data'] = df.iplot(
#             asFigure=True, kind='scatter', mode='lines+markers', size=1)
#
#     return fig

@app.callback(Output('dynamic-reaplce', 'options'),
              [
                  Input( 'upload-data', 'contents' ),
                  Input( 'upload-data', 'filename' ),
              ],
              )

def update_multi(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        mis = df.columns[df.isnull().any()].tolist()
        # mis = str(mis).replace('[', '').replace(']', '').replace("", '').replace(':', "").replace("'", '')

        if mis is not None or mis != "":
            return [{'label': i, 'value': i} for i in sorted(list(mis))]
        else:
            return []
    else:

        return []



@app.callback(Output('dynamic-choice', 'options'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
              ],
              )
def update_multi(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        mis = df.columns[df.isnull().any()].tolist()
        # mis = str(mis).replace('[', '').replace(']', '').replace("", '').replace(':', "").replace("'", '')

        if mis is not None or mis != "":
            return [{'label': i, 'value': i} for i in sorted(list(mis))]
        else:
            return []
    else:

        return []


@app.callback(Output('output-data-upload', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
                  Input("slct_year", "value"),
                  Input("dropall", "n_clicks"),
                  Input("dropdup", "n_clicks"),
                  Input("dynamic-choice", "value"),
                  Input("dynamic-reaplce", "value")
                  # Input(component_id='dynamic-choice', component_property='value')
              ])
def update_table(contents, filename, is_selected, dropall, dropdup, multiValues,dynamic_choice ):

    print(multiValues)
    table = html.Div()

    if contents is not None and is_selected == "all":
        if dropall:
            if len(multiValues) != 0:
                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                df = df.dropna(axis=0, subset=multiValues)

                table = html.Div([
                    html.H5(filename),
                    dash_table.DataTable(
                        data=df.to_dict('rows'),
                        columns=[{'name': i,
                                  'id': i,
                                  'deletable': True,
                                  'renamable': True}
                                 for i in df.columns
                                 ],
                        page_size=20,
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={
                            'height': '300px',
                            'overflowY': 'auto',
                        },
                        style_cell_conditional=[
                            {
                                'if': {'column_id': i},
                                'textAlign': 'center'
                            } for i in df.columns
                        ],
                        editable=True,
                        row_deletable=True,
                        filter_action="native",
                        sort_action="native",
                    ),
                ])
            else:
                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                df = df.dropna()

                table = html.Div([
                    html.H5(filename),
                    dash_table.DataTable(
                        data=df.to_dict('rows'),
                        columns=[{'name': i,
                                  'id': i,
                                  'deletable': True,
                                  'renamable': True}
                                 for i in df.columns
                                 ],
                        page_size=20,
                        fixed_rows={'headers': True, 'data': 0},
                        style_table={
                            'height': '300px',
                            'overflowY': 'auto',
                        },
                        style_cell_conditional=[
                            {
                                'if': {'column_id': i},
                                'textAlign': 'center'
                            } for i in df.columns
                        ],
                        editable=True,
                        row_deletable=True,
                        filter_action="native",
                        sort_action="native",
                    ),
                ])

            return table
        elif dropdup:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            df = df.drop_duplicates(keep='first')

            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('records'),
                    columns=[{'name': i,
                              'id': i,
                              'deletable': True,
                              'renamable': True}
                             for i in df.columns
                             ],
                    page_size=20,
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={
                        'height': '300px',
                        'overflowY': 'auto',
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': i},
                            'textAlign': 'center'
                        } for i in df.columns
                    ],
                    editable=True,
                    row_deletable=True,
                    filter_action="native",
                    sort_action="native",
                    # fixed_rows={'headers': True, 'data': 0},

                    # style_as_list_view=True,
                ),

                # html.Button('Add Row', id='editing-rows-button', n_clicks=0),

                # dcc.Graph(id='adding-rows-graph'),
                html.Hr(),

                # html.Div('Raw Content'),
                # html.Pre(contents[0:200] + '...', style={
                #     'whiteSpace': 'pre-wrap',
                #     'wordBreak': 'break-all'
                # })
            ])

            return table
        else:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)


            table = html.Div([
                html.H5(filename),
                dash_table.DataTable(
                    data=df.to_dict('rows'),
                    columns=[{'name': i,
                              'id': i,
                              'deletable': True,
                              'renamable': True}
                             for i in df.columns
                             ],
                    # page_size=20,
                    fixed_rows={'headers': True, 'data': 0},
                    style_table={
                        'height': '300px',
                        'overflowY': 'auto',
                    },
                    style_cell={  # ensure adequate header width when text is shorter than cell's text
                        'minWidth': 95, 'maxWidth': 95, 'width': 95
                    },
                    style_cell_conditional=[
                        {
                            'if': {'column_id': i},
                            'textAlign': 'center'
                        } for i in df.columns
                    ],
                    style_data={  # overflow cells' content into multiple lines
                        'whiteSpace': 'normal',
                        'height': 'auto'
                    },
                    editable=True,
                    row_deletable=True,
                    filter_action="native",
                    sort_action="native",

                ),

                # html.Button('Add Row', id='editing-rows-button', n_clicks=0),

                # dcc.Graph(id='adding-rows-graph'),
                # html.Hr(),

                # html.Div('Raw Content'),
                # html.Pre(contents[0:200] + '...', style={
                #     'whiteSpace': 'pre-wrap',
                #     'wordBreak': 'break-all'
                # })
            ])

            return table
    elif contents is not None and is_selected == "mean":
        print(dynamic_choice)
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_choice:
            mean = df[i].mean()
            df[i] = df[i].fillna(mean)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i,
                          'id': i,
                          'deletable': True,
                          'renamable': True}
                         for i in df.columns
                         ],
                page_size=20,
                fixed_rows={'headers': True, 'data': 0},
                style_table={
                    'height': '300px',
                    'overflowY': 'auto',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': i},
                        'textAlign': 'center'
                    } for i in df.columns
                ],
                editable=True,
                row_deletable=True,
                filter_action="native",
                sort_action="native",
                # style_as_list_view=True,
            ),

            # html.Button('Add Row', id='editing-rows-button', n_clicks=0),

            # dcc.Graph(id='adding-rows-graph'),
            html.Hr(),

            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #     'whiteSpace': 'pre-wrap',
            #     'wordBreak': 'break-all'
            # })
        ])

        return table
    elif contents is not None and is_selected == "mode":
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_choice:
            mode = df[i].mode()
            df[i] = df[i].fillna(mode)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i,
                          'id': i,
                          'deletable': True,
                          'renamable': True}
                         for i in df.columns
                         ],
                page_size=20,
                fixed_rows={'headers': True, 'data': 0},
                style_table={
                    'height': '300px',
                    'overflowY': 'auto',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': i},
                        'textAlign': 'center'
                    } for i in df.columns
                ],
                editable=True,
                row_deletable=True,
                filter_action="native",
                sort_action="native",
                # style_as_list_view=True,
            ),

            # html.Button('Add Row', id='editing-rows-button', n_clicks=0),

            # dcc.Graph(id='adding-rows-graph'),
            html.Hr(),

            # html.Div('Raw Content'),
            # html.Pre(contents[0:200] + '...', style={
            #     'whiteSpace': 'pre-wrap',
            #     'wordBreak': 'break-all'
            # })
        ])

        return table
    elif contents is not None and is_selected == "median":
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_choice:
            median = df[i].median()
            df[i] = df[i].fillna(median)

        table = html.Div([
            html.H5(filename),
            dash_table.DataTable(
                data=df.to_dict('rows'),
                columns=[{'name': i,
                          'id': i,
                          'deletable': True,
                          'renamable': True}
                         for i in df.columns
                         ],
                page_size=20,
                fixed_rows={'headers': True, 'data': 0},
                style_table={
                    'height': '300px',
                    'overflowY': 'auto',
                },
                style_cell_conditional=[
                    {
                        'if': {'column_id': i},
                        'textAlign': 'center'
                    } for i in df.columns
                ],
                editable=True,
                row_deletable=True,
                filter_action="native",
                sort_action="native",
                # style_as_list_view=True,
            ),

            html.Hr(),

        ])

        return table

if __name__ == '__main__':
    app.run_server(debug=True)
