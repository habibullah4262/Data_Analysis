import streamlit as st #streamlit - Front end framework
import pandas as pd #data wrangling library in python
import plotly.express as px #Dynamic Visualization library in python


st.title("E-commerce Sales analysis Dashboard")

# data=pd.read_csv("supermarket_sales.csv")

# st.dataframe(data)


def load_data(file_path):
    data=pd.read_csv(file_path)
    data["Date"]=pd.to_datetime(data["Date"],errors="coerce")
    data=data.dropna(subset=["Date"]) #remove with invalid dates
    data["Branch"]=data["Branch"].replace("A","Gulshan")
    data["Branch"]=data["Branch"].replace("B","Johar")
    data["Branch"]=data["Branch"].replace("C","Saddar")
    return data

data_path="./supermarket_sales.csv"

data= load_data(data_path)
st.sidebar.header("Filters")

#data=pd.read_csv("supermarket_sales.csv")
#st.dataframe(data)

select_branch=st.sidebar.multiselect("Select Branch",options=data["Branch"].unique())
select_product=st.sidebar.multiselect("Select Product",options=data["Product line"].unique())
select_customer=st.sidebar.multiselect("Select Customer Type",options=data["Customer type"].unique())
select_gender=st.sidebar.multiselect("Select Gender",options=data["Gender"].unique())

filtered_data= data[(data["Branch"].isin(select_branch)) & (data["Product line"].isin(select_product)) & (data["Customer type"].isin(select_customer)) & (data["Gender"].isin(select_gender))]

st.dataframe(filtered_data)

total_sales=filtered_data["Total"].sum().round(2)
gross_income=filtered_data["gross income"].sum().round(2)
total_cogs=filtered_data["cogs"].sum().round(2)
ave_rating=filtered_data["Rating"].mean()
total_quantity=filtered_data["Quantity"].sum().round(2)
cust_count=filtered_data["Invoice ID"].nunique()

st.subheader("Key Metrics")

col1,col2,col3,col4,col5,col6 = st.columns(6)

with col1:
    st.metric(label="Customer Count",value=cust_count)

with col2:
    st.metric(label="Total Sales",value=total_sales)

with col3:
    st.metric(label="Gross Income",value=gross_income)

with col4:  
    st.metric(label="Average Rating",value=ave_rating)

with col5:
    st.metric(label="Total Quantity",value=total_quantity)

with col6:
    st.metric(label="Total Costs on goods",value=total_cogs)


sales_by_gender=filtered_data.groupby("Gender")["Total"].sum().sort_values().reset_index()
#st.subheader(":::::::::::::::::::Total Sales by Gender::::::::::::::::")
col7,col8=st.columns(2)

with col7:
    fig_gender = px.bar(
        sales_by_gender,
        x="Gender",
        y="Total",
        title="Total Sales by Gender",
        text="Total",
        color="Gender"
    )

    st.plotly_chart(fig_gender)

sales_by_branch=filtered_data.groupby("Branch")["Total"].sum().sort_values().reset_index()

with col8:
    fig_branch = px.bar(
        sales_by_branch,
        x="Branch",
        y="Total",
        title="Total Sales by Branch",
        text="Total",
        color="Branch"
    )

    st.plotly_chart(fig_branch)


#Customer type:

sales_by_payment= filtered_data.groupby("Payment")["Total"].sum().reset_index()

fig_payment= px.pie(

    sales_by_payment,
    names="Payment",
    values="Total",
    title="Sales by Payment Method"
)

st.plotly_chart(fig_payment)