import streamlit as st 
from db_helper import DB
import plotly.express as px
import pandas as pd
obj=DB()
st.sidebar.title("flight analytics")
user_option =st.sidebar.selectbox('menu',['select one','check flights','analytics'])
st.markdown("""
# ✈️ Flight Analytics Dashboard — User Guide

---

# 📌 Overview

The Flight Analytics Dashboard is an interactive web application developed using **Python**, **Streamlit**, **Pandas**, **SQL**, and **Plotly**.

The dashboard allows users to:
- Search available flights between cities
- Explore airline analytics
- Analyze airport traffic
- Visualize flight patterns using interactive charts
- Perform route-based flight analysis

The application is designed with a modern dark-themed user interface to provide a clean and user-friendly experience.

---

# 🚀 Accessing the Application

Open the deployed application using the provided project link.

The dashboard runs directly in the browser, so no local installation is required for users.

---

# 📘 Additional Documentation

For complete project details, technical implementation, source code, and setup instructions, refer to the project's GitHub README documentation.

The README contains:
- Project architecture
- Database details
- Installation guide
- SQL implementation
- Technologies used
- Source code explanation

---

# 🖥️ Dashboard Interface

The application interface is divided into two main sections:

---

# 1️⃣ Sidebar Panel

Located on the left side of the screen.

The sidebar contains:
- Dashboard title
- Navigation menu
- Feature selection dropdown
- Flight route controls

Menu options include:
- check flights
- analytics

The sidebar is used for interacting with the dashboard features.

---

# 2️⃣ Main Visualization Area

Located on the right side of the dashboard.

This section displays:
- Flight search results
- Interactive charts
- Airport analytics
- Airline statistics
- Visual insights

The displayed content changes dynamically based on user selections.

---

# 🔍 Feature 1 — Check Flights

## 📌 Purpose

The **check flights** feature allows users to search for available flights between selected cities.

This feature helps users:
- Verify flight availability
- Explore airline routes
- Identify operating airlines

---

# ✅ Steps to Use

## Step 1 — Open Menu

From the sidebar dropdown select:

```text id="j8f2wa"
check flights""")


if user_option == "check flights":
    st.title('check flights')
    col1,col2=st.columns(2)
    cities=obj.fetch_city_names()
    with col1:
        selected_source=st.selectbox('source',sorted(cities))

    with col2:
        selected_destination=st.selectbox("destination",sorted(cities))
    if st.button("search"):
        
        results=obj.fetch_source_destination(selected_source,selected_destination)
        if len(results)>0:
           st.dataframe(results)
        else: 
            st.title("no flight exists")

        
elif user_option=='analytics':
    airlines,frequency=obj.fetch_ailline_frequency()
    col1,col2=st.columns(2)
    with col1:
        fig = px.pie(names=airlines, values=frequency,   title="frequency of flights")
    

        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',
            legend=dict(
                x=1,
                y=1
            ))
        st.plotly_chart(fig)



    
    with col2:
        data =obj.bussiest_airport()
        df=pd.DataFrame(data,columns=["airport","count"])
        fig = px.bar(df, x='airport', y='count', title='Bussiest airport')
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)

        st.plotly_chart(fig)
      



    col1,col2=st.columns(2)
    df=obj.daily_number_of_flights()
    data1=pd.DataFrame(df,columns=["days","count"])
    with col1:
        
        fig = px.line(
        data1,
        x='days',
        y='count',
        title='flight fly daily',

        markers=True )
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)
        st.plotly_chart(fig)
       
    with col2:
        airline_avg=obj.airlines_avg_price()
        airline_avg_price_df=pd.DataFrame(airline_avg,columns=["airlines","avg_price"])
        fig = px.bar(airline_avg_price_df, x='airlines', y='avg_price', title='airlines and their avg price')
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)

        st.plotly_chart(fig)
       

        
    

    
    
    data3=obj.stop_varies_price()
    price_varies_stop_df=pd.DataFrame(data3,columns=["airline","stops","avg_price"])
    fig = px.bar(
    price_varies_stop_df,
    x='airline',
    y='avg_price',
    color='stops',
    barmode='group',
    title='Average Ticket Price by Airline and Number of Stops'
    )
    fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)

    st.plotly_chart(fig)



    col1,col2=st.columns(2)
    df_flights=obj.monthly_operated_flights()
    with col1:
       fig = px.bar(df_flights, x='month', y='num_flights', title='Highest Number of Flights Operated in June')
       fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)

       st.plotly_chart(fig)
       
    with col2:
        costly_day_df=obj.most_costly_day()
        fig = px.bar(costly_day_df, x='day', y='avg price', title='Most costly day to fly is Thursday',color_discrete_sequence=['gray'])
        fig.update_traces(width=0.6) 
        fig.update_layout(
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',)
        st.plotly_chart(fig)







    

else:
    pass

print(obj.monthly_operated_flights())