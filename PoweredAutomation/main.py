import base64
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc # Dash componetents
import pandas as pd
# from Pages import analytics_page, import_data
import spacy
import dash_daq as daq


app = dash.Dash(
    # #CSS External#
    external_stylesheets=[dbc.themes.MATERIA]
)

app.config.suppress_callback_exceptions = True

server = app.server

nlp = spacy.load('en_core_web_sm')
def most_frequent(List):
        return max(set(List), key = List.count)

buturl="https://img.icons8.com/color/48/000000/search.png"

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

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([  # Layout render
        dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [

                            dbc.Col(dbc.NavbarBrand("Powered Automation", className="ml-2")),
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
                                                'margin': '10px'  # 10px from all side
                                            }
                                        ),
                                        dcc.Upload(  # Upload component
                                            id='upload-data',  # Input for callback
                                            children=html.Div([
                                                'Drag and Drop or ',
                                                html.A('Select Files')  # Attribute
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

                                        dbc.Button("Goto Analytics Page",
                                                   color="primary",
                                                   className="ml-2",
                                                   href='/data_analysis',
                                                   id="goto-analytics"
                                                   ),

                                    ]
                                ),
                                style={'margin': '20px', 'padding': '16px'},  # Cardbody style
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
                                                'margin-bottom': '10px'  # 10px from all side
                                            }
                                        ),
                                        dcc.Dropdown(id='dynamic-drop',

                                                     multi=False,
                                                     placeholder='DB Server',

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

                                        dbc.Button("Connect",
                                                   color="primary",
                                                   className="ml-2",
                                                   style={'margin': '20px'},
                                                   href='data_analysis',
                                                   ),
                                    ]
                                ),
                                style={'margin': '20px', 'padding': '20px'},  # Cardbody style
                            )
                        )
                    ],
                    style={
                        'margin-top': "100px"  # Row style
                    }
                ),
            ]
        ),
    ],
    id='page-content'),
    html.Div([  # Layout render

        dbc.Navbar(
            [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [

                            dbc.Col(dbc.NavbarBrand("Powered Automation", className="ml-2")),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    # href="https://plot.ly",
                ),
                # dbc.NavbarToggler( id="navbar-toggler" ),
                dbc.Collapse(search_bar, id="navbar-collapse", navbar=True),
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

                                        html.H5("Fill missing values using below options or select columns",
                                                className="fill_missing"),
                                        dbc.Row([
                                            dbc.Col(
                                                [dcc.Dropdown(id='dynamic-reaplce',

                                                             multi=True,
                                                             placeholder='Filter Column',
                                                             ),

                                                 ]

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
                                                                   labelStyle={'display': 'inline-block',
                                                                               'text-align': 'justify'}
                                                                   # radio button with label
                                                                   ),

                                                    )
                                        ])
                                    ]
                                ),
                                style={
                                    'margin': '10px',
                                    'height': 'auto'  # Automatic hieght increase
                                },
                            ),
                        ),
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [

                                        html.H5("Drop all null value rows or Drop duplicates using below buttons",
                                                className="drop_missing"),

                                        # html.Div(id='dynamic-choice'),
                                        dcc.Dropdown(id='dynamic-choice',
                                                     multi=True,
                                                     placeholder='Filter Column'),

                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Drop All Null",
                                                        color="info",
                                                        className="mr-1",
                                                        id="dropall",
                                                        style={
                                                            'margin-top': '10px',
                                                            'padding': '5px'
                                                        },
                                                        size="sm"
                                                    ),
                                                    width=3
                                                ),
                                                dbc.Col(
                                                    dbc.Button(
                                                        "Drop Duplicate",
                                                        color="warning",
                                                        className="mr-1",
                                                        id="dropdup",
                                                        style={
                                                            'margin-top': '10px',
                                                            'padding': '5px'
                                                        },
                                                        size="sm"
                                                    ),
                                                    width=3
                                                ),
                                                dbc.Col(
                                                    daq.ToggleSwitch(
                                                        id='show_stat',
                                                        value=False,
                                                        label='Show/Hide Statistics',
                                                        labelPosition='left',
                                                        style={
                                                            'margin-top': '10px',
                                                            'padding': '5px'
                                                        },
                                                    ),
                                                )
                                            ]
                                        )

                                        # dbc.Button(
                                        #     "Show Statistics",
                                        #     color="#ebc334",
                                        #     className="mr-2",
                                        #     id="show_stat",
                                        #     n_clicks=0,
                                        #     # value="show",
                                        #     style={
                                        #         'margin-top': '10px'
                                        #     }
                                        # ),
                                    ]
                                ),
                                style={
                                    'margin': '10px',
                                    'height': 'auto'
                                },
                            )
                        )
                    ],
                    style={
                        'margin-top': "100px" # Row style
                     }
                ),

                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    [
                                        dbc.Row(
                                            [
                                                dbc.Col(
                                                    [
                                                        html.H5("Data Info", className="drop_missing", style={"text-align": "center"}),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [
                                                                        html.Ul(
                                                                            id="output"
                                                                        ),
                                                                    ]
                                                                ),
                                                                dbc.Col(
                                                                    [
                                                                        html.Ul(
                                                                            id="output-values"
                                                                        )
                                                                    ]
                                                                )
                                                            ]
                                                        )
                                                     ]
                                                ),
                                                dbc.Col(
                                                    [
                                                        html.H5("Column Data Type", className="drop_missing", style={"text-align": "center"}),
                                                        dbc.Row(
                                                            [
                                                                dbc.Col(
                                                                    [

                                                                        html.Ul(
                                                                            id="output-column"
                                                                        ),


                                                                    ]

                                                                ),

                                                                dbc.Col(
                                                                    [
                                                                        html.Ul(
                                                                            id="output-column-values"
                                                                        )
                                                                    ]

                                                                ),

                                                                dbc.Col(
                                                                    [
                                                                        html.Ul(
                                                                            id="output-col"
                                                                        ),
                                                                    ]
                                                                ),

                                                            ]
                                                        )
                                                    ],
                                                )
                                            ]
                                        )
                                    ]
                                ),
                                style={'margin': '10px'},
                            )
                        ),
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id='output-data-describe')
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id='output-graph1')
                        ),
                        dbc.Col(
                            html.Div(id='output-graph2')
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            html.Div(id='output-graph3')
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                dbc.CardBody(
                                    # html.H5("Custom CSS", className="card-title"),
                                    [
                                        dbc.Row(
                                            dbc.Col(
                                                [
                                                        dbc.Button(
                                                            "Download Data",
                                                            color="warning",
                                                            className="mr-1",
                                                            id="download_data",
                                                            style={
                                                                'margin-top': '10px',
                                                                'padding': '5px'
                                                            },
                                                            size="sm"
                                                        ),
                                                        dcc.RadioItems(
                                                            id="allradio",
                                                            options=[
                                                                {'label': 'All', 'value': 'allradiodata'},
                                                                {'label': 'Top 10 rows', 'value': 'head'},
                                                                {'label': 'Last 10 rows', 'value': 'tail'}
                                                            ],
                                                            value='allradiodata',
                                                            labelStyle={'display': 'inline-block','padding': '5px'},
                                                            inputStyle={
                                                                "margin-right": "5px",
                                                            },
                                                            inputClassName="checkmark",
                                                            style={"text-align": "right"},
                                                            className="myallradio"
                                                        ),
                                                    ]
                                            )
                                        ),
                                        html.Div(
                                            id='output-data-upload',
                                            className='table-wrapper-scroll-y my-custom-scrollbar'
                                        )
                                    ]
                                ),
                                style={'margin': '10px'},

                            )

                        )
                    ]
                ),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #                         html.H5("Graph 1", className="fill_missing"),
                #
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': '300px'
                #                 },
                #             ),
                #         ),
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #                         html.H5("Graph 2", className="drop_missing"),
                #
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': '300px'
                #                 },
                #             )
                #         )
                #     ]
                # ),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #                         html.H5("Graph 3", className="fill_missing"),
                #
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': '300px'
                #                 },
                #             ),
                #         ),
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #                         html.H5("Graph 4",
                #                                 className="drop_missing"),
                #
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': '300px'
                #                 },
                #             )
                #         )
                #     ]
                # ),
            ]
        )

    ],
    id="page-1-content-1"),

])

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


# Index Page callback
@app.callback([Output('page-content', 'style'),
               Output('page-1-content-1', 'style')],
              [
                  Input('url', 'pathname'),
               # Input('upload-data', 'contents'),
               # Input('upload-data', 'filename'),
               ])
def display_page(pathname):
    # if contents:
    if pathname == '/data_analysis':
        return {"display": "none"}, {"display": "inline"}
    else:
        return {"display": "inline"}, {"display": "none"}


@app.callback(
        Output('output-data-describe',"children"),
        [
            Input('upload-data', 'contents'),
            Input('upload-data', 'filename'),
            Input('show_stat', 'value')
        ],
)
def update_desc(contents, filename, show_stat):
    if contents is not None:
        print(show_stat)
        if show_stat:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            # pd.options.display.float_format = '${:,.4f}'.format
            dt = df.describe()
            dt=dt.reset_index()
            dt=dt.rename(columns={"index": "" })
            # dt = df.applymap( "${0:.f}".format )
            table =dbc.Card(
                dbc.CardBody(
                    [
                        dbc.Table.from_dataframe(dt,
                                                 className="all_data",
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 size="sm",
                                                 style={
                                                     "padding": "0",
                                                     "width": "100"
                                                 }
                                                 )
                        ]
                ),
                style={'margin': '10px'},
            )

            return table
        else:
            return None
    else:
        return None




@app.callback(
    [
        Output("output", "children"),
        Output("output-values", "children"),
        Output("output-column", "children"),
        Output("output-column-values", "children"),
        Output("output-col", "children"),



    ], # Return Childern value
    [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename')
    ],
)
def update_output(contents, filename):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        mis = df.columns[df.isnull().any()].tolist()
        # mis = str(mis).replace('[', '').replace(']', '').replace("", '').replace(':', "").replace("'", '')

        col = df.columns
        s = []
        for i in col:
            lst = []
            for index, rows in df.iterrows():
                doc = nlp(str(rows[i]))

                for ent in doc.ents:
                    test_data = i, ent.label_
                    lst.append(test_data[1])
            try:
                s.append((i, most_frequent(lst)))
            except:
                s.append((i, 'CATEGORY'))

        dt = df.dtypes
        dlist = [str( dt[1] ) for dt in dt.iteritems()]
        print(s)

        # dt1=dbc.Table.from_dataframe(dt)



        # for ent in s:
        #     print(ent[0], ent[1])


        columnList = [
            "Number of columns",
            "Number of rows",
            "Columns with empty cell",
            "Total duplicate rows",
            "Missing Percentage"

        ]
        percent_missing = df.isnull().sum() / df.shape[0]
        per = (sum( percent_missing ) / len( df.columns ))
        per = "%.3f" % per
        print(per)

        columnValueList = [
            len(df.columns),
            len(df),
            len(mis),
            df.duplicated().sum(),
            per


        ]

        return [html.Li(i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'}) for i in columnList], \
               [html.Li(i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'}) for i in columnValueList],\
               [html.Li(i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'}) for i in [ent[0] for ent in s]], \
               [html.Li(i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'}) for i in [ent[1] for ent in s]],\
               [html.Li( i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'} ) for i in [str( dt[1] ) for dt in dt.iteritems()]]


    else:
        columnList = [
            "Number of columns",
            "Number of rows",
            "Columns with empty cell",
            "Total duplicate rows"
        ]
        return [html.Li(i, style={"list-style": "none", "font-size": "13px", 'font-weight': '430'}) for i in columnList], None, None, None, None

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

@app.callback(dash.dependencies.Output('output-data-upload', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
                  Input("slct_year", "value"),
                  Input("dropall", "n_clicks"),
                  Input("dropdup", "n_clicks"),
                  Input("dynamic-choice", "value"),
                  Input("dynamic-reaplce", "value"),
                  Input("allradio", "value")

                  # Input(component_id='dynamic-choice', component_property='value')
              ]
              )
def page_1_dropdown(contents, filename, is_selected, dropall, dropdup, multiValues,dynamic_choice,radioall):
    print(radioall)
    if contents is not None and is_selected == "all":
        if dropall:
            if len(multiValues) != 0:
                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                df = df.dropna(axis=0, subset=multiValues)

                # table = html.Div([
                #     html.H5(filename),
                #     dash_table.DataTable(
                #         data=df.to_dict('rows'),
                #         columns=[{'name': i,
                #                   'id': i,
                #                   'deletable': True,
                #                   'renamable': True}
                #                  for i in df.columns
                #                  ],
                #         page_size=20,
                #         fixed_rows={'headers': True, 'data': 0},
                #         style_table={
                #             'height': '400px',
                #             'overflowY': 'auto',
                #         },
                #         style_cell_conditional=[
                #             {
                #                 'if': {'column_id': i},
                #                 'textAlign': 'center'
                #             } for i in df.columns
                #         ],
                #         editable=True,
                #         row_deletable=True,
                #         filter_action="native",
                #         sort_action="native",
                #     ),
                # ])
                table = dbc.Table.from_dataframe(df,
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 # size="sm",
                                                 # className='table-wrapper-scroll-y my-custom-scrollbar',
                                                 style={
                                                     "padding": "0",
                                                 })
            else:
                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                df = df.dropna()

                # table = html.Div([
                #     html.H5(filename),
                #     dash_table.DataTable(
                #         data=df.to_dict('rows'),
                #         columns=[{'name': i,
                #                   'id': i,
                #                   'deletable': True,
                #                   'renamable': True}
                #                  for i in df.columns
                #                  ],
                #         # page_size=20,
                #         fixed_rows={'headers': True, 'data': 0},
                #         style_table={
                #             'height': '300px',
                #             'overflowY': 'auto',
                #         },
                #         style_cell_conditional=[
                #             {
                #                 'if': {'column_id': i},
                #                 'textAlign': 'center'
                #             } for i in df.columns
                #         ],
                #         editable=True,
                #         row_deletable=True,
                #         filter_action="native",
                #         sort_action="native",
                #     ),
                # ])

                table = dbc.Table.from_dataframe(df,
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 # size="sm",
                                                 # className='table-wrapper-scroll-y my-custom-scrollbar',
                                                 style={
                                                     "padding": "0",
                                                 })

            return table
        elif dropdup:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            df = df.drop_duplicates(keep='first')

            # table = html.Div([
            #     html.H5(filename),
            #     dash_table.DataTable(
            #         data=df.to_dict('records'),
            #         columns=[{'name': i,
            #                   'id': i,
            #                   'deletable': True,
            #                   'renamable': True}
            #                  for i in df.columns
            #                  ],
            #         page_size=20,
            #         fixed_rows={'headers': True, 'data': 0},
            #         style_table={
            #             'height': '300px',
            #             'overflowY': 'auto',
            #         },
            #         style_cell_conditional=[
            #             {
            #                 'if': {'column_id': i},
            #                 'textAlign': 'center'
            #             } for i in df.columns
            #         ],
            #         editable=True,
            #         row_deletable=True,
            #         filter_action="native",
            #         sort_action="native",
            #         # fixed_rows={'headers': True, 'data': 0},
            #
            #         # style_as_list_view=True,
            #     ),
            #
            #     # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
            #
            #     # dcc.Graph(id='adding-rows-graph'),
            #     html.Hr(),
            #
            #     # html.Div('Raw Content'),
            #     # html.Pre(contents[0:200] + '...', style={
            #     #     'whiteSpace': 'pre-wrap',
            #     #     'wordBreak': 'break-all'
            #     # })
            # ])

            table = dbc.Table.from_dataframe(df,
                                             bordered=True,
                                             hover=True,
                                             responsive=True,
                                             striped=True,
                                             # size="sm",
                                             # className='table-wrapper-scroll-y my-custom-scrollbar',
                                             style={
                                                 "padding": "0",
                                             })

            return table

        else:
            if radioall=='allradiodata':

                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                table = dbc.Table.from_dataframe(df,
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 # size="sm",
                                                 # className='table-wrapper-scroll-y my-custom-scrollbar',
                                                 style={
                                                     "padding": "0",
                                                 })

                # table = html.Div([
                #     html.H5(filename),
                #     dash_table.DataTable(
                #         data=df.to_dict('rows'),
                #         columns=[{'name': i,
                #                   'id': i,
                #                   'deletable': True,
                #                   'renamable': True}
                #                  for i in df.columns
                #                  ],
                #         # page_size=20,
                #         fixed_rows={'headers': True, 'data': 0},
                #         style_table={
                #             'height': '300px',
                #             'overflowY': 'auto',
                #         },
                #         style_cell={  # ensure adequate header width when text is shorter than cell's text
                #             'minWidth': 95, 'maxWidth': 95, 'width': 95
                #         },
                #         style_cell_conditional=[
                #             {
                #                 'if': {'column_id': i},
                #                 'textAlign': 'center'
                #             } for i in df.columns
                #         ],
                #         style_data={  # overflow cells' content into multiple lines
                #             'whiteSpace': 'normal',
                #             'height': 'auto'
                #         },
                #         editable=True,
                #         row_deletable=True,
                #         filter_action="native",
                #         sort_action="native",
                #
                #     ),
                #
                #     # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
                #
                #     # dcc.Graph(id='adding-rows-graph'),
                #     # html.Hr(),
                #
                #     # html.Div('Raw Content'),
                #     # html.Pre(contents[0:200] + '...', style={
                #     #     'whiteSpace': 'pre-wrap',
                #     #     'wordBreak': 'break-all'
                #     # })
                # ])

                return table
            elif radioall=='head':
                contents = contents[0]
                filename = filename[0]
                df = parse_data( contents, filename )
                df=df.head(10)

                table = dbc.Table.from_dataframe(df,
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 # size="sm",
                                                 # className='table-wrapper-scroll-y my-custom-scrollbar',
                                                 style={
                                                     "padding": "0",
                                                 })

                return table
            elif radioall=='tail':
                contents = contents[0]
                filename = filename[0]
                df = parse_data( contents, filename )
                df=df.tail(10)

                table = dbc.Table.from_dataframe(df,
                                                 bordered=True,
                                                 hover=True,
                                                 responsive=True,
                                                 striped=True,
                                                 # size="sm",
                                                 # className='table-wrapper-scroll-y my-custom-scrollbar',
                                                 style={
                                                     "padding": "0",
                                                 })

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

        # table = html.Div([
        #     html.H5(filename),
        #     dash_table.DataTable(
        #         data=df.to_dict('rows'),
        #         columns=[{'name': i,
        #                   'id': i,
        #                   'deletable': True,
        #                   'renamable': True}
        #                  for i in df.columns
        #                  ],
        #         page_size=20,
        #         fixed_rows={'headers': True, 'data': 0},
        #         style_table={
        #             'height': '300px',
        #             'overflowY': 'auto',
        #         },
        #         style_cell_conditional=[
        #             {
        #                 'if': {'column_id': i},
        #                 'textAlign': 'center'
        #             } for i in df.columns
        #         ],
        #         editable=True,
        #         row_deletable=True,
        #         filter_action="native",
        #         sort_action="native",
        #         # style_as_list_view=True,
        #     ),
        #
        #     # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        #
        #     # dcc.Graph(id='adding-rows-graph'),
        #     html.Hr(),
        #
        #     # html.Div('Raw Content'),
        #     # html.Pre(contents[0:200] + '...', style={
        #     #     'whiteSpace': 'pre-wrap',
        #     #     'wordBreak': 'break-all'
        #     # })
        # ])
        table = dbc.Table.from_dataframe(df,
                                         bordered=True,
                                         hover=True,
                                         responsive=True,
                                         striped=True,
                                         # size="sm",
                                         # className='table-wrapper-scroll-y my-custom-scrollbar',
                                         style={
                                             "padding": "0",
                                         })

        return table
    elif contents is not None and is_selected == "mode":
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_choice:
            mode = df[i].mode()
            df[i] = df[i].fillna(mode)

        # table = html.Div([
        #     html.H5(filename),
        #     dash_table.DataTable(
        #         data=df.to_dict('rows'),
        #         columns=[{'name': i,
        #                   'id': i,
        #                   'deletable': True,
        #                   'renamable': True}
        #                  for i in df.columns
        #                  ],
        #         page_size=20,
        #         fixed_rows={'headers': True, 'data': 0},
        #         style_table={
        #             'height': '300px',
        #             'overflowY': 'auto',
        #         },
        #         style_cell_conditional=[
        #             {
        #                 'if': {'column_id': i},
        #                 'textAlign': 'center'
        #             } for i in df.columns
        #         ],
        #         editable=True,
        #         row_deletable=True,
        #         filter_action="native",
        #         sort_action="native",
        #         # style_as_list_view=True,
        #     ),
        #
        #     # html.Button('Add Row', id='editing-rows-button', n_clicks=0),
        #
        #     # dcc.Graph(id='adding-rows-graph'),
        #     html.Hr(),
        #
        #     # html.Div('Raw Content'),
        #     # html.Pre(contents[0:200] + '...', style={
        #     #     'whiteSpace': 'pre-wrap',
        #     #     'wordBreak': 'break-all'
        #     # })
        # ])

        table = dbc.Table.from_dataframe(df,
                                         bordered=True,
                                         hover=True,
                                         responsive=True,
                                         striped=True,
                                         # size="sm",
                                         # className='table-wrapper-scroll-y my-custom-scrollbar',
                                         style={
                                             "padding": "0",
                                         })

        return table
    elif contents is not None and is_selected == "median":
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_choice:
            median = df[i].median()
            df[i] = df[i].fillna(median)

        # table = html.Div([
        #     html.H5(filename),
        #     dash_table.DataTable(
        #         data=df.to_dict('rows'),
        #         columns=[{'name': i,
        #                   'id': i,
        #                   'deletable': True,
        #                   'renamable': True}
        #                  for i in df.columns
        #                  ],
        #         page_size=20,
        #         fixed_rows={'headers': True, 'data': 0},
        #         style_table={
        #             'height': '300px',
        #             'overflowY': 'auto',
        #         },
        #         style_cell_conditional=[
        #             {
        #                 'if': {'column_id': i},
        #                 'textAlign': 'center'
        #             } for i in df.columns
        #         ],
        #         editable=True,
        #         row_deletable=True,
        #         filter_action="native",
        #         sort_action="native",
        #         # style_as_list_view=True,
        #     ),
        #
        #     html.Hr(),
        #
        # ])

        table = dbc.Table.from_dataframe(df,
                                         bordered=True,
                                         hover=True,
                                         responsive=True,
                                         striped=True,
                                         # size="sm",
                                         # className='table-wrapper-scroll-y my-custom-scrollbar',
                                         style={
                                             "padding": "0",
                                         })

        return table



if __name__ == '__main__':
    app.run_server(debug=True)