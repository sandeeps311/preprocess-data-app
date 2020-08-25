import base64
import io
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc # Dash componetents
import pandas as pd
import spacy
import dash_daq as daq
import plotly.express as px
import numpy as np


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
# fillmiss= html.Div(
#     [
#         # html.H5( "Fill missing values using below options or select columns",
#         #      className="fill_missing" ),
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H5("Select columns"),
#                         dcc.Dropdown(
#                             id='dynamic-reaplce',
#                             multi=True,
#                             placeholder='Filter Column',
#                         ),
#                      ]
#                 ),
#                 # dbc.Col( dbc.RadioItems( id="slct_year",
#                 #                          # className="radio-inline",
#                 #                          options=[
#                 #                              {'label': 'Show All', 'value': 'all'},
#                 #                              {'label': 'Mean', 'value': 'mean'},
#                 #                              {'label': 'Mode', 'value': 'mode'},
#                 #                              {'label': 'Median', 'value': 'median'}
#                 #                          ],
#                 #                          value='all',
#                 #                          labelStyle={'display': 'inline-block',
#                 #                                      'text-align': 'justify'}
#                 #                          # radio button with label
#                 #                          ),
#                 #
#                 #          )
#                 dbc.Col(
#                     # dbc.RadioItems(
#                     #     id="slct_year",
#                     #     options=[
#                     #        {'label': 'Show All', 'value': 'all'},
#                     #        {'label': 'Mean', 'value': 'mean'},
#                     #        {'label': 'Mode', 'value': 'mode'},
#                     #        {'label': 'Median', 'value': 'median'}
#                     #    ],
#                     #     value='all',
#                     #     labelStyle={
#                     #         'display': 'inline-block',
#                     #         'text-align': 'justify'
#                     #     }
#                     # ),
#                     [html.H5("Replace with"),
#                     dcc.Dropdown(
#                         id='slct_year',
#                         options=[
#                             # {'label': 'Show All', 'value': 'all'},
#                             {'label': 'Mean', 'value': 'mean'},
#                             {'label': 'Mode', 'value': 'mode'},
#                             {'label': 'Median', 'value': 'median'}
#                         ],
#                         value=''
#                     ),]
#                 ),
#                 dbc.Col(
#                     dbc.Button(
#                         "Fill Missing",
#                         color="info",
#                         className="mr-1",
#                         id="dropall",
#                         style={
#                             'margin-top': '27px',
#                             'padding': '8px'
#                         },
#                         # size="sm"
#                     ),
#                 )
#             ]
#         )
#     ]
# )

# dropnull = html.Div(
#     [
#
#
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H5("Drop all null value rows",),
#                         dcc.Dropdown(
#                             id='dynamic-choice_null',
#                             multi=True,
#                             placeholder='Filter Column'
#                         ),
#                     ]
#                 ),
#                 dbc.Col(
#                     dbc.Button(
#                         "Drop All Null",
#                         color="info",
#                         className="mr-1",
#                         id="dropall",
#                         style={
#                             'margin-top': '27px',
#                             'padding': '8px'
#                         },
#                         # size="sm"
#                     ),
#                     # width=3
#                 ),
#             ]
#         )
#
#     ]
# ),

# fillmiss1= dbc.Row(
#                     [
#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#
#                                         html.H5("Fill missing values using below options or select columns",
#                                                 className="fill_missing"),
#                                         dbc.Row(
#                                             [
#                                                 dbc.Col(
#                                                     [
#                                                         dcc.Dropdown(
#                                                             id='dynamic-reaplce',
#                                                             multi=True,
#                                                             placeholder='Filter Column',
#                                                         ),
#                                                      ]
#                                                 ),
#                                                 dbc.Col(
#                                                     # dbc.RadioItems(
#                                                     #     id="slct_year",
#                                                     #     options=[
#                                                     #        {'label': 'Show All', 'value': 'all'},
#                                                     #        {'label': 'Mean', 'value': 'mean'},
#                                                     #        {'label': 'Mode', 'value': 'mode'},
#                                                     #        {'label': 'Median', 'value': 'median'}
#                                                     #    ],
#                                                     #     value='all',
#                                                     #     labelStyle={
#                                                     #         'display': 'inline-block',
#                                                     #         'text-align': 'justify'
#                                                     #     }
#                                                     # ),
#                                                     dbc.DropdownMenu(
#                                                         id="slct_year",
#                                                         label="Menu",
#                                                         children=[
#                                                             dbc.DropdownMenuItem("Show All"),
#                                                             dbc.DropdownMenuItem("Mean"),
#                                                             dbc.DropdownMenuItem("Mode"),
#                                                             dbc.DropdownMenuItem("Median"),
#                                                         ],
#                                                     )
#                                                 ),
#                                                 dbc.Col(
#                                                     dbc.Button(
#                                                         "Replace",
#                                                         color="info",
#                                                         className="mr-1",
#                                                         id="dropall",
#                                                         # style={
#                                                         #     'margin-top': '10px',
#                                                         #     'padding': '5px'
#                                                         # },
#                                                         # size="sm"
#                                                     ),
#                                                 )
#                                             ]
#                                         )
#                                     ]
#                                 ),
#                                 style={
#                                     'margin': '10px',
#                                     'height': 'auto'  # Automatic hieght increase
#                                 },
#                             ),
#                         ),
#                         dbc.Col(
#                             dbc.Card(
#                                 dbc.CardBody(
#                                     [
#
#                                         html.H5("Drop all null value rows or Drop duplicates using below buttons",
#                                                 className="drop_missing"),
#
#                                         # html.Div(id='dynamic-choice'),
#                                         dcc.Dropdown(id='dynamic-choice',
#                                                      multi=True,
#                                                      placeholder='Filter Column'),
#
#                                         dbc.Row(
#                                             [
#                                                 dbc.Col(
#                                                     dbc.Button(
#                                                         "Drop All Null",
#                                                         color="info",
#                                                         className="mr-1",
#                                                         id="dropall",
#                                                         style={
#                                                             'margin-top': '10px',
#                                                             'padding': '5px'
#                                                         },
#                                                         size="sm"
#                                                     ),
#                                                     width=3
#                                                 ),
#                                                 dbc.Col(
#                                                     dbc.Button(
#                                                         "Drop Duplicate",
#                                                         color="warning",
#                                                         className="mr-1",
#                                                         id="dropdup",
#                                                         style={
#                                                             'margin-top': '10px',
#                                                             'padding': '5px'
#                                                         },
#                                                         size="sm"
#                                                     ),
#                                                     width=3
#                                                 ),
#                                                 dbc.Col(
#                                                     daq.ToggleSwitch(
#                                                         id='show_stat',
#                                                         value=False,
#                                                         label='Show/Hide Statistics',
#                                                         labelPosition='left',
#                                                         style={
#                                                             'margin-top': '10px',
#                                                             'padding': '5px'
#                                                         },
#                                                     ),
#                                                 )
#                                             ]
#                                         )
#
#                                         # dbc.Button(
#                                         #     "Show Statistics",
#                                         #     color="#ebc334",
#                                         #     className="mr-2",
#                                         #     id="show_stat",
#                                         #     n_clicks=0,
#                                         #     # value="show",
#                                         #     style={
#                                         #         'margin-top': '10px'
#                                         #     }
#                                         # ),
#                                     ]
#                                 ),
#                                 style={
#                                     'margin': '10px',
#                                     'height': 'auto'
#                                 },
#                             )
#                         )
#                     ],
#                 ),

# dropdup = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H5("Drop duplicates"),
#                         dcc.Dropdown(
#                             id='dynamic-choice_dup',
#                             multi=True,
#                             placeholder='Filter Column'
#                         ),
#                     ]
#                 ),
#                 dbc.Col(
#                     dbc.Button(
#                         "Drop Duplicate",
#                         color="warning",
#                         className="mr-1",
#                         id="dropdup",
#                         style={
#                             'margin-top': '27px',
#                             'padding': '8px'
#                         },
#                         # size="sm"
#                     ),
#                     # width=3
#                 ),
#             ]
#         )
#     ]
# ),

# outlier = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         html.H5("Show Outlier"),
#                         dcc.Dropdown(
#                             id='dynamic-choice_outlier',
#                             multi=True,
#                             placeholder='Filter Column'
#                         ),
#                     ]
#                 ),
#                 dbc.Col(
#                     dbc.Button(
#                         "Show Outlier",
#                         color="warning",
#                         className="mr-1",
#                         id="dropdup",
#                         style={
#                             'margin-top': '27px',
#                             'padding': '8px'
#                         },
#                         # size="sm"
#                     ),
#                     # width=3
#                 ),
#             ]
#         )
#     ]
# ),

# datasplit = html.Div(
#     [
#         dbc.Row(
#             [
#                 dbc.Col(
#                     [
#                         # html.H5("Enter Chunks"),
#                         dbc.Input(
#                             id="input",
#                             placeholder="Chunks",
#                             type="text",
#                             # style={
#                             #     'margin-top': '27px',
#                             #     'padding': '8px'
#                             # }
#                         ),
#                     ]
#                 ),
#                 dbc.Col(
#                     [
#                         dbc.Button(
#                             "Split Data",
#                             color="primary",
#                             className="mr-11"
#                         ),
#                     ]
#                 )
#             ]
#         )
#     ]
# ),



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
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #
                #                         html.H5("Fill missing values using below options or select columns",
                #                                 className="fill_missing"),
                #                         dbc.Row([
                #                             dbc.Col(
                #                                 [dcc.Dropdown(id='dynamic-reaplce',
                #
                #                                              multi=True,
                #                                              placeholder='Filter Column',
                #                                              ),
                #
                #                                  ]
                #
                #                             ),
                #                             dbc.Col(dbc.RadioItems(id="slct_year",
                #                                                    # className="radio-inline",
                #                                                    options=[
                #                                                        {'label': 'Show All', 'value': 'all'},
                #                                                        {'label': 'Mean', 'value': 'mean'},
                #                                                        {'label': 'Mode', 'value': 'mode'},
                #                                                        {'label': 'Median', 'value': 'median'}
                #                                                    ],
                #                                                    value='all',
                #                                                    labelStyle={'display': 'inline-block',
                #                                                                'text-align': 'justify'}
                #                                                    # radio button with label
                #                                                    ),
                #
                #                                     )
                #                         ])
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': 'auto'  # Automatic hieght increase
                #                 },
                #             ),
                #         ),
                #         dbc.Col(
                #             dbc.Card(
                #                 dbc.CardBody(
                #                     [
                #
                #                         html.H5("Drop all null value rows or Drop duplicates using below buttons",
                #                                 className="drop_missing"),
                #
                #                         # html.Div(id='dynamic-choice'),
                #                         dcc.Dropdown(id='dynamic-choice',
                #                                      multi=True,
                #                                      placeholder='Filter Column'),
                #
                #                         dbc.Row(
                #                             [
                #                                 dbc.Col(
                #                                     dbc.Button(
                #                                         "Drop All Null",
                #                                         color="info",
                #                                         className="mr-1",
                #                                         id="dropall",
                #                                         style={
                #                                             'margin-top': '10px',
                #                                             'padding': '5px'
                #                                         },
                #                                         size="sm"
                #                                     ),
                #                                     width=3
                #                                 ),
                #                                 dbc.Col(
                #                                     dbc.Button(
                #                                         "Drop Duplicate",
                #                                         color="warning",
                #                                         className="mr-1",
                #                                         id="dropdup",
                #                                         style={
                #                                             'margin-top': '10px',
                #                                             'padding': '5px'
                #                                         },
                #                                         size="sm"
                #                                     ),
                #                                     width=3
                #                                 ),
                #                                 dbc.Col(
                #                                     daq.ToggleSwitch(
                #                                         id='show_stat',
                #                                         value=False,
                #                                         label='Show/Hide Statistics',
                #                                         labelPosition='left',
                #                                         style={
                #                                             'margin-top': '10px',
                #                                             'padding': '5px'
                #                                         },
                #                                     ),
                #                                 )
                #                             ]
                #                         )
                #
                #                         # dbc.Button(
                #                         #     "Show Statistics",
                #                         #     color="#ebc334",
                #                         #     className="mr-2",
                #                         #     id="show_stat",
                #                         #     n_clicks=0,
                #                         #     # value="show",
                #                         #     style={
                #                         #         'margin-top': '10px'
                #                         #     }
                #                         # ),
                #                     ]
                #                 ),
                #                 style={
                #                     'margin': '10px',
                #                     'height': 'auto'
                #                 },
                #             )
                #         )
                #     ],
                #     style={
                #         'margin-top': "100px" # Row style
                #      }
                # ),

                dbc.Row(
                    [
                        dbc.Col(
                            [

                                dbc.Card([
                                    dbc.CardHeader(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            html.H5("Data Info", className="drop_missing", style={"text-align": "center"}),
                                                        ],

                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5("Column Data Type", className="drop_missing", style={"text-align": "center"}),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            daq.ToggleSwitch(
                                                                id='show_stat',
                                                                value=False,
                                                                label='Show Stats',
                                                                labelPosition='left',
                                                                # style={
                                                                #     # 'margin-top': '10px',
                                                                #     'padding': '0px'
                                                                # },

                                                            ),
                                                        ],
                                                        width=2
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.Row(
                                                                [
                                                                    dbc.Col(
                                                                        [
                                                                            html.Ul(
                                                                                id="output"
                                                                            ),
                                                                        ],
                                                                        # width=3
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
                                                         ],
                                                        width=6
                                                    ),
                                                    dbc.Col(
                                                        [
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
                                ],
                                    style={'margin-top': '20px'},
                                )
                            ]
                        ),
                    ],
                style={
                        'margin-top': "100px" # Row style
                     }
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
                            html.Div(id='corr-table')
                        ),
                        dbc.Col(
                            html.Div(id='output-heatmap')
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Div(id="outlier_graph")
                            ]
                        )
                    ]
                ),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        # dbc.CardHeader(
                                        #
                                        # ),
                                        dbc.CardBody(
                                            [
                                                dbc.Tabs(
                                                    [
                                                        dbc.Tab(
                                                            html.Div(
                                                                [
                                                                    # html.H5( "Fill missing values using below options or select columns",
                                                                    #      className="fill_missing" ),
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                [
                                                                                    html.H5(
                                                                                        "Select columns",
                                                                                    ),
                                                                                    dcc.Dropdown(
                                                                                        id='dynamic-reaplce',
                                                                                        multi=True,
                                                                                        placeholder='Filter Column',
                                                                                    ),
                                                                                 ],
                                                                            ),
                                                                            # dbc.Col( dbc.RadioItems( id="slct_year",
                                                                            #                          # className="radio-inline",
                                                                            #                          options=[
                                                                            #                              {'label': 'Show All', 'value': 'all'},
                                                                            #                              {'label': 'Mean', 'value': 'mean'},
                                                                            #                              {'label': 'Mode', 'value': 'mode'},
                                                                            #                              {'label': 'Median', 'value': 'median'}
                                                                            #                          ],
                                                                            #                          value='all',
                                                                            #                          labelStyle={'display': 'inline-block',
                                                                            #                                      'text-align': 'justify'}
                                                                            #                          # radio button with label
                                                                            #                          ),
                                                                            #
                                                                            #          )
                                                                            dbc.Col(
                                                                                # dbc.RadioItems(
                                                                                #     id="slct_year",
                                                                                #     options=[
                                                                                #        {'label': 'Show All', 'value': 'all'},
                                                                                #        {'label': 'Mean', 'value': 'mean'},
                                                                                #        {'label': 'Mode', 'value': 'mode'},
                                                                                #        {'label': 'Median', 'value': 'median'}
                                                                                #    ],
                                                                                #     value='all',
                                                                                #     labelStyle={
                                                                                #         'display': 'inline-block',
                                                                                #         'text-align': 'justify'
                                                                                #     }
                                                                                # ),
                                                                                [html.H5("Replace with"),
                                                                                dcc.Dropdown(
                                                                                    id='slct_year',
                                                                                    options=[
                                                                                        # {'label': 'Show All', 'value': 'all'},
                                                                                        {'label': 'Mean', 'value': 'mean'},
                                                                                        {'label': 'Mode', 'value': 'mode'},
                                                                                        {'label': 'Median', 'value': 'median'}
                                                                                    ],
                                                                                    value=''
                                                                                ),
                                                                                 ]
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Button(
                                                                                    "Fill Missing",
                                                                                    color="info",
                                                                                    className="mr-1",
                                                                                    id="fill_missing",
                                                                                    style={
                                                                                        'margin-top': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                            )
                                                                        ],
                                                                        style={
                                                                            "margin-top": "25px"
                                                                        }
                                                                    )
                                                                ]
                                                            ),
                                                            label="Fill Missing Data",
                                                            tab_id="tab-1"
                                                        ),
                                                        dbc.Tab(
                                                            html.Div(
                                                                [
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                [
                                                                                    html.H5("Drop all null value rows",),
                                                                                    dcc.Dropdown(
                                                                                        id='dynamic-choice_null',
                                                                                        multi=True,
                                                                                        placeholder='Filter Column'
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Button(
                                                                                    "Drop All Null",
                                                                                    color="info",
                                                                                    className="mr-1",
                                                                                    id="dropall",
                                                                                    style={
                                                                                        'margin-top': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "margin-top": "25px"
                                                                        }
                                                                    )

                                                                ]
                                                            ),
                                                            label="Drop Null Values",
                                                            tab_id="tab-2"
                                                        ),
                                                        dbc.Tab(
                                                            html.Div(
                                                                [
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                [
                                                                                    html.H5("Drop duplicates"),
                                                                                    dcc.Dropdown(
                                                                                        id='dynamic-choice_dup',
                                                                                        multi=True,
                                                                                        placeholder='Filter Column'
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Button(
                                                                                    "Drop Duplicate",
                                                                                    color="warning",
                                                                                    className="mr-1",
                                                                                    id="dropdup",
                                                                                    style={
                                                                                        'margin-top': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "margin-top": "25px"
                                                                        }
                                                                    )
                                                                ]
                                                            ),
                                                            label="Drop Duplicates",
                                                            tab_id="tab-3"
                                                        ),
                                                        dbc.Tab(
                                                            html.Div(
                                                                [
                                                                    dbc.Row(
                                                                        [
                                                                            dbc.Col(
                                                                                [
                                                                                    html.H5("Show Outlier"),
                                                                                    dcc.Dropdown(
                                                                                        id='dynamic-choice_outlier',
                                                                                        multi=True,
                                                                                        placeholder='Filter Column'
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                            dbc.Col(
                                                                                dbc.Button(
                                                                                    "Show Outlier",
                                                                                    color="warning",
                                                                                    className="mr-1",
                                                                                    id="show_outlier",
                                                                                    style={
                                                                                        'margin-top': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "margin-top": "25px"
                                                                        }
                                                                    )
                                                                ]
                                                            ),
                                                            label="Outliers",
                                                            tab_id="tab-4"
                                                        ),
                                                        dbc.Tab(
                                                            html.Div(
                                                                [
                                                                    dbc.Row(
                                                                        [
                                                                            # html.H5("Split large data file", style={'text-align': "center"}),
                                                                            dbc.Col(
                                                                                [
                                                                                    # html.H5("Enter Chunks"),
                                                                                    dbc.Input(
                                                                                        id="Chunks_Input",
                                                                                        placeholder="Chunks Size",
                                                                                        type="text",
                                                                                        # style={
                                                                                        #     'margin-top': '27px',
                                                                                        #     'padding': '8px'
                                                                                        # }
                                                                                    ),
                                                                                ]
                                                                            ),
                                                                            # dbc.Col(
                                                                            #     [
                                                                            #         # html.H5("Enter Chunks"),
                                                                            #         dbc.Input(
                                                                            #             id="input_file",
                                                                            #             placeholder="Input File Path",
                                                                            #             type="text",
                                                                            #             # style={
                                                                            #             #     'margin-top': '27px',
                                                                            #             #     'padding': '8px'
                                                                            #             # }
                                                                            #         ),
                                                                            #     ]
                                                                            # ),
                                                                            # dbc.Col(
                                                                            #     [
                                                                            #         # html.H5("Enter Chunks"),
                                                                            #         dbc.Input(
                                                                            #             id="output_file",
                                                                            #             placeholder="Output File Path",
                                                                            #             type="text",
                                                                            #             # style={
                                                                            #             #     'margin-top': '27px',
                                                                            #             #     'padding': '8px'
                                                                            #             # }
                                                                            #         ),
                                                                            #     ]
                                                                            # ),
                                                                            dbc.Col(
                                                                                [
                                                                                    dbc.Button(
                                                                                        "Split Data",
                                                                                        color="primary",
                                                                                        className="mr-11"
                                                                                    ),
                                                                                ]
                                                                            )
                                                                        ],
                                                                        style={
                                                                            "margin-top": "25px"
                                                                        }
                                                                    )
                                                                ]
                                                            ),
                                                            label="Data Split",
                                                            tab_id="tab-5"
                                                        ),
                                                        # dbc.Tab(label="Data Encoding", tab_id="tab-6"),
                                                    ],
                                                    id="card-tabs",
                                                    card=True,
                                                    active_tab="tab-1",
                                                )
                                            ]
                                        ),
                                    ],
                                    style={'margin-top': '20px'},
                                )
                            ]
                        )
                    ]
                ),
                # dbc.Row(
                #     [
                #         dbc.Col(
                #             html.Div(id='output-pairplot')
                #         )
                #     ]
                # ),
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardHeader(
                                        [
                                            dbc.Row(
                                                [
                                                    dbc.Col(
                                                        [
                                                            dbc.Button(
                                                                "Download Data",
                                                                color="warning",
                                                                className="mr-1",
                                                                id="download_data",
                                                                style={
                                                                    'margin-top': '5px',
                                                                    'padding': '7px'
                                                                },
                                                                # size="sm"
                                                            ),
                                                        ]
                                                    ),
                                                    dbc.Col(
                                                        [
                                                            dcc.RadioItems(
                                                                id="allradio",
                                                                options=[
                                                                    {'label': 'All', 'value': 'allradiodata'},
                                                                    {'label': 'Top 10 rows', 'value': 'head'},
                                                                    {'label': 'Last 10 rows', 'value': 'tail'}
                                                                ],
                                                                value='allradiodata',
                                                                labelStyle={'display': 'inline-block',
                                                                            'padding': '5px'},
                                                                inputStyle={
                                                                    "margin-right": "5px",
                                                                },
                                                                inputClassName="checkmark",
                                                                style={
                                                                    'margin-top': '5px',
                                                                    "text-align": "right"
                                                                },
                                                                className="myallradio"
                                                            ),
                                                        ]
                                                    )
                                                ]
                                            )
                                        ]
                                    ),
                                    dbc.CardBody(
                                        [
                                            dbc.Row(
                                                dbc.Col(
                                                    [


                                                        ]
                                                )
                                            ),
                                            html.Div(
                                                id='output-data-upload',
                                                className='table-wrapper-scroll-y my-custom-scrollbar'
                                            ),
                                            # html.P(id='save-button-hidden', style={'display':'none'}),
                                        ]
                                    ),
                                ],
                                style={'margin-top': '20px', 'margin-bottom': '20px'},
                            )
                        )
                    ]
                ),
            ]
        )

    ],
    id="page-1-content-1"),

])

# @app.callback(
#     Output("content", "children"),
#     [
#       Input("card-tabs", "active_tab")
#     ]
# )
# def switch_tab(at):
#     if at == "tab-1":
#         return fillmiss
#     elif at == "tab-2":
#         return dropnull
#     elif at=="tab-3":
#         return dropdup
#     elif at=="tab-4":
#         return outlier
#     elif at=="tab-5":
#         return datasplit
#     return None

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
        [Output('output-data-describe', "children"),
         Output('corr-table', "children"),
         Output('output-heatmap', "children"),

         ],
        [
            Input('upload-data', 'contents'),
            Input('upload-data', 'filename'),
            Input('show_stat', 'value'),

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
            # dt = dt.dropna()
            # dt = df.applymap( "${0:.f}".format )
            table =dbc.Card(

                [
                    dbc.CardHeader(
                        html.H5("Statistics", style={"text-align": "center"}),
                    ),
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
                ],
                style={'margin-top': '20px'},
            )
            dt_corr = df.corr()
            dt_corr = dt_corr.reset_index()
            dt_corr = dt_corr.rename( columns={"index": ""} )
            # dt_corr = dt_corr.dropna()
            table_corr = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Corealation", style={"text-align": "center"}),
                    ),
                    dbc.CardBody(
                        [
                            dbc.Table.from_dataframe( dt_corr,
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
                ],
                style={'margin-top': '20px', 'margin-right': '5px', 'height': "400px"},
            )
            htmap=dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5( "Corealation Plot", style={"text-align": "center"} ),
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                id='StyleBox',
                                figure=
                                {
                                    'data': [{
                                        'z': dt_corr.values.T.tolist(),
                                        'y': dt_corr.columns.tolist(),
                                        'x': dt_corr.index.tolist(),
                                        'ygap': 2,
                                        'reversescale': 'true',
                                        'colorscale': [[0, 'white'], [1, 'blue']],
                                        'type': 'heatmap',
                                    }],
                                    'layout': {
                                        'height': 250,
                                        # 'width': scaled_size,
                                        # 'xaxis': {'side': 'top'},
                                        # 'margin': {
                                        #     'l': left_margin,
                                        #     'r': right_margin,
                                        #     'b': 150,
                                        #     't': 100

                                    }
                                }

                            )
                        ]
                    )
                ],
                style={
                    'margin-top': '20px',
                    'margin-left': '5px',
                    'height': "400px"
                },
            )
            # df1 = df
            # cols = df1.select_dtypes( [np.int64, np.float64] ).columns
            # print(cols)
            # scatter = dbc.Card(
            #     dbc.CardBody(
            #
            #         [
            #             html.H5( "Pair Plot", style={"text-align": "center"} ),
            #             dcc.Graph(
            #                 id='Style_matrix',
            #
            #                 figure=
            #                 px.scatter_matrix( df1,
            #                                          dimensions=cols,
            #                                          # color=
            #
            #                                    )
            #             )
            #         ]
            #     )
            # )

            return table, table_corr, htmap
        else:
            return None, None, None
    else:
        return None, None, None


@app.callback(
    Output('outlier_graph', "children"),
    [
        Input('upload-data', 'contents'),
        Input('upload-data', 'filename'),
        Input('show_outlier', 'n_clicks'),
        Input('dynamic-choice_outlier', 'value')
    ],
)
def show_outliers(contents, filename, show_outlier, choice_outlier):
    if contents is not None:
        if show_outlier:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)
            # corr_matrix = df.corr().abs()
            # high_corr_var = np.where(corr_matrix > 0.9)
            # high_corr_var = [(corr_matrix.columns[x], corr_matrix.columns[y]) for x, y in zip(*high_corr_var) if
            #                  x != y and x < y]
            # out = [item for t in high_corr_var for item in t]
            # x = np.array(out)

            fig = px.box(df, y=choice_outlier, )
            # fig.add_trace(marker_color = 'indianred')

            outlierPlot = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Outliers", style={"text-align": "center"})
                    ),
                    dbc.CardBody(
                        [
                            dcc.Graph(
                                id="outlier_style",
                                figure=fig,

                            )
                        ]
                    )
                ],
                style={
                    'margin-top': '20px',
                    # 'margin-left': '5px',
                    # 'height': "400px"
                },
            )

            return outlierPlot
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

@app.callback(
    [
        Output('dynamic-reaplce', 'options'),
        Output('dynamic-choice_null', 'options'),
        Output('dynamic-choice_dup', 'options'),
        Output('dynamic-choice_outlier', 'options')
    ],
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

        df1 = df.columns[df.duplicated().any()].tolist()[0]
        print("sdfasdf == "+str(df1))

        corr_matrix = df.corr().abs()
        high_corr_var = np.where(corr_matrix > 0.9)
        high_corr_var = [(corr_matrix.columns[x], corr_matrix.columns[y]) for x, y in zip(*high_corr_var) if
                         x != y and x < y]
        out = [item for t in high_corr_var for item in t]
        x = np.array(out)
        df2 = np.unique(x)

        dynamic_replace = []
        dynamic_choice = []
        dynamic_outliers = []

        if mis is not None or mis != "":
            dynamic_replace = [{'label': i, 'value': i} for i in sorted(list(mis))]

        if df1 is not None or df1 != "":
            dynamic_choice = [{'label': i, 'value': i} for i in sorted(list(df1))]

        if df2 is not None or df2 != "":
            dynamic_outliers = [{'label': i, 'value': i} for i in sorted(list(df2))]
        # else:
        #     return []
        return dynamic_replace, dynamic_replace, dynamic_choice, dynamic_outliers
    else:

        return [], [], [], []


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

        if mis is not None or mis != "":
            return [{'label': i, 'value': i} for i in sorted(list(mis))]
        else:
            return []
    else:

        return []

@app.callback(
    # [
    #     Output('output-data-upload', 'children'),
    #     Output('save-button-hidden', 'children')
    # ],
Output('output-data-upload', 'children'),
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
                  Input("slct_year", "value"),
                  Input("dropall", "n_clicks"),
                  Input("dropdup", "n_clicks"),
                  Input("dynamic-choice_null", "value"),
                  Input("dynamic-choice_dup", "value"),
                  Input("dynamic-reaplce", "value"),
                  Input("dynamic-choice_outlier", "value"),
                  Input("allradio", "value"),
                  Input("fill_missing", "n_clicks"),
                  Input("download_data", "n_clicks")
              ]
              )
def page_1_dropdown(
        contents,
        filename,
        is_selected,
        dropall,
        dropdup,
        dynamic_choice_null,
        dynamic_choice_dup,
        dynamic_reaplce,
        dynamic_choice_outlier,
        radioall,
        fill_missing,
        download_data
):
    print(radioall)
    if contents is not None and is_selected == "mean" and fill_missing:
        print(dynamic_reaplce)
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_reaplce:
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
    elif contents is not None and is_selected == "mode" and fill_missing:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_reaplce:
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
    elif contents is not None and is_selected == "median" and fill_missing:
        contents = contents[0]
        filename = filename[0]
        df = parse_data(contents, filename)
        misingcols = df.columns[df.isnull().any()].tolist()

        for i in dynamic_reaplce:
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
    elif contents is not None:
        if dropall:
            if dynamic_choice_null is not None:
                contents = contents[0]
                filename = filename[0]
                df = parse_data(contents, filename)

                df = df.dropna(axis=0, subset=dynamic_choice_null)

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

                # if download_data:
                #     dashTable = dash_table.DataTable(
                #         id='table',
                #         columns=[{"name": i, "id": i} for i in df.columns],
                #         data=df.to_dict('records'),
                #         export_format='xlsx',
                #         export_headers='display',
                #         merge_duplicate_headers=True
                #     )
                #     return table, dashTable
                # else:
                #     return table, None
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



if __name__ == '__main__':
    app.run_server(host="0.0.0.0")
