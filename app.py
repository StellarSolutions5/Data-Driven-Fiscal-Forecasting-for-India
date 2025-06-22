import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.graph_objects as go
import pandas as pd
from my_linechart import *


# Load the dataset



# Capital Account
df_capital = pd.read_excel("CAPITAL_Receipt_expenditures_Predicted.xlsx")
df_capital.columns = [col.split(" (")[0] for col in df_capital.columns]  # Clean column names
df_capital.rename(columns={"YEAR": "Year"}, inplace=True)


# Revenue Account
df_revenue = pd.read_excel("REVENUE_Receipt_expenditures_Predicted.xlsx")

# Ensure correct column names
df_revenue.rename(columns={"YEAR": "Year"}, inplace=True)
df_revenue['Year'] = pd.to_datetime(df_revenue['Year']).dt.year  # Convert to integer years

# Identify predicted data (last row)
predicted_year = df_revenue.iloc[-1]['Year']
df_revenue['is_predicted'] = df_revenue['Year'] == predicted_year

# Categorizing columns
revenue_columns = [col for col in df_revenue.columns if 'REVENUE' in col or 'TAX' in col]
expenditure_columns = [col for col in df_revenue.columns if 'EXPENDITURE' in col or 'DISBURSEMENTS' in col]
nontax_columns = [col for col in df_revenue.columns if 'NONTAX' in col or 'INTEREST' in col]

# Union Territories (without legislature)
df_ut = pd.read_excel("LEGISLATURE_predicted.xlsx")
df_ut['Year'] = pd.to_datetime(df_ut['Year']).dt.year  # Convert to integer years
df_ut.rename(columns={
    "LADAKH _Receipts": "LADAKH_Receipts",
    "LADAKH _Expenditures": "LADAKH_Expenditures",
    "Total_Receipts (B+C+D+E+F)": "Total_Receipts",
    "Total_Expenditures (H+I+J+K+L)": "Total_Expenditures"
}, inplace=True)

# print(df_ut.columns)
ut_list = ["ALL"] + ["CHANDIGARH", "ANDAMAN AND NICOBAR ISLANDS", "DADRA AND NAGAR HAVELI DAMAN AND DIU", "LAKSHADWEEP", "LADAKH"]
# CHANDIGARH_Receipts


# Public Account
df_public = pd.read_excel("PUBLIC_Receipt_expenditures_Predicted.xlsx")
# Ensure correct column name
df_public.rename(columns={"YEAR": "Year"}, inplace=True)
df_public['Year'] = pd.to_datetime(df_public['Year']).dt.year  # Convert to integer years
# Rename incorrect column names
df_public.rename(columns={
    "NATIONAL_SMALL_SAVINGS_FUND_Receipts": "National_Small_Savings_Fund_Receipts",
    "NATIONAL_SMALL_SAVINGS_FUND_Expenditures": "National_Small_Savings_Fund_Expenditures",
    "STATE_PROVIDENT_FUND_AND_OTHER_ACCOUNTS_Receipts": "State_Provident_Fund_Receipts",
    "STATE_PROVIDENT_FUND_AND_OTHER_ACCOUNTS_Expenditures": "State_Provident_Fund_Expenditures",
    "RESERVE_FUNDS_Receipts": "Reserve_Funds_Receipts",
    "RESERVE_FUNDS_Expenditures": "Reserve_Funds_Expenditures",
    "DEPOSITS_AND_ADVANCES_Receipts": "Deposits_and_Advances_Receipts",
    "DEPOSITS_AND_ADVANCES_Expenditures": "Deposits_and_Advances_Expenditures"
}, inplace=True)

colors = {"Receipts": "blue", "Expenditures": "green", "Predicted": "red"}
category_list = [
    "All",  # Option to show all categories
    "National_Small_Savings_Fund", 
    "State_Provident_Fund", 
    "Reserve_Funds", 
    "Deposits_and_Advances"
]

# Disbursement Charged on the Consolidated Fund of India
df_total = pd.read_excel("IA_Totals.xlsx")
# Ensure correct column names
df_total.rename(columns={"YEAR": "Year"}, inplace=True)
df_total['Year'] = pd.to_datetime(df_total['Year']).dt.year  # Convert to integer years

# Identify columns
total_columns = ["GRAND_TOTAL"]
total_columns1 = ["TOTAL_CONSOLIDATED_FUND_OF_INDIA_RECEIPTS", "TOTAL_CONSOLIDATED_FUND_OF_INDIA_DISBURSEMENTS"]

# Initialize Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)
app.title = "Budget Dashboard"
server = app.server


        
def create_line_chart(df, columns, title):
    fig = go.Figure()
    for i, col in enumerate(columns):
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df[col],
            mode='lines+markers',
            name=col.replace('_', ' '),
            line=dict(color=color_palette[i % len(color_palette)])
        ))
    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value")
    return fig

def create_ut_chart(selected_ut):
    fig = go.Figure()
    if selected_ut == "ALL":
        for ut in ut_list[1:]:
            for data_type in ["Receipts", "Expenditures"]:
                y_column = f"{ut}_{data_type}"
                fig.add_trace(go.Scatter(
                    x=df_ut['Year'],
                    y=df_ut[y_column],
                    mode='lines+markers',
                    name=f"{ut} {data_type}",
                    line=dict(width=1)
                ))
    else:
        for data_type in ["Receipts", "Expenditures"]:
            y_column = f"{selected_ut}_{data_type}"
            fig.add_trace(go.Scatter(
                x=df_ut['Year'],
                y=df_ut[y_column],
                mode='lines+markers',
                name=data_type,
                line=dict(color=color_palette[0 if data_type == "Receipts" else 1])
            ))
    fig.update_layout(title=f"{selected_ut}: Receipts & Expenditures Over Years", xaxis_title="Year", yaxis_title="Value")
    return fig

def create_line_chart_PUBLIC(selected_category):
    fig = go.Figure()
    colors = {"Receipts": "blue", "Expenditures": "green", "Predicted": "red"}
    all_colors = ["blue", "green", "orange", "purple", "brown"]  # Different colors for 'All' option
    
    if selected_category == "All":
        for i, category in enumerate(category_list[1:]):  # Skip "All" in iteration
            for data_type in ["Receipts", "Expenditures"]:
                y_column = f"{category}_{data_type}"
                fig.add_trace(go.Scatter(
                    x=df_public['Year'],
                    y=df_public[y_column],
                    mode='lines+markers',
                    name=f"{category.replace('_', ' ')} {data_type}",
                    line=dict(color=all_colors[i % len(all_colors)])
                ))
    else:
        for data_type in ["Receipts", "Expenditures"]:
            y_column = f"{selected_category}_{data_type}"
            fig.add_trace(go.Scatter(
                x=df_public['Year'],
                y=df_public[y_column],
                mode='lines+markers',
                name=data_type,
                line=dict(color=colors[data_type])
            ))
            
            # Highlight predicted year
            fig.add_trace(go.Scatter(
                x=[predicted_year],
                y=[df_public[df_public['Year'] == predicted_year][y_column].values[0]],
                mode='markers',
                name=f"{data_type} (Predicted)",
                marker=dict(color=colors["Predicted"], size=10, symbol='circle-open')
            ))
    
    fig.update_layout(title=f"{selected_category.replace('_', ' ')}: Receipts & Expenditures Over Years", 
                      xaxis_title="Year", 
                      yaxis_title="Value")
    return fig


def create_line_chart_ut(selected_ut):
    fig = go.Figure()
    colors = {"Receipts": "blue", "Expenditures": "green", "Predicted": "red"}    # Dropdown options
    # Dropdown options
    ut_list = ["ALL"] + ["CHANDIGARH", "ANDAMAN AND NICOBAR ISLANDS", "DADRA AND NAGAR HAVELI DAMAN AND DIU", "LAKSHADWEEP", "LADAKH"]

    if selected_ut == "ALL":
        for ut in ut_list[1:]:
            for data_type in ["Receipts", "Expenditures"]:
                y_column = f"{ut}_{data_type}"
                fig.add_trace(go.Scatter(
                    x=df_ut['Year'],
                    y=df_ut[y_column],
                    mode='lines+markers',
                    name=f"{ut} {data_type}",
                    line=dict(width=1)
                ))
    else:
        for data_type in ["Receipts", "Expenditures"]:
            y_column = f"{selected_ut}_{data_type}"
            fig.add_trace(go.Scatter(
                x=df_ut['Year'],
                y=df_ut[y_column],
                mode='lines+markers',
                name=data_type,
                line=dict(color=colors[data_type])
            ))
            
            # Highlight predicted year
            fig.add_trace(go.Scatter(
                x=[predicted_year],
                y=[df_ut[df_ut['Year'] == predicted_year][y_column].values[0]],
                mode='markers',
                name=f"{data_type} (Predicted)",
                marker=dict(color=colors["Predicted"], size=10, symbol='circle-open')
            ))
    
    fig.update_layout(title=f"{selected_ut}: Receipts & Expenditures Over Years", xaxis_title="Year", yaxis_title="Value")
    return fig

def create_line_chart1(title, y_columns):
    fig = go.Figure()
    colors = {"Receipts": "blue", "Expenditures": "green", "Predicted": "red"}
    color_palette = ["blue", "green", "orange", "purple", "brown", "pink", "gray", "cyan"]
    predicted_color = "red"
    for i, col in enumerate(y_columns):
        color = color_palette[i % len(color_palette)]  # Assign unique colors
        fig.add_trace(go.Scatter(
            x=df_ut['Year'],
            y=df_ut[col],
            mode='lines+markers',
            name=col,
            line=dict(dash='solid', color=color),
            marker=dict(size=6)
        ))
    
    # Highlight predicted year
    for i, col in enumerate(y_columns):
        fig.add_trace(go.Scatter(
            x=[predicted_year],
            y=[df_ut[df_ut['Year'] == predicted_year][col].values[0]],
            mode='markers',
            name=f"{col} (Predicted)",
            marker=dict(color=predicted_color, size=10, symbol='circle-open')
        ))
    
    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value")
    return fig

app.layout = html.Div([

    dbc.Carousel(
        items=[
            {"key": "1", "src": "/assets/5.jpg?text=Slide+1", "caption": ""},
            {"key": "2", "src": "/assets/7.jpg?text=Slide+2", "caption": ""},
            {"key": "3", "src": "/assets/6.jpg?text=Slide+3", "caption": ""},
        ],
        controls=True, 
        indicators=True,
        interval=2000,
    ),

    html.Hr(),


    html.Div(["Forecasted Union Budget 2025-2026"], 
        style={
            "font-size": "38px",
            "font-weight": "bold",
            "text-align": "center",
        }),

    html.Div([

        html.Img(src="/assets/png-banner.png", style={"width": "100%", "object-fit": "cover"}),

        dbc.Container([
            dbc.NavbarSimple(
                children=[
                    # dbc.NavItem(dbc.NavLink("Total", href="/total", style={"color": "white"})),

                    # html.Div(" | ", style={"color": "white", "margin-top":"6px", "margin-left":"5px", "margin-right": "5px"}),
                    html.Div(" | ", style={"color": "white", "margin-top":"6px", "margin-left":"5px", "margin-right": "5px"}),

                    dbc.NavItem(dbc.NavLink("HOME ", href="/", style={"color": "white"})),

                    html.Div(" | ", style={"color": "white", "margin-top":"6px", "margin-left":"5px", "margin-right": "5px"}),

                    dbc.DropdownMenu(
                        label="Statement I - Consolidated Fund of India",
                        children=[

                            dbc.DropdownMenuItem("Revenue Account", href="/revenue",
                            style={
                                "min-width": "320px",
                                "white-space": "nowrap",
                                "padding": "10px 20px"
                            }),

                            dbc.DropdownMenuItem("Capital Account", href="/capital",
                            style={
                                "min-width": "320px",
                                "white-space": "nowrap",
                                "padding": "10px 20px"
                            }),
                            
                            dbc.DropdownMenuItem("Total", href="/total",
                            style={
                                "min-width": "320px",
                                "white-space": "nowrap",
                                "padding": "10px 20px"
                            }),
                        ],
                        style={"width": "auto"}
                    ),

                    html.Div(" | ", style={"color": "white", "margin-top":"6px", "margin-left":"5px", "margin-right": "5px"}),

                    dbc.NavItem(dbc.NavLink("Statment IA - Disbursements Charged", href="/total1", style={"color": "white"})),

                    html.Div(" | ", style={"color": "white", "margin-top":"6px", "margin-left":"5px", "margin-right": "5px"}),

                    dbc.DropdownMenu(
                        label="Statement III - Public Account of India",
                        children=[
                            dbc.DropdownMenuItem("Union Territories (without Legislature)", href="/ut",
                            style={
                                "min-width": "300px",
                                "white-space": "nowrap",
                                "padding": "10px 20px"
                            }),
                            dbc.DropdownMenuItem("Public Account", href="/public",
                            style={
                                "min-width": "300px",
                                "white-space": "nowrap",
                                "padding": "10px 20px"
                            }),
                        ],
                        style={"width": "auto"}
                    ),
                ],
                brand="Budget Dashboard",
                color="primary",
                dark=True,
            ),
            dcc.Location(id="url", refresh=False),
            html.Div(id="page-content")
        ]
        , 
        style={
            "position": "relative",
            "margin-top": "-110px"
        }
        ),

        html.Img(src="/assets/png-banner-btm.png", style={"width": "100%", "object-fit": "cover"}),

    ], 
    style={
        "background-color": "#fcefdf",
        "position": "relative",
        "text-align": "center",
        "background-color": "#fcefdf"
    })

]),

@app.callback(
    Output("page-content", "children"),
    [Input("url", "pathname")]
)
def display_page(pathname):
    # if pathname is None or pathname == "/":
    #     # pathname = "/total"
    if pathname == "/":
        # Replace this with your actual data for Total Receipts and Expenditures
        df_receipts_expenditures = pd.read_excel("Cumulative_Budget_Predicted.xlsx")  # Example filename
        # Ensure correct column names
        df_receipts_expenditures.rename(columns={"YEAR": "Year"}, inplace=True)
        df_receipts_expenditures['Year'] = pd.to_datetime(df_receipts_expenditures['Year']).dt.year  # Convert to integer years

        # Bar chart for Total Receipts and Expenditure Over the Years
        bar_fig = go.Figure()
        bar_fig.add_trace(go.Bar(x=df_receipts_expenditures['Year'], 
                                  y=df_receipts_expenditures['Total Receipts'], 
                                  name='Total Receipts', 
                                  marker_color='blue'))
        bar_fig.add_trace(go.Bar(x=df_receipts_expenditures['Year'], 
                                  y=df_receipts_expenditures['Total Expenditure'], 
                                  name='Total Expenditure', 
                                  marker_color='green'))
        bar_fig.update_layout(barmode='group', 
                              title='Total Receipts and Expenditure Over the Years', 
                              xaxis_title='Year', 
                              yaxis_title='Amount')

        # Line chart combining Revenue Deficit, Fiscal Deficit, and Primary Deficit
        line_fig = go.Figure()
        line_fig.add_trace(go.Scatter(x=df_receipts_expenditures['Year'], 
                                       y=df_receipts_expenditures['Revenue Deficit'], 
                                       mode='lines+markers', 
                                       name='Revenue Deficit', 
                                       line=dict(color='blue')))
        line_fig.add_trace(go.Scatter(x=df_receipts_expenditures['Year'], 
                                       y=df_receipts_expenditures['Fiscal Deficit'], 
                                       mode='lines+markers', 
                                       name='Fiscal Deficit', 
                                       line=dict(color='red')))
        line_fig.add_trace(go.Scatter(x=df_receipts_expenditures['Year'], 
                                       y=df_receipts_expenditures['Primary Deficit'], 
                                       mode='lines+markers', 
                                       name='Primary Deficit', 
                                       line=dict(color='green')))
        line_fig.update_layout(title='Deficit Trends Over the Years', 
                               xaxis_title='Year', 
                               yaxis_title='Amount')
        # total_columns1 = ["TOTAL_CONSOLIDATED_FUND_OF_INDIA_RECEIPTS", "TOTAL_CONSOLIDATED_FUND_OF_INDIA_DISBURSEMENTS"]

        return html.Div([
            html.H1("Welcome to AI Enabled Budget Forecasting", style={"textAlign": "center"}),
            dcc.Graph(id="total-receipts-expenditures", figure=bar_fig),
            dcc.Graph(id="deficit-trends", figure=line_fig),
            dcc.Graph(figure=create_line_chart(df_receipts_expenditures, df_receipts_expenditures, "Budgetary Trends Over the Years"))
        ])
    
    elif pathname == "/capital":
        return html.Div([
            html.H1("Capital Account - Receipts & Expenditures", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            
            html.Div([
                dcc.Graph(
                    id="public-debt-pie-1",
                    figure=go.Figure(
                        data=[go.Pie(
                            labels=["TOTAL_INTERNAL_DEBT_OF_CENTRAL_GOVERNMENT", "EXTERNAL_DEBT_Receipts"],
                            values=[df_capital.iloc[-1]["TOTAL_INTERNAL_DEBT_OF_CENTRAL_GOVERNMENT"], df_capital.iloc[-1]["EXTERNAL_DEBT_Receipts"]],
                            hole=0.3
                        )]
                    ).update_layout(
                        title=f"Public Debt Composition in {df_capital.iloc[-1]['Year']}",
                        width=555,
                        height=500,
                        legend=dict(
                            orientation="h",
                            x=0.5,
                            y=-0.2,
                            xanchor="center",
                            yanchor="top"
                        )
                    )
                ),
                dcc.Graph(
                    id="public-debt-pie-2",
                    figure=go.Figure(
                        data=[go.Pie(labels=["CAPITAL_ACCOUNT_OF_GENERAL_SERVICES", "CAPITAL_ACCOUNT_OF_SOCIAL_SERVICES", "CAPITAL_ACCOUNT_OF_ECONOMIC_SERVICES"], 
                                    values=[df_capital.iloc[-1]["CAPITAL_ACCOUNT_OF_GENERAL_SERVICES"], df_capital.iloc[-1]["CAPITAL_ACCOUNT_OF_SOCIAL_SERVICES"], df_capital.iloc[-1]["CAPITAL_ACCOUNT_OF_ECONOMIC_SERVICES"]],
                                    hole=0.3)]
                    ).update_layout(
                        title=f"Sector-wise Capital Expenditure in {df_capital.iloc[-1]['Year']}",
                        width=555,
                        height=500,
                        legend=dict(
                            orientation="h",
                            x=0.5,
                            y=-0.2,
                            xanchor="center",
                            yanchor="top"
                        )
                    )
                ),
            ], style={'display': 'flex', 'justify-content': 'space-around'}),
            dcc.Graph(
                id="total-public-debt-trend",
                figure=create_line_chart_CAPITAL(df_capital, ["TOTAL_PUBLIC_DEBT_Receipts", "TOTAL_PUBLIC_DEBT_Expenditures", "CAPITAL_ACCOUNT_OF_GENERAL_SERVICES", "CAPITAL_ACCOUNT_OF_SOCIAL_SERVICES", "CAPITAL_ACCOUNT_OF_ECONOMIC_SERVICES"], "Total Public Debt: Receipts vs Expenditures").update_layout(yaxis_type="log")
            ),
            dcc.Graph(
                id="breakdown-capital-receipts",
                figure=create_line_chart_CAPITAL(df_capital, ["TOTAL_INTERNAL_DEBT_OF_CENTRAL_GOVERNMENT", "EXTERNAL_DEBT_Receipts", "TOTAL_RECOVERIES_OF_LOANS_AND_ADVANCES", "MISCELLANEOUS_CAPITAL_RECEIPTS"], "Breakdown of Capital Receipts Over the Years").update_layout(yaxis_type="log")
            )
        ])
    
    elif pathname == "/revenue":
         
    
         return html.Div([
            html.H1("Revenue Account - Receipts & Expenditures", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            html.H3("Revenue Components", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            
            dcc.Graph(figure=create_line_chart_REVENUE(df_revenue,revenue_columns, "Revenue Components Over Years")),
            # dcc.Graph(figure=create_bar_chart(revenue_columns, "Revenue Breakdown by Year")),
            dcc.Graph(figure=create_pie_chart_revenue(df_revenue,revenue_columns, "Revenue Distribution ")),
            
            html.H3("Expenditure Components", style={"textAlign": "center","margin-top":"10px","background-color": "rgba(255,255,255, 0.6)"}),
            dcc.Graph(figure=create_line_chart_REVENUE(df_revenue,expenditure_columns, "Expenditure Components Over Years")),
            # dcc.Graph(figure=create_bar_chart(expenditure_columns, "Expenditure Breakdown by Year")),
            dcc.Graph(figure=create_pie_chart_revenue(df_revenue,expenditure_columns, "Expenditure Distribution ")),
            
            html.H3("Non-Tax Revenue Components", style={"textAlign": "center","margin-top":"10px","background-color": "rgba(255,255,255, 0.6)"}),
            dcc.Graph(figure=create_line_chart_REVENUE(df_revenue,nontax_columns, "Non-Tax Revenue Components Over Years")),
            # dcc.Graph(figure=create_bar_chart(nontax_columns, "Non-Tax Revenue Breakdown by Year")),
            dcc.Graph(figure=create_pie_chart_revenue(df_revenue,nontax_columns, "Non-Tax Revenue Distribution ")),
        ])
    
    elif pathname == "/ut":
        return html.Div([

            html.H1("Union Territories (without Legislature) - Receipts & Expenditures", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            dcc.Graph(
                id="public-debt-pie-1",
                figure=go.Figure(
                    data=[go.Pie(labels=["Total Receipts vs Expenditures", "Total_Expenditures"], 
                                values=[df_ut.iloc[-1]["Total_Receipts"], df_ut.iloc[-1]["Total_Expenditures"]],
                                hole=0.3)]
                ).update_layout(title=f"Predicted Total Receipts vs Expenditures in {df_ut.iloc[-1]['Year']}")
            ),
            dcc.Graph(
                id="total-receipts-expenditures",
                figure=create_line_chart1("Total Receipts vs Expenditures", 
                                        ["Total_Receipts", "Total_Expenditures"])
            ),
            # html.Label("Select Union Territory:"),
            # html.H3("Select Union Territory:", style={"textAlign": "center","margin-top":"10px","background-color": "rgba(255,255,255, 0.6)"}),
            # dcc.Dropdown(
            #     id="ut-selector",
            #     options=[{"label": ut, "value": ut} for ut in ut_list],
            #     value="ALL",
            #     clearable=False
            # ),
            # dcc.Graph(id="dynamic-ut-chart")

            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Label("Select Union Territory:", style={"font-weight": "bold", "margin-right": "10px"}), 
                            width="auto"), 
                    
                    dbc.Col(
                        dcc.Dropdown(
                            id="ut-selector",
                            options=[{"label": ut, "value": ut} for ut in ut_list],
                            style={"width": "600px"},
                            value="ALL",
                            clearable=False
                        ),
                        width="auto"
                    )
                ], align="center", justify="center", style={"margin-top": "30px", "margin-bottom": "10px"})  # Align label and dropdown vertically
            ], fluid=True),

            dcc.Graph(id="dynamic-ut-chart")

        ])
    
    elif pathname == "/public":
        return html.Div([
            html.H1("Public Account - Receipts & Expenditures", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            html.Div([
                dcc.Graph(
                    id="public-debt-pie-1",
                    figure=go.Figure(
                        data=[go.Pie(labels=["National_Small_Savings_Fund_Receipts", "State_Provident_Fund_Receipts","Reserve_Funds_Receipts","Deposits_and_Advances_Receipts"], 
                                    values=[df_public.iloc[-1]["National_Small_Savings_Fund_Receipts"], df_public.iloc[-1]["State_Provident_Fund_Receipts"],df_public.iloc[-1]["Reserve_Funds_Receipts"],df_public.iloc[-1]["Deposits_and_Advances_Receipts"]],
                                    hole=0.3)]
                    ).update_layout(title=f"Public Saving in {df_public.iloc[-1]['Year']}",
                        width=555,
                        height=500, 
                        legend=dict(
                            orientation="h",
                            x=0.5,
                            y=-0.2,
                            xanchor="center",
                            yanchor="top"
                        )
                    )
                ),
                dcc.Graph(
                    id="public-debt-pie-2",
                    figure=go.Figure(
                        data=[go.Pie(labels=["National_Small_Savings_Fund_Expenditures", "State_Provident_Fund_Expenditures", "Reserve_Funds_Expenditures","Deposits_and_Advances_Expenditures"], 
                                    values=[df_public.iloc[-1]["National_Small_Savings_Fund_Expenditures"], df_public.iloc[-1]["State_Provident_Fund_Expenditures"], df_public.iloc[-1]["Reserve_Funds_Expenditures"], df_public.iloc[-1]["Deposits_and_Advances_Expenditures"]],
                                    hole=0.3)]
                    ).update_layout(title=f"Public Expenditure in {df_public.iloc[-1]['Year']}",
                        width=555,
                        height=500,
                        legend=dict(
                            orientation="h",
                            x=0.5,
                            y=-0.2,
                            xanchor="center",
                            yanchor="top"
                        )
                    )
                )
            ], style={'display': 'flex', 'justify-content': 'space-around'}),


            # html.Label("Select Category:"),
            # dcc.Dropdown(
            #     id="category-selector",
            #     options=[{"label": cat.replace('_', ' '), "value": cat} for cat in category_list],
            #     value="National_Small_Savings_Fund",
            #     clearable=False
            # ),
            # dcc.Graph(id="dynamic-line-chart")

            dbc.Container([
                dbc.Row([
                    dbc.Col(html.Label("Select Category:", style={"font-weight": "bold", "margin-right": "10px"}), 
                            width="auto"),
                    
                    dbc.Col(
                        dcc.Dropdown(
                            id="category-selector",
                            options=[{"label": cat.replace('_', ' '), "value": cat} for cat in category_list],
                            style={"width": "600px"},
                            value="National_Small_Savings_Fund",
                            clearable=False
                        ),
                        width="auto"
                    )
                ], align="center", justify="center", style={"margin-top": "30px", "margin-bottom": "10px"})  # Align label and dropdown vertically
            ], fluid=True),
            
            dcc.Graph(id="dynamic-line-chart")
    
        ])
    
    elif pathname == "/total":
        return html.Div([
            html.H1("Total Receipt & Expenditures (Consolidated Fund of India)", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
            html.H3("Consolidated Fund Components", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),

            dcc.Graph(figure=create_line_chart_REVENUE(df_total, total_columns1, "Consolidated Fund Components Over Years")),
            dcc.Graph(figure=create_bar_chart_revenue(df_total, total_columns1, "Consolidated Fund Breakdown by Year")),
            dcc.Graph(figure=create_pie_chart_revenue(df_total, total_columns1, "Consolidated Fund Distribution "))
        ]) 


    elif pathname == "/total1":
        return html.Div([
             html.H1("Disbursements Charged on the Consolidated Fund of India", style={"textAlign": "center","background-color": "rgba(255,255,255, 0.6)"}),
             dcc.Graph(figure=create_line_chart_REVENUE(df_total, total_columns, "Grand Total Components Over Years")),
             dcc.Graph(figure=create_bar_chart_revenue(df_total, total_columns, "Grand Total Breakdown by Year")),
        ])
    

    return html.H3("Welcome to AI Enabled Budget Forcasting")

@app.callback(
    Output("dynamic-ut-chart", "figure"),
    [Input("ut-selector", "value")]
)
def update_ut_chart(selected_ut):
    return create_ut_chart(selected_ut)
@app.callback(
    dash.dependencies.Output("dynamic-line-chart", "figure"),
    [dash.dependencies.Input("category-selector", "value")]
)

def update_line_chart(selected_category):
    return create_line_chart_PUBLIC(selected_category)

# app.run_server(debug=True, host='0.0.0.0', port=8050)

if __name__ == "__main__":
    app.run_server(debug=True)
