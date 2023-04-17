import mysql.connector
import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd

mydb = mysql.connector.connect(
    host="127.0.0.1",
    port=3308,
    user="root",
    password="",
    database="sales_data_db"
)

mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM transactions")
transactions = mycursor.fetchall()

transactions_df = pd.DataFrame(transactions, columns=["TransactionID", "Date", "EmployeeID", "ProductID", "SalesAmount"])

mycursor.execute("SELECT * FROM products")
products = mycursor.fetchall()

product_df = pd.DataFrame(products, columns=["ProductID", "ProductName", "ProductCategory", "ProductPrice"])

merged_df = pd.merge(transactions_df, product_df, on="ProductID", how="left")

fig = px.scatter(merged_df, x="SalesAmount", y="Date", color="EmployeeID", hover_data=["ProductName", "ProductCategory", "ProductPrice"])

app = dash.Dash(__name__)

app.layout = html.Div(children=[
    html.H1(children='Sales Transactions Scatter Plot'),
    
    dcc.Graph(
        id='scatter-plot',
        figure=fig
    ),
    
    html.Br(),
    
    html.Label('Select Employee:'),
    dcc.Dropdown(
        id='employee-dropdown',
        options=[
            {'label': 'Employee 1', 'value': 1},
            {'label': 'Employee 2', 'value': 2},
            {'label': 'Employee 3', 'value': 3},
            {'label': 'Employee 4', 'value': 4},
            {'label': 'Employee 5', 'value': 5}
        ],
        value=1
    ),
    
    html.Br(),
    
    html.Label('Select Product:'),
    dcc.Dropdown(
        id='product-dropdown',
        options=[{'label': row['ProductName'], 'value': row['ProductID']} for index, row in product_df.iterrows()],
        value=1
    ),
    
    html.Br(),
    
    dcc.Graph(
        id='employee-sales-plot'
    )
])

@app.callback(
    dash.dependencies.Output('employee-sales-plot', 'figure'),
    [dash.dependencies.Input('employee-dropdown', 'value'),
     dash.dependencies.Input('product-dropdown', 'value')])
def update_employee_sales(employee_value, product_value):
    filtered_df = merged_df[(merged_df['EmployeeID'] == employee_value) & (merged_df['ProductID'] == product_value)]
    employee_sales_fig = px.bar(filtered_df, x='Date', y='SalesAmount')
    return employee_sales_fig

if __name__ == '__main__':
    app.run_server(debug=True)
