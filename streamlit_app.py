
import streamlit as st

st.write('Hello')
import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output

st.write('after pandas')

import pyodbc




# Creating a connection string
connection_string = ("river={ODBC Driver 18 for SQL Server};Server=tcp:maria3159.database.windows.net,1433;Database=maria;Uid=maria;Pwd={Sana@3159};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

# Declare PYODBC connection with the string
cnxn = pyodbc.connect(connection_string)

# Declaring cursor
cursor = cnxn.cursor()

# Executing a select statement to fetch all records
cursor.execute("SELECT * FROM [dbo].[supermarkt_sales]")

# Fetch all results from the query
results = cursor.fetchall()

# Get column names from the cursor description
columns = [column[0] for column in cursor.description]

# Create a DataFrame from the fetched data
df = pd.DataFrame.from_records(results, columns=columns)

# Strip whitespace from column names
df.columns = df.columns.str.strip()

# Close the cursor and connection after using them
cursor.close()
cnxn.close()

# Initialize Dash app
app = Dash(__name__)

# Layout of the app
app.layout = html.Div([
    dcc.Tabs([
        dcc.Tab(label='Pie Chart', children=[
            dcc.Graph(id='pie-chart')
        ]),
        dcc.Tab(label='Data Table', children=[
            dash_table.DataTable(
                id='data-table',
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict('records'),
                page_size=10,  # Set the number of rows per page
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left'},
            )
        ])
    ])
])

# Callback to update the pie chart
@app.callback(
    Output('pie-chart', 'figure'),
    Input('pie-chart', 'id')
)
def update_pie_chart(_):
    product_line_column = 'Product_line'  # Use the correct column name

    if product_line_column in df.columns:
        product_line_counts = df[product_line_column].value_counts()
        fig = px.pie(
            names=product_line_counts.index,
            values=product_line_counts.values,
            title='Distribution of Product Lines',
            color_discrete_sequence=px.colors.qualitative.Set3  # Use a colorful palette
        )
        return fig
    return {}

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
