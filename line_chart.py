import plotly.graph_objects as go
# import plotly.graph_objects as go
import plotly.express as px
color_palette = ["blue", "green", "orange", "purple", "brown", "pink", "gray", "cyan"]
predicted_color = "red"


def create_line_chart_CAPITAL(df, columns, title):
    # Identify predicted data (last row)
    predicted_year = df.iloc[-1]['Year']
    df['is_predicted'] = df['Year'] == predicted_year

    fig = go.Figure()
    for i, col in enumerate(columns):
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df[col],
            mode='lines+markers',
            name=col.replace('_', ' '),
            line=dict(color=color_palette[i % len(color_palette)])
        ))

        # Highlight predicted year
    for i, col in enumerate(columns):
        fig.add_trace(go.Scatter(
            x=[predicted_year],
            y=[df[df['Year'] == predicted_year][col].values[0]],
            mode='markers',
            name=f"{col} (Predicted)",
            marker=dict(color=predicted_color, size=10, symbol='circle-open')
        ))

    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value")

    return fig

def create_line_chart_REVENUE(df, columns, title):
    fig = go.Figure()
    predicted_year = df.iloc[-1]['Year']
    df['is_predicted'] = df['Year'] == predicted_year

    for i, col in enumerate(columns):
        color = color_palette[i % len(color_palette)]  # Assign unique colors
        fig.add_trace(go.Scatter(
            x=df['Year'],
            y=df[col],
            mode='lines+markers',
            name=col,
            line=dict(dash='solid', color=color),
            marker=dict(size=6)
        ))
    
    # Highlight predicted year
    for i, col in enumerate(columns):
        fig.add_trace(go.Scatter(
            x=[predicted_year],
            y=[df[df['Year'] == predicted_year][col].values[0]],
            mode='markers',
            name=f"{col} (Predicted)",
            marker=dict(color=predicted_color, size=10, symbol='circle-open')
        ))
    
    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value")
    return fig


def create_bar_chart_revenue(df, columns, title):
    fig = go.Figure()
    for i, col in enumerate(columns):
        fig.add_trace(go.Bar(
            x=df['Year'],
            y=df[col],
            name=col.replace('_', ' '),
            marker=dict(color=color_palette[i % len(color_palette)])
        ))
    
    fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value", barmode='group')
    return fig

def create_pie_chart_revenue(df, columns, title):
    
    latest_year_data = df[df['Year'] == df['Year'].max()].iloc[0]
    values = [latest_year_data[col] for col in columns]
    labels = [col.replace('_', ' ') for col in columns]
    title = title + str(df.iloc[-1]['Year'])
    fig = px.pie(values=values, names=labels, title=title, color_discrete_sequence=color_palette)
    return fig

# def create_line_chart_UT(df, columns, title):
#     fig = go.Figure()
#     for i, col in enumerate(columns):
#         fig.add_trace(go.Scatter(
#             x=df['Year'],
#             y=df[col],
#             mode='lines+markers',
#             name=col.replace('_', ' '),
#             line=dict(color=color_palette[i % len(color_palette)])
#         ))
#     fig.update_layout(title=title, xaxis_title="Year", yaxis_title="Value")
#     return fig

# def create_ut_chart(df_ut,selected_ut,ut_list):
#     fig = go.Figure()
#     if selected_ut == "ALL":
#         for ut in ut_list[1:]:
#             for data_type in ["Receipts", "Expenditures"]:
#                 y_column = f"{ut}_{data_type}"
#                 fig.add_trace(go.Scatter(
#                     x=df_ut['Year'],
#                     y=df_ut[y_column],
#                     mode='lines+markers',
#                     name=f"{ut} {data_type}",
#                     line=dict(width=1)
#                 ))
#     else:
#         for data_type in ["Receipts", "Expenditures"]:
#             y_column = f"{selected_ut}_{data_type}"
#             fig.add_trace(go.Scatter(
#                 x=df_ut['Year'],
#                 y=df_ut[y_column],
#                 mode='lines+markers',
#                 name=data_type,
#                 line=dict(color=color_palette[0 if data_type == "Receipts" else 1])
#             ))
#     fig.update_layout(title=f"{selected_ut}: Receipts & Expenditures Over Years", xaxis_title="Year", yaxis_title="Value")
#     return fig