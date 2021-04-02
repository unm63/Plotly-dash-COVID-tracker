# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 08:30:24 2021

@author: ujwal
"""

import dash
import dash_bootstrap_components as dbc
import dash_html_components as html
import dash_core_components as dcc
import requests
import pandas as pd
import plotly.graph_objects as go;
import plotly.express as px
from plotly.offline import init_notebook_mode, plot
import numpy as np
from dash.dependencies import Input,Output
import dash_table

app = dash.Dash(external_stylesheets = [ dbc.themes.FLATLY,])

#PLOTLY_LOGO = "https://images.plot.ly/logo/new-branding/plotly-logomark.png"
COVID_IMG = "https://www.fda.gov/files/Coronavirus_3D_illustration_by_CDC_1600x900.png"

url = "https://api.covid19api.com/summary"
response_world = requests.request("GET", url)
df_countries = pd.DataFrame(response_world.json()['Countries'])
df_global = pd.DataFrame(response_world.json()['Global'], index = [0])
df_last_updated= response_world.json()['Date']

confirmed = df_global['TotalConfirmed'][0]
newconfirmed = df_global['NewConfirmed'][0]
deaths = df_global['TotalDeaths'][0]
newdeaths = df_global['NewDeaths'][0]
recovered = df_global['TotalRecovered'][0]
newrecovered = df_global['NewRecovered'][0]

data = {'alpha-2':["AD", "AE", "AF", "AG", "AI", "AL", "AM", "AN", "AO", "AQ", "AR", "AS", "AT", "AU", "AW",
                   "AZ", "BA", "BB", "BD", "BE", "BF", "BG", "BH", "BI", "BJ", "BM", "BN", "BO", "BR",
                   "BS", "BT", "BV", "BW", "BY", "BZ", "CA", "CC", "CD", "CF", "CG", "CH", "CJ", "CK",
                   "CL", "CM", "CN", "CO", "CR", "CU", "CV", "CK", "CY", "CZ", "DE", "DJ", "DK", "DM",
                   "DO", "DZ", "EC", "EE", "EG", "EH", "ER", "ES", "ET", "FI", "FJ", "FK", "FN", "FO",
                   "FR", "GA", "GB", "GD", "GE", "GF", "GG", "GH", "GI", "GL", "GM", "GN", "GP", "GQ",
                   "GR", "GS", "GT", "GU", "GW", "GY", "HK", "HM", "HN", "HR", "HT", "HU", "ID", "IE",
                   "IL", "IM", "IN", "IO", "IQ", "IR", "IS", "IT", "JE", "JN", "JO", "JP", "KE", "KG",
                   "KH", "KI", "KM", "KN", "KP", "KR", "KW", "KY", "KZ", "LA", "LB", "LC", "LY", "LK", 
                   "LR", "LS", "LT", "LU", "LV", "LY", "MA", "MC", "MD", "ME", "MG", "MH", "MK", "ML",
                   "MM", "MN", "MO", "MP", "MQ", "MR", "MS", "MT", "MU", "MV", "MW", "MX", "MY", "MZ",
                   "NA", "NC", "NE", "NF", "NG", "NI", "NL", "NO", "NP", "NR", "NU", "NZ", "OM", "PA",
                   "PE", "PF", "PG", "PH", "PK", "PL", "PM", "PN", "PR", "PS", "PT", "PW", "PY", "QA",
                   "RE", "RO", "RS", "RU", "RW", "SA", "SB", "SC", "SD", "SE", "SG", "SH", "SI", "SJ",
                   "SK", "SL", "SM", "SN", "SO", "SR", "SS", "ST", "SV", "SY", "SZ", "TC", "TD", "TF",
                   "TG", "TH", "TJ", "TK", "TL", "TM", "TN", "TO", "TR", "TT", "TV", "TW", "TZ", "UA",
                   "UG", "UM", "US", "UY", "UZ", "VA", "VC", "VE", "VG", "VI", "VN", "VU", "WF", "WS",
                   "YE", "YT", "ZA", "ZM", "ZW"],

'iso-alpha':["AND", "ARE", "AFG", "ATG", "AIA", "ALB", "ARM", "ANT", "AGO", "ATA", "ARG", "ASM", "AUT", "AUS", "ABW",
             "AZE", "BIH", "BRB", "BGD", "BEL", "BFA", "BGR", "BHR", "BDI", "BEN", "BMU", "BRN", "BOL", "BRA",
             "BHS", "BTN", "BVT", "BWA", "BLR", "BLZ", "CAN", "CCK", "COD", "CAF", "COG", "CHE", "CIV", "COK",
             "CHL", "CMR", "CHN", "COL", "CRI", "CUB", "CPV", "CXR", "CYP", "CZE", "DEU", "DJI", "DNK", "DMA",
             "DOM", "DZA", "ECU", "EST", "EGY", "ESH", "ERI", "ESP", "ETH", "FIN", "FJI", "FLK", "FSM", "FRO",
             "FRA", "GAB", "GBR", "GRD", "GEO", "GUF", "GGY", "GHA", "GIB", "GRL", "GMB", "GIN", "GLP", "GNQ",
             "GRC", "SGS", "GTM", "GUM", "GNB", "GUY", "HKG", "HMD", "HND", "HRV", "HTI", "HUN", "IDN", "IRL",
             "ISR", "IMN", "IND", "IOT", "IRQ", "IRN", "ISL", "ITA", "JEY", "JAM", "JOR", "JPN", "KEN", "KGZ",
             "KHM", "KIR", "COM", "KNA", "PRK", "KRO", "KWT", "CYM", "KAZ", "LAO", "LBN", "LCA", "LIE", "LKA",
             "LBR", "LSO", "LTU", "LUX", "LVA", "LBY", "MAR", "MCO", "MDA", "MNE", "MDG", "MHL", "MKD", "MLI",
             "MMR", "MNG", "MAC", "MNP", "MTQ", "MRT", "MSR", "MLT", "MUS", "MDV", "MWI", "MEX", "MYS",
             "MOZ", "NAM", "NCL", "NER", "NFK", "NGA", "NIC", "NLD", "NOR", "NPL", "NRU", "NIU", "NZL", "OMN",
             "PAN", "PER", "PYF", "PNG", "PHL", "PAK", "POL", "SPM", "PCN", "PRI", "PSE", "PRT", "PLW", "PRY",
             "QAT", "REU", "ROU", "SRB", "RUS", "RWA", "SAU", "SLB", "SYC", "SDN", "SWE", "SGP", "SHN", "SVN",
             "SJM", "SVK", "SLE", "SMR", "SEN", "SOM", "SUR", "SSD", "STP", "SLV", "SYR", "SWZ", "TCA", "TCD",
             "ATF", "TGO", "THA", "TJK", "TKL", "TLS", "TKM", "TUN", "TON", "TUR", "TTO", "TUV", "TWN", "TZA",
             "UKR", "UGA", "UMI", "USA", "URY", "UZB", "VAT", "VCT", "VEN", "VGB", "VIR", "VNM", "VUT", "WLF",
             "WSM", "YEM", "MYT", "ZAF", "ZMB", "ZWE"]}

code_mapping = pd.DataFrame(data)

df_world_f = pd.merge(df_countries[['Country','TotalConfirmed','TotalDeaths','TotalRecovered','CountryCode']],code_mapping, left_on = 'CountryCode', right_on = 'alpha-2', how = 'inner')

def world_map(df):
    fig = px.choropleth(df, locations="iso-alpha", color="TotalConfirmed",
                        hover_name="Country", 
                        hover_data = ['TotalConfirmed','TotalDeaths','TotalRecovered'],
                        projection="orthographic",
                        color_continuous_scale=px.colors.sequential.Plasma)
    fig.update_layout(margin = dict(l=4,r=4,t=4,b=4))
    return fig


def data_for_cases(header, total_cases, new_cases):
    card_content = [
        dbc.CardHeader(header),
        dbc.CardBody(
                [
                       dcc.Markdown(dangerously_allow_html = True,
                                    children = ["{0} <br><sub>+{1}</sub></br>".format(total_cases,new_cases)])])
        ]
    return card_content


body_app = dbc.Container([
        dbc.Row([
                dbc.Col(dbc.Card(data_for_cases("Confirmed",f'{confirmed:,}',f'{newconfirmed:,}'), color = 'primary', style = {'text-align':'center'}, inverse = True)),
                dbc.Col(dbc.Card(data_for_cases("Recovered",f'{recovered:,}',f'{newconfirmed:,}'), color = 'success', style = {'text-align':'center'}, inverse = True)),
                dbc.Col(dbc.Card(data_for_cases("Deaths",f'{deaths:,}',f'{newdeaths:,}'), color = 'danger', style = {'text-align':'center'}, inverse = True))
                
                ]),
        
        html.Br(),
        
        dbc.Row([dbc.Col(dcc.Graph(id = 'world-graph', figure = world_map(df_world_f)), style = {'height':'450px'}),
                         
                 dbc.Col([html.Div(id = 'dropdown-div', children = 
                                           [dcc.Dropdown(id = 'country-dropdown',
                                                        options = [{'label':i,'value':i} for i in np.append(['All'],df_countries['Country'].unique())],
                                                        value = 'All',
                                                        placeholder = 'Select the country'
        )], style = {'width':'100%', 'display':'inline block'}),
                                  
                                  html.Div(id = 'world-table-output')
                                 ],style = {'height': '450px'})
        
        ])
        ],fluid=True)


navbar = dbc.Navbar(id = 'navbar', children = [
        
        html.A(
        dbc.Row([
                dbc.Col(html.Img(src = COVID_IMG, height = "70px")),
                dbc.Col(
                        dbc.NavbarBrand("Covid 19 Live Tracker", style = {'color':'black',
                                                              'fontsize':'25px',
                                                              'fontFamily': 'Times New Roman'}))
    ], align = "center",
    no_gutters = True),
href = '/'
),
dbc.Button(id = 'button', children = "Support Us", color = "primary", className = 'ml-auto', href = '/')])

app.layout = html.Div(id = 'parent', children = [navbar, body_app])


@app.callback(Output(component_id='world-table-output', component_property='children'),
              [Input(component_id='country-dropdown', component_property='value')])

def table_country(country):
    if country == 'All':
        df_final = df_countries
    else:
        df_final = df_countries.loc[df_countries['Country'] == '{}'.format(country)]
    return dash_table.DataTable(
            data = df_final[['Country','TotalConfirmed','TotalRecovered','TotalDeaths']].to_dict('records'),
            columns = [{'id':c, 'name':c} for c in df_final[['Country','TotalConfirmed','TotalRecovered','TotalDeaths']].columns],
            fixed_rows = {'headers':True},
            
            sort_action = 'native', 
            
            style_table = {'maxHeight':'450px'},
            style_header = {'backgroundColor':'rgb(224,224,224)',
                            'fontWeight':'bold',
                            'border':'4px solid white',
                            'fontSize': '12px'},
            style_data_conditional = [
                    {
                            'if': {'row_index': 'odd'},
                            'backgroundColor': 'rgb(240,240,240)',
                            'fontSize':'12px'
                            },
                    {
                            'if': {'row_index': 'even'},
                            'backgroundColor': 'rgb(255,255,255)',
                            'fontSize':'12px'
                        }
                    ],
            
            style_cell = {
                    'textAlign': 'center',
                    'fontFamily': 'Times New Roman',
                    'border': '4px solid white',
                    'maxWidth': '50px',
                    'textOverflow': 'ellipsis',
                    }
            )

if __name__ == "__main__":
    app.run_server()