import streamlit as st
import pandas as pd
import plotly.express as px

# Page Config

st.set_page_config(page_title="Superstore Dashboard", layout="wide")

# Load Dataset

url = "https://raw.githubusercontent.com/leonism/sample-superstore/master/data/superstore.csv"
df = pd.read_csv(url)

# Data Cleaning

df.dropna(subset=["Customer ID"], inplace=True)
df.drop_duplicates(inplace=True)

# Date Conversion

df["Order Date"] = pd.to_datetime(df["Order Date"])

# Sidebar Filters

st.sidebar.header("Filters")

selected_region = st.sidebar.multiselect(
"Region",
options=df["Region"].unique(),
default=df["Region"].unique()
)

selected_category = st.sidebar.multiselect(
"Category",
options=df["Category"].unique(),
default=df["Category"].unique()
)

selected_segment = st.sidebar.multiselect(
"Segment",
options=df["Segment"].unique(),
default=df["Segment"].unique()
)

# Apply Filters

filtered_df = df[
(df["Region"].isin(selected_region))
& (df["Category"].isin(selected_category))
& (df["Segment"].isin(selected_segment))
].copy()

# Title

st.title("Superstore Sales Dashboard")

# KPIs

st.header("Key Metrics")

total_sales = filtered_df["Sales"].sum()
total_profit = filtered_df["Profit"].sum()
total_orders = filtered_df["Order ID"].nunique()
total_customers = filtered_df["Customer ID"].nunique()
total_products = filtered_df["Product ID"].nunique()

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Sales", f"₹{total_sales:,.0f}")
c2.metric("Total Profit", f"₹{total_profit:,.0f}")
c3.metric("Total Orders", total_orders)
c4.metric("Total Customers", total_customers)
c5.metric("Total Products", total_products)

# Chart 1 - Sales by Region

st.header("Sales by Region")

region_sales = (
filtered_df.groupby("Region")["Sales"]
.sum()
.reset_index()
)

fig1 = px.bar(
region_sales,
x="Region",
y="Sales",
title="Sales by Region"
)

st.plotly_chart(fig1, use_container_width=True)

# Chart 2 - Profit by Category

st.header("Profit by Category")

category_profit = (
filtered_df.groupby("Category")["Profit"]
.sum()
.reset_index()
)

fig2 = px.bar(
category_profit,
x="Category",
y="Profit",
title="Profit by Category"
)

st.plotly_chart(fig2, use_container_width=True)

# Chart 3 - Year-wise Sales Trend

st.header("Year-wise Sales Trend")

filtered_df["Year"] = filtered_df["Order Date"].dt.year

year_sales = (
filtered_df.groupby("Year")["Sales"]
.sum()
.reset_index()
)

fig3 = px.line(
year_sales,
x="Year",
y="Sales",
markers=True,
title="Year-wise Sales Trend"
)

st.plotly_chart(fig3, use_container_width=True)

# Chart 4 - Sales by Segment

st.header("Sales by Segment")

segment_sales = (
filtered_df.groupby("Segment")["Sales"]
.sum()
.reset_index()
)

fig4 = px.pie(
segment_sales,
names="Segment",
values="Sales",
title="Sales by Segment"
)

st.plotly_chart(fig4, use_container_width=True)

# Chart 5 - Top 10 Products

st.header("Top 10 Products by Sales")

top_products = (
filtered_df.groupby("Product Name")["Sales"]
.sum()
.sort_values(ascending=False)
.head(10)
.reset_index()
)

fig5 = px.bar(
top_products,
x="Sales",
y="Product Name",
orientation="h",
title="Top 10 Products"
)

st.plotly_chart(fig5, use_container_width=True)

# Dataset Preview

st.header("Dataset Preview")
st.dataframe(filtered_df.head())
