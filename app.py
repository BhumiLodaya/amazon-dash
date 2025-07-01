import pandas as pd
import plotly.express as px
import dash
from dash import html, dcc
import os

# Debug print for local / Render logs
print("✅ Current directory contents:", os.listdir())

# Load CSV safely
try:
    df = pd.read_csv("C:/Users/bhumi/OneDrive/Desktop/professional/internship/sales/sales_cleaned.csv", low_memory=False)
    print("✅ CSV Loaded Successfully")
    print("Columns:", df.columns.tolist())
except Exception as e:
    print("❌ CSV Load Failed:", e)
    df = pd.DataFrame()

# Clean column names
df.columns = df.columns.str.strip()  # remove extra spaces
df.rename(columns={'Sales Channel ': 'Sales Channel'}, inplace=True)

# Start Dash app
app = dash.Dash(__name__)
server = app.server  # Needed for deployment on platforms like Render

# Layout
app.layout = html.Div(
    style={'backgroundColor': '#111111', 'color': '#FFFFFF', 'padding': '20px'},
    children=[
        html.H1("📊 Amazon Sales Dashboard", style={'textAlign': 'center'}),

        # Sales by Category
        dcc.Graph(
            id='sales-by-category',
            figure=px.bar(
                df.groupby('Category', as_index=False)['Amount'].sum(),
                x='Category', y='Amount',
                title='Sales by Category',
                color='Category',
                color_discrete_sequence=px.colors.qualitative.Bold
            ).update_layout(paper_bgcolor='#111111', plot_bgcolor='#111111', font_color='white')
        ),
        html.P("📦 This bar chart shows total sales grouped by product category. It helps you identify the most profitable product types."),

        # Top Shipping Cities
        dcc.Graph(
            id='top-cities',
            figure=px.bar(
                df.groupby('ship-city')['Amount'].sum().nlargest(10).reset_index(),
                x='ship-city', y='Amount',
                title='Top 10 Shipping Cities by Sales',
                color='ship-city',
                color_discrete_sequence=px.colors.sequential.Viridis
            ).update_layout(paper_bgcolor='#111111', plot_bgcolor='#111111', font_color='white')
        ),
        html.P("🏙️ These are the top 10 cities based on shipping-related sales, revealing where most purchases are being shipped."),

        # Top Shipping States
        dcc.Graph(
            id='top-states',
            figure=px.bar(
                df.groupby('ship-state', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False).head(10),
                x='ship-state', y='Amount',
                title='Top 10 Shipping States by Sales',
                color='ship-state',
                color_discrete_sequence=px.colors.sequential.Aggrnyl
            ).update_layout(paper_bgcolor='#111111', plot_bgcolor='#111111', font_color='white')
        ),
        html.P("📌 This bar chart shows the top 10 states in India based on total order value, revealing regional demand."),

        # Sales by Product Size
        dcc.Graph(
            id='sales-by-size',
            figure=px.bar(
                df.groupby('Size', as_index=False)['Amount'].sum().sort_values(by='Amount', ascending=False),
                x='Size', y='Amount',
                title='Sales by Product Size',
                color='Size',
                color_discrete_sequence=px.colors.qualitative.Safe
            ).update_layout(paper_bgcolor='#111111', plot_bgcolor='#111111', font_color='white')
        ),
        html.P("📐 This chart breaks down total sales based on product sizes. It helps identify which sizes perform best."),

        # Sales Distribution by Order Status
        dcc.Graph(
            id='status-distribution',
            figure=px.pie(
                df, names='Status', values='Amount',
                title='Sales Distribution by Order Status',
                color_discrete_sequence=px.colors.sequential.Rainbow
            ).update_layout(paper_bgcolor='#111111', font_color='white')
        ),
        html.P("📦 This pie chart shows how much revenue each delivery status contributes, such as Delivered, Cancelled, or Returned."),

        html.H3("💡 More Insights Coming Soon!", style={'marginTop': '40px'}),
        html.P("Additional dashboards like Product Performance, Customer Return Rate, and Region-wise Profitability will be added.")
    ]
)

# Run the app locally
if __name__ == '__main__':
    app.run(debug=True)
