import pandas as pd
import plotly.express as px

# 1. Load the data
df = pd.read_csv('Sample - Superstore.csv', encoding='windows-1252')

# 2. THE MATH: Group by Product Name, add up the Sales, and sort highest to lowest
product_sales = df.groupby('Product Name')['Sales'].sum().reset_index()
top_10_products = product_sales.sort_values(by='Sales', ascending=False).head(10)

# 3. THE VISUAL: Build a horizontal bar chart
fig = px.bar(
    top_10_products,
    x='Sales',
    y='Product Name',
    orientation='h', # 'h' makes it horizontal so product names are easy to read
    title='Top 10 Highest Grossing Products'
)

# 4. Make it look neat by ordering the bars
fig.update_layout(yaxis={'categoryorder':'total ascending'})

# 5. Show it to the world!
fig.show()

# --- MISSION 2: PROFIT BY REGION ---

# 1. THE MATH: Group by Region and add up the Profit
region_profit = df.groupby('Region')['Profit'].sum().reset_index()

# 2. THE VISUAL: Build a vertical bar chart
fig2 = px.bar(
    region_profit,
    x='Region',
    y='Profit',
    color='Profit', # This adds the color scale based on profitability!
    title='Overall Profit by Region'
)

# 3. Make it look neat by ordering the bars highest to lowest
fig2.update_layout(xaxis={'categoryorder':'total descending'})

# 4. Show it!
fig2.show()

# --- MISSION 3: REVENUE TRENDS OVER TIME ---

# 1. THE DATA PREP: Tell pandas that 'Order Date' is an actual calendar date, not just text
df['Order Date'] = pd.to_datetime(df['Order Date'])

# 2. THE MATH: Group the data by Year and Month, and sum up the Sales
# We group by the specific month period, then convert it back to a timestamp so Plotly can draw it
monthly_sales = df.groupby(df['Order Date'].dt.to_period('M'))['Sales'].sum().reset_index()
monthly_sales['Order Date'] = monthly_sales['Order Date'].dt.to_timestamp()

# 3. THE VISUAL: Build a continuous line chart
fig3 = px.line(
    monthly_sales,
    x='Order Date',
    y='Sales',
    title='Revenue Trends Over Time (Monthly)',
    markers=True # This adds a little dot on the line for every single month!
)

# 4. Show it!
fig3.show()