import streamlit as st
import pandas as pd
import plotly.express as px

# --- 1. SETUP PAGE ---
st.set_page_config(page_title="Pro Superstore Analytics", layout="wide")
st.title("📊 Integrated Business Performance Dashboard")

# --- 2. LOAD DATA ---
df = pd.read_csv('Sample - Superstore.csv', encoding='windows-1252')
df['Order Date'] = pd.to_datetime(df['Order Date'])

# --- 3. SIDEBAR CONTROLS ---
st.sidebar.header("Global Dashboard Controls")

# THE MASTER METRIC SELECTOR: Allows both or individual views
selected_metrics = st.sidebar.multiselect(
    "Choose Metrics to View:",
    options=["Sales", "Profit"],
    default=["Sales", "Profit"] # Default to showing both for comparison
)

# Geographic & Category Filters
regions = st.sidebar.multiselect("Select Region:", options=df["Region"].unique(), default=df["Region"].unique())
categories = st.sidebar.multiselect("Select Category:", options=df["Category"].unique(), default=df["Category"].unique())

# Apply filters to the data
df_selection = df.query("Region == @regions & Category == @categories")

# --- 4. DATA TRANSFORMATION ---
# We need to "melt" the data so we can plot multiple metrics (Sales/Profit) together
# This is the secret to getting distinctive colors on one chart
melted_df = df_selection.melt(
    id_vars=['Order Date', 'Region', 'Product Name'],
    value_vars=selected_metrics,
    var_name='Metric',
    value_name='Amount'
)

# --- 5. THE VISUALS ---

# Chart 1: Revenue & Profit Trends over Time
trend_data = melted_df.groupby([melted_df['Order Date'].dt.to_period('M'), 'Metric'])['Amount'].sum().reset_index()
trend_data['Order Date'] = trend_data['Order Date'].dt.to_timestamp()
fig_trend = px.line(
    trend_data, x='Order Date', y='Amount', color='Metric',
    title='Monthly Performance Trend', markers=True,
    color_discrete_map={'Sales': 'red', 'Profit': 'green'}
)

# Chart 2: Regional Comparison (Grouped)
reg_data = melted_df.groupby(['Region', 'Metric'])['Amount'].sum().reset_index()
fig_reg = px.bar(
    reg_data, x='Region', y='Amount', color='Metric', barmode='group',
    title='Regional Sales vs Profit',
    color_discrete_map={'Sales': 'red', 'Profit': 'green'}
)

# Chart 3: Top Products Comparison
prod_data = melted_df.groupby(['Product Name', 'Metric'])['Amount'].sum().reset_index()
# We sort by the first metric in your list to keep it organized
top_names = df_selection.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10).index
prod_data = prod_data[prod_data['Product Name'].isin(top_names)]

fig_prod = px.bar(
    prod_data, x='Amount', y='Product Name', color='Metric', barmode='group',
    orientation='h', title='Top 10 Products: Sales vs Profit',
    color_discrete_map={'Sales': 'red', 'Profit': 'green'}
)
fig_prod.update_layout(yaxis={'categoryorder':'total ascending'})

# --- 6. DISPLAY DASHBOARD ---
st.plotly_chart(fig_trend, width='stretch')

col1, col2 = st.columns(2)
with col1:
    st.plotly_chart(fig_reg, width='stretch')
with col2:
    st.plotly_chart(fig_prod, width='stretch')