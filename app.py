import pybase64
import io
import urllib
import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc # Dash componetents
import pandas as pd
import dash_daq as daq
import plotly.express as px
import numpy as np
from dash_extensions import Download
from dash_extensions.snippets import send_data_frame



app = dash.Dash(
    # #CSS External#
    external_stylesheets=[dbc.themes.MATERIA]
)

app.config.suppress_callback_exceptions = True

app.title = 'Data pre-processing app'


server = app.server

def most_frequent(List):
    return max(set(List), key = List.count)

buturl="https://img.icons8.com/color/48/000000/search.png"
global_df=pd.DataFrame()
print(global_df)
def downloadData(df):
    download_data_df = df.to_csv(index=False, encoding='utf-8')
    csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(download_data_df)
    return html.Div([
        html.Div(
            [
                html.Div([
                    html.A(
                        'DOWNLOAD DATA',
                        id='download-link-Invoice',
                        download="data.csv",
                        href=csv_string,
                        target="_blank",
                        style={
                            'margin-top': '40'
                        }
                    ),
                ], )
            ],
            className="w-100 d-dash",
            style={'margin-top': '40', 'margin-left': '50'}
        ),
    ])
search_bar = dbc.Container(
    [
        dbc.Row(
            [
                dbc.Col(dbc.Input(type="search", placeholder="Type a query to perform operations on data and change graph"),style={

                                                    'marginLeft': '120px'},),
                # dbc.Col(
                #     dbc.Button("Search", color="primary", className="ml-2",),
                #
                #     width="auto",
                # ),
                html.Img(src=buturl, height="40px")
            ],
            no_gutters=True,
            className="col-md-11",
            align="center",
        )
    ]
)


app.layout = html.Div(
    [
    dcc.Location(id='url', refresh=False),

    html.Div([  # Layout render

        dbc.Container(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.H5(  ## H5 Header size H1, H2,H3
                                                    "Import your Excel or CSV file",
                                                    className="importfile",
                                                    style={
                                                        'marginBottom': '25px',
                                                        'textAlign': 'center'
                                                    }
                                            ),
                                            dcc.Upload(  # Upload component
                                                id='upload-data',  # Input for callback
                                                children=html.Div(
                                                    [
                                                        'Drag and Drop or ',
                                                        html.A('Select Files')  # Attribute
                                                    ]
                                                ),

                                                style={
                                                    'width': '100%',
                                                    'height': '320px',
                                                    'lineHeight': '60px',
                                                    'borderWidth': '1px',
                                                    'borderStyle': 'dashed',
                                                    'borderRadius': '10px',
                                                    'textAlign': 'center',
                                                    'margin': '10px',
                                                    'padding': '125px'
                                                },

                                                # Allow multiple files to be uploaded
                                                multiple=True

                                            ),

                                            # dbc.Button("Goto Analytics Page",
                                            #            color="primary",
                                            #            className="ml-2",
                                            #            href='/data_analysis',
                                            #            id="goto-analytics"
                                            #            ),

                                        ]
                                    )
                                ],
                                style={'margin': '25px', 'padding': '20px'},  # Cardbody style
                            ),
                        ),

                    ],
                    style={
                        'marginTop': "20px",  # Row style
                        'marginBottom': '20px'
                    }
                ),
            ]
        ),
        html.Footer(
            html.Div(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5(
                                            "Contributor",
                                            style={
                                                "textAlign": "center"
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H6(
                                        html.A(
                                            "Ajinkya Deshmukh",
                                            href="https://www.linkedin.com/in/ajinkya-deshmukh-3bb96112b",
                                            target="_blank"
                                        ),
                                        style={
                                            "textAlign": "right"
                                        }
                                    ),

                                ),
                                dbc.Col(
                                    html.H6(
                                        html.A(
                                            "Sandeep Sharma",
                                            href="https://www.linkedin.com/in/sandeep-sharma-2bb949bb/",
                                            target="_blank"
                                        ),
                                        style={
                                            "textAlign": "left"
                                        }
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )
    ],
    id='page-content'),
    html.Div([  # Layout render

        # dbc.Navbar(
        #     [
        #         # html.A(
        #         #     # Use row and col to control vertical alignment of logo / brand
        #         #     # dbc.Row(
        #         #     #     [
        #         #     #         dbc.Col(dbc.NavbarBrand("Powered Automation", className="ml-2")),
        #         #     #     ],
        #         #     #     align="center",
        #         #     #     no_gutters=True,
        #         #     # ),
        #         #     # href="https://plot.ly",
        #         # ),
        #         # dbc.NavbarToggler( id="navbar-toggler" ),
        #         dbc.Collapse(search_bar, id="navbar-collapse", navbar=True, ),
        #     ],
        #     color="White",
        #     dark=False,
        #     fixed='top',
        #     style={'textAlign': 'center'}
        # ),

        dbc.Container(
            [

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
                                                            html.H5("DATA INFO", className="drop_missing", style={"textAlign": "center"}),
                                                        ],

                                                    ),
                                                    dbc.Col(
                                                        [
                                                            html.H5("DATA TYPE", className="drop_missing", style={"textAlign": "center"}),
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
                                                                #     # 'marginTop': '10px',
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

                                                                    # dbc.Col(
                                                                    #     [
                                                                    #         html.Ul(
                                                                    #             id="output-column-values"
                                                                    #         )
                                                                    #     ]
                                                                    #
                                                                    # ),

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
                                                        style={
                                                            'height': "200px",
                                                            'position': 'relative',
                                                            # 'overflow': 'auto'
                                                        },
                                                        className='table-wrapper-scroll-y my-custom-scrollbar'
                                                    )
                                                ]
                                            )
                                        ],
                                    ),
                                ],
                                    style={'marginTop': '20px'},
                                )
                            ]
                        ),
                    ],
                style={
                        'marginTop': "20px" # Row style
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
                            html.Div(
                                id='corr-table',

                            )
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
                                                                                                                                             #          )
                                                                            dbc.Col(

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
                                                                                        'marginTop': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                            )
                                                                        ],
                                                                        style={
                                                                            "marginTop": "25px"
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
                                                                                        'marginTop': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "marginTop": "25px"
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
                                                                                        'marginTop': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),
                                                                        ],
                                                                        style={
                                                                            "marginTop": "25px"
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
                                                                                        'marginTop': '27px',
                                                                                        'padding': '8px'
                                                                                    },
                                                                                    # size="sm"
                                                                                ),
                                                                                # width=3
                                                                            ),

                                                                        ],
                                                                        style={
                                                                            "marginTop": "25px"
                                                                        }
                                                                    )
                                                                ]
                                                            ),
                                                            label="Outliers",
                                                            tab_id="tab-4"
                                                        ),
                                                        # dbc.Tab(
                                                        #     html.Div(
                                                        #         [
                                                        #             dbc.Row(
                                                        #                 [
                                                        #                     dbc.Col(
                                                        #                         [
                                                        #                             html.H5(
                                                        #                                 "Select column X",
                                                        #                             ),
                                                        #                             dcc.Dropdown(
                                                        #                                 id='selectX',
                                                        #                                 multi=True,
                                                        #                                 placeholder='Filter Column',
                                                        #                             ),
                                                        #                         ],
                                                        #                     ),
                                                        #                     dbc.Col(
                                                        #                         [html.H5("Select column Y"),
                                                        #                          dcc.Dropdown(
                                                        #                              id='selectY',
                                                        #                              options=[
                                                        #
                                                        #                              ],
                                                        #                              value=''
                                                        #                          ),
                                                        #                          ]
                                                        #                     ),
                                                        #
                                                        #                     dbc.Col(
                                                        #                         [
                                                        #                             dbc.Button(
                                                        #                                 "Show best fit",
                                                        #                                 color="primary",
                                                        #                                 className="mr-11",
                                                        #                                 id="split_data",
                                                        #                                 style={
                                                        #                                     'marginTop': '27px',
                                                        #                                     'padding': '8px'
                                                        #                                 },
                                                        #
                                                        #                             ),
                                                        #                         ]
                                                        #                     )
                                                        #                 ],
                                                        #                 style={
                                                        #                     "marginTop": "25px"
                                                        #                 }
                                                        #             )
                                                        #         ]
                                                        #     ),
                                                        #     label="Best Fit Algorithm",
                                                        #     tab_id="tab-5"
                                                        # ),
                                                    ],
                                                    id="card-tabs",
                                                    card=True,
                                                    active_tab="tab-1",
                                                )
                                            ]
                                        ),
                                    ],
                                    style={'marginTop': '20px'},
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
                                                            # downloadData(global_df)
                                                            dbc.Button(
                                                            #     html.A(
                                                            #     "Download Data",
                                                            #     id="download_data",
                                                            #     href="",
                                                            #     download="Data.csv",
                                                            #     target="_blank"
                                                            #
                                                            # ),
                                                                'EXPORT DATA',
                                                                # href='',
                                                                color="warning",
                                                                className="mr-1",
                                                                id="download_data_button",
                                                                style={
                                                                    'marginTop': '5px',
                                                                    'padding': '7px'
                                                                },
                                                                # size="sm"
                                                            ),
                                                            Download(id="download_my_data")
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
                                                                    "marginRight": "5px",
                                                                },
                                                                inputClassName="checkmark",
                                                                style={
                                                                    'marginTop': '5px',
                                                                    "textAlign": "right"
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

                                            html.Div(
                                                id='output-data-upload',
                                                className='table-wrapper-scroll-y custom-table-scrollbar'
                                            ),
                                            # html.P(id='save-button-hidden', style={'display':'none'}),
                                        ]
                                    ),
                                ],
                                style={'marginTop': '20px', 'marginBottom': '20px'},
                            )
                        )
                    ]
                ),
            ]
        ),
        html.Footer(
            html.Div(
                dbc.Container(
                    [
                        dbc.Row(
                            [
                                dbc.Col(
                                    [
                                        html.H5(
                                            "Contributor",
                                            style={
                                                "textAlign": "center"
                                            }
                                        )
                                    ]
                                )
                            ]
                        ),
                        dbc.Row(
                            [
                                dbc.Col(
                                    html.H6(
                                        html.A(
                                            "Ajinkya Deshmukh",
                                            href="https://www.linkedin.com/in/ajinkya-deshmukh-3bb96112b",
                                            target="_blank"
                                        ),
                                        style={
                                            "textAlign": "right",
                                        }
                                    ),

                                ),
                                dbc.Col(
                                    html.H6(
                                        html.A(
                                            "Sandeep Sharma",
                                            href="https://www.linkedin.com/in/sandeep-sharma-2bb949bb/",
                                            target="_blank"
                                        ),
                                        style={
                                            "textAlign": "left"
                                        }
                                    )
                                )
                            ]
                        )
                    ]
                )
            )
        )
    ],
    id="page-1-content-1"),

],
    # style={'background-image': "url(/assets/back.jpg)"}
)


def parse_data(contents, filename):  #CSV or Excel read and return DF
    content_type, content_string = contents.split(',')

    decoded = pybase64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV or TXT file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), low_memory=False)
            return df
        elif 'xlsx' or 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
            return df
        elif 'txt' or 'tsv' in filename:
            # Assume that the user upl, delimiter = r'\s+'oaded an excel file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), delimiter=r'\s+', low_memory=False)
            return df
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

def GetHumanReadable(size,precision=2):
    suffixes=['B','KB','MB','GB','TB']
    suffixIndex = 0
    while size > 1024 and suffixIndex < 4:
        suffixIndex += 1 #increment the index of the suffix
        size = size/1024.0 #apply the division
    return "%.*f%s"%(precision,size,suffixes[suffixIndex])

def dashDataTable(df):
    table = dash_table.DataTable(
        id='myAllData',
        data=df.to_dict('records'),
        columns=[{'id': c, 'name': c} for c in df.columns],
        # fixed_rows={'headers': True, 'data': 0},
        page_size=30,
        style_cell={  # ensure adequate header width when text is shorter than cell's text
            'textAlign': 'center'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
    )

    return table


# Index Page callback
@app.callback([Output('page-content', 'style'),
               Output('page-1-content-1', 'style')],
              [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename')
              ])
def display_page(content, filename):
    # if contents:
    if content:
        return {"display": "none"}, {"display": "inline"}
    else:
        return {"display": "inline"}, {"display": "none"}


@app.callback(
        [
            Output('output-data-describe', "children"),
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
            dt = dt.reset_index()
            dt = dt.rename(columns={"index": "" })

            # dt = dt.dropna()
            # dt = df.applymap( "${0:.f}".format )

            print(f"Len is {df.columns}")

            if len(dt.columns) > 5:
                customClass = 'table-wrapper-scroll-y data-info-scroll'
            else:
                customClass = ''

            table =dbc.Card(

                [
                    dbc.CardHeader(
                        html.H5("STATISTICS", style={"textAlign": "center"}),
                    ),
                    dbc.CardBody(
                        [
                            dbc.Table.from_dataframe(dt,
                                                     className=customClass,
                                                     bordered=True,
                                                     hover=True,
                                                     responsive=True,
                                                     striped=True,
                                                     size="sm",
                                                     style={
                                                         "padding": "0",
                                                         # "width": "auto"
                                                     }
                                                     )
                            ]
                    ),
                ],

                style={'marginTop': '20px'},
            )
            dt_corr = df.corr()
            dt_corr = dt_corr.reset_index()
            dt_corr = dt_corr.rename( columns={"index": ""} )
            # dt_corr = dt_corr.dropna()
            table_corr = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("CORRELATION", style={"textAlign": "center"}),
                    ),
                    dbc.CardBody(
                        [
                            dbc.Table.from_dataframe( dt_corr,
                                                      className='table-wrapper-scroll-y my-custom-scrollbar',
                                                      bordered=True,
                                                      hover=True,
                                                      responsive=True,
                                                      striped=True,
                                                      size="sm",
                                                      style={
                                                          "padding": "0",
                                                          "width": "100",
                                                      }
                                                      )
                        ],
                        # style={
                        #
                        # }
                    ),
                ],
                style={
                    'marginTop': '20px',
                    'marginRight': '5px',
                    'height': "500px",
                },
            )
            htmap = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5( "CORRELATION MATRIX", style={"textAlign": "center"} ),
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
                                        'height': 400,
                                        'width': 500,
                                        'xaxis': {'side': 'top'},
                                        'margin': {
                                            'l': 100,
                                            'r': 70,
                                            'b': 100,
                                            't': 70
                                        }
                                    }
                                }
                            )
                        ]
                    )
                ],
                style={
                    'marginTop': '20px',
                    'marginLeft': '5px',
                    'height': "500px"
                },
            )


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
        if show_outlier and choice_outlier:
            contents = contents[0]
            filename = filename[0]
            df = parse_data(contents, filename)

            fig = px.box(df, y=choice_outlier, )

            outlierPlot = dbc.Card(
                [
                    dbc.CardHeader(
                        html.H5("Outliers", style={"textAlign": "center"})
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
                    'marginTop': '20px',
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
        # Output("output-column-values", "children"),
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

        dt = df.dtypes


        columnList = [
            "Number of columns",
            "Number of rows",
            "Columns with empty cell",
            "Total duplicate rows",
            "Missing Percentage",
            "Total Memory Used"
        ]
        percent_missing = df.isnull().sum() / df.shape[0]
        per = (sum( percent_missing ) / len( df.columns ))
        per = "%.3f" % per
        memoryUsed = df.memory_usage(index=True).sum()
        print(per)

        columnValueList = [
            len(df.columns),
            len(df),
            len(mis),
            df.duplicated().sum(),
            per+"%",
            GetHumanReadable(memoryUsed)
        ]

        # [html.Li(i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'}) for i in [ent[1] for ent in s]],\

        return [html.Li(i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'}) for i in columnList], \
               [html.Li(i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'}) for i in columnValueList],\
               [html.Li(i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'}) for i in df.columns], \
               [html.Li( i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'} ) for i in [str( dt[1] ) for dt in dt.iteritems()]]
    else:
        columnList = [
            "Number of columns",
            "Number of rows",
            "Columns with empty cell",
            "Total duplicate rows",
            "Missing Percentage",
            "Total Memory Used"
        ]
        return [html.Li(i, style={"listStyle": "none", "fontSize": "13px", 'fontWeight': '430'}) for i in columnList], None, None, None

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

        # df1 = df.columns[df.duplicated().any()].tolist()[0]
        df1 = df.columns
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
        num_replace = []



        col_numerics = df.select_dtypes(include=np.number).columns.tolist()

        df_null = df[col_numerics]

        df_col_null = df_null.columns[df_null.isnull().any()].tolist()


        if df_col_null is not None or df_col_null != "":
            num_replace = [{'label': i, 'value': i} for i in sorted(list(df_col_null))]

        if mis is not None or mis != "":
            dynamic_replace = [{'label': i, 'value': i} for i in sorted(list(mis))]

        if df1 is not None or df1 != "":
            dynamic_choice = [{'label': i, 'value': i} for i in sorted(list(df1))]

        if df2 is not None or df2 != "":
            dynamic_outliers = [{'label': i, 'value': i} for i in sorted(list(df2))]
        # else:
        #     return []
        return num_replace, dynamic_replace, dynamic_choice, dynamic_outliers
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
    [Output('output-data-upload', 'children'),
     Output("download_my_data", "data")],
    [
                  Input('upload-data', 'contents'),
                  Input('upload-data', 'filename'),
                  Input("slct_year", "value"),
                  Input("dropall", "n_clicks"),
                  Input("dropdup", "n_clicks"),
                  Input("dynamic-choice_null", "value"),
                  Input("dynamic-choice_dup", "value"),
                  Input("dynamic-reaplce", "value"),
                  # Input("dynamic-choice_outlier", "value"),
                  Input("allradio", "value"),
                  Input("fill_missing", "n_clicks"),
                  Input("download_data_button", "n_clicks")
              ],
    # [State('download_data', 'href')]
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
        radioall,
        fill_missing,
        download_click
):
    if contents is not None:
        contents = contents[0]
        filename = filename[0]

        df = parse_data(contents, filename)

        # def ReadCondTable(df, dropall=None, dropdup=None, is_selected=None, fill_missing=None):
        #     if dropall and dropdup and (is_selected == "mean" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mean = df[i].mean()
        #                 df[i] = df[i].fillna( mean )
        #
        #         return dashDataTable( df )
        #
        #     elif dropall and dropdup and (is_selected == "mode" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mode = df[i].mode()
        #                 df[i] = df[i].fillna( mode )
        #
        #         return dashDataTable( df )
        #     elif dropall and dropdup and (is_selected == "median" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 median = df[i].median()
        #                 df[i] = df[i].fillna( median )
        #
        #         return dashDataTable( df )
        #     ####################
        #     elif dropall and (is_selected == "mean" and fill_missing):
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mean = df[i].mean()
        #                 df[i] = df[i].fillna( mean )
        #         return dashDataTable( df )
        #
        #     elif dropall and (is_selected == "mode" and fill_missing):
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mode = df[i].mode()
        #                 df[i] = df[i].fillna( mode )
        #         return dashDataTable( df )
        #
        #     elif dropall and (is_selected == "median" and fill_missing):
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 median = df[i].median()
        #                 df[i] = df[i].fillna( median )
        #         return dashDataTable( df )
        #
        #     ###########################
        #
        #     elif dropdup and (is_selected == "mean" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mean = df[i].mean()
        #                 df[i] = df[i].fillna( mean )
        #         return dashDataTable( df )
        #     elif dropdup and (is_selected == "mode" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 mode = df[i].mode()
        #                 df[i] = df[i].fillna( mode )
        #         return dashDataTable( df )
        #         # pass
        #     elif dropdup and (is_selected == "median" and fill_missing):
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         if fill_missing:
        #             for i in dynamic_reaplce:
        #                 median = df[i].median()
        #                 df[i] = df[i].fillna( median )
        #         return dashDataTable( df )
        #
        #     #########################
        #     elif dropdup and dropall:
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #             # return dashDataTable( df )
        #         if dynamic_choice_dup:
        #             df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #             # print( df )
        #
        #         return dashDataTable( df )
        #
        #
        #         # pass
        #     #######################
        #     elif dropall:
        #         print( 'dropall' )
        #         if dynamic_choice_null is not None:
        #             df = df.dropna( axis=0, subset=dynamic_choice_null )
        #             return dashDataTable( df )
        #         else:
        #             df = df.dropna()
        #             print( df )
        #             return dashDataTable( df )
        #     ##############################
        #     elif dropdup:
        #         df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
        #         print( df )
        #         return dashDataTable( df )
        #
        #     ###########################
        #     elif is_selected == "mean" and fill_missing:
        #         for i in dynamic_reaplce:
        #             mean = df[i].mean()
        #             df[i] = df[i].fillna(mean)
        #         # df=df[i]
        #         return dashDataTable(df)
        #
        #     elif is_selected == "mode" and fill_missing:
        #         for i in dynamic_reaplce:
        #             mode = df[i].mode()
        #             df[i] = df[i].fillna( mode )
        #             # df=df[i]
        #         return dashDataTable( df )
        #
        #
        #     elif is_selected == "median" and fill_missing:
        #         for i in dynamic_reaplce:
        #             median = df[i].median()
        #             df[i] = df[i].fillna( median )
        #         # df=df[i]
        #         return dashDataTable( df )
        #     else:
        #         return  dashDataTable( df )

        changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

        if radioall == 'allradiodata':
            if dropall and dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna( mean )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")

                # df['DataFrame column'].round(decimals=number)
                return dashDataTable( df ), None
            elif dropall and dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna( mode )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            elif dropall and dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna( median )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            ####################
            elif dropall and (is_selected == "mean" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna( mean )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            elif dropall and (is_selected == "mode" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna( mode )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            elif dropall and (is_selected == "median" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna( median )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            ###########################
            elif dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna( mean )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            elif dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna( mode )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
                # pass
            elif dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna( median )
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            #########################
            elif dropdup and dropall:
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                    # return dashDataTable( df )
                if dynamic_choice_dup:
                    df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                    # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None


                # pass
            #######################
            elif dropall:
                print( 'dropall' )
                if dynamic_choice_null is not None:
                    df = df.dropna( axis=0, subset=dynamic_choice_null )
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable( df ), None
                else:
                    df = df.dropna()
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable( df ), None
            ##############################
            elif dropdup:
                df = df.drop_duplicates( keep='first', subset=dynamic_choice_dup )
                # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            ###########################
            elif is_selected == "mean" and fill_missing:
                for i in dynamic_reaplce:
                    mean = df[i].mean()
                    df[i] = df[i].fillna(mean)
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif is_selected == "mode" and fill_missing:
                for i in dynamic_reaplce:
                    mode = df[i].mode()
                    df[i] = df[i].fillna( mode )
                    df[i] = df[i].round(decimals=2)
                    # df=df[i]
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            elif is_selected == "median" and fill_missing:
                for i in dynamic_reaplce:
                    median = df[i].median()
                    df[i] = df[i].fillna( median )
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable( df ), None
            else:
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
        elif radioall == 'head':
            df=df.head(10)
            if dropall and dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ####################
            elif dropall and (is_selected == "mean" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and (is_selected == "mode" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and (is_selected == "median" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ###########################
            elif dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
                # pass
            elif dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            #########################
            elif dropdup and dropall:
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                    # return dashDataTable( df )
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                    # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None

                # pass
            #######################
            elif dropall:
                print('dropall')
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable(df), None
                else:
                    df = df.dropna()
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable(df), None
            ##############################
            elif dropdup:
                df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ###########################
            elif is_selected == "mean" and fill_missing:
                for i in dynamic_reaplce:
                    mean = df[i].mean()
                    df[i] = df[i].fillna(mean)
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif is_selected == "mode" and fill_missing:
                for i in dynamic_reaplce:
                    mode = df[i].mode()
                    df[i] = df[i].fillna(mode)
                    df[i] = df[i].round(decimals=2)
                    # df=df[i]
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif is_selected == "median" and fill_missing:
                for i in dynamic_reaplce:
                    median = df[i].median()
                    df[i] = df[i].fillna(median)
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            else:
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
        elif radioall == 'tail':
            df = df.tail( 10 )
            if dropall and dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ####################
            elif dropall and (is_selected == "mean" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and (is_selected == "mode" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropall and (is_selected == "median" and fill_missing):
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ###########################
            elif dropdup and (is_selected == "mean" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mean = df[i].mean()
                        df[i] = df[i].fillna(mean)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif dropdup and (is_selected == "mode" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        mode = df[i].mode()
                        df[i] = df[i].fillna(mode)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
                # pass
            elif dropdup and (is_selected == "median" and fill_missing):
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                if fill_missing:
                    for i in dynamic_reaplce:
                        median = df[i].median()
                        df[i] = df[i].fillna(median)
                        df[i] = df[i].round(decimals=2)
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            #########################
            elif dropdup and dropall:
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                    # return dashDataTable( df )
                if dynamic_choice_dup:
                    df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                    # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None

                # pass
            #######################
            elif dropall:
                print('dropall')
                if dynamic_choice_null is not None:
                    df = df.dropna(axis=0, subset=dynamic_choice_null)
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable(df), None
                else:
                    df = df.dropna()
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                    return dashDataTable(df), None
            ##############################
            elif dropdup:
                df = df.drop_duplicates(keep='first', subset=dynamic_choice_dup)
                # print( df )
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            ###########################
            elif is_selected == "mean" and fill_missing:
                for i in dynamic_reaplce:
                    mean = df[i].mean()
                    df[i] = df[i].fillna(mean)
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif is_selected == "mode" and fill_missing:
                for i in dynamic_reaplce:
                    mode = df[i].mode()
                    df[i] = df[i].fillna(mode)
                    df[i] = df[i].round(decimals=2)
                    # df=df[i]
                    if 'download_data_button' in changed_id:
                        return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            elif is_selected == "median" and fill_missing:
                for i in dynamic_reaplce:
                    median = df[i].median()
                    df[i] = df[i].fillna(median)
                    df[i] = df[i].round(decimals=2)
                # df=df[i]
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None
            else:
                if 'download_data_button' in changed_id:
                    return dashDataTable(df), send_data_frame(df.to_csv, filename="some_name.csv")
                return dashDataTable(df), None

    else:
        return None, None


# @app.callback(
#     Output("download_my_data", "data"),
#     [Input("download_data_button", "n_clicks")]
# )
# def func(n_clicks):
#     if n_clicks:
#         # download_data_df = global_df.to_csv(index=False, encoding='utf-8')
#         # csv_string = "data:text/csv;charset=utf-8," + urllib.parse.quote(download_data_df)
#         return send_data_frame(global_df.to_csv, filename="some_name.csv")



if __name__ == '__main__':
    app.run_server()