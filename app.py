import streamlit as st 
from db_helper import DB
import plotly.express as px
import pandas as pd
obj=DB()
st.sidebar.title("flight analytics")
user_option =st.sidebar.selectbox('menu',['select one','check flights','analytics'])


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

        st.plotly_chart(fig)


    
    with col2:
        data =obj.bussiest_airport()
        df=pd.DataFrame(data,columns=["airport","count"])
        fig = px.bar(df, x='airport', y='count', title='Bussiest airport')
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
        st.plotly_chart(fig)
    with col2:
        airline_avg=obj.airlines_avg_price()
        airline_avg_price_df=pd.DataFrame(airline_avg,columns=["airlines","avg_price"])
        fig = px.bar(airline_avg_price_df, x='airlines', y='avg_price', title='airlines and their avg price')
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

    st.plotly_chart(fig)



    col1,col2=st.columns(2)
    df_flights=obj.monthly_operated_flights()
    with col1:
       fig = px.bar(df_flights, x='month', y='num_flights', title='Highest Number of Flights Operated in June')
       st.plotly_chart(fig)

    with col2:
        costly_day_df=obj.most_costly_day()
        fig = px.bar(costly_day_df, x='day', y='avg price', title='Most costly day to fly is Thursday',color_discrete_sequence=['gray'])
        fig.update_traces(width=0.6) 
        st.plotly_chart(fig)







    

else:
    pass

print(obj.monthly_operated_flights())