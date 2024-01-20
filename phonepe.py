import os
import pandas as pd
import json
import psycopg2 
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image
from git.repo.base import Repo


# Setting up page configuration

icon = Image.open("Phonepe.png")
st.set_page_config(page_title= "Phonepe Pulse Data Visualization",
                   page_icon="🧊",
                   layout= "wide",
                   initial_sidebar_state= "expanded",
                   menu_items={
                       'Get Help': 'https://www.phonepe.com/pulse/explore/transaction/2022/4/',
                       'About': """Data has been cloned from Phonepe Pulse Github Repo"""})

#SQL connection

mydb=psycopg2.connect(host="localhost",
                        user="postgres",
                        password="priya1",
                        database="phonepe_pulse",
                        port="5432")
mycursor=mydb.cursor()

# Creating option menu in the side bar

with st.sidebar:
    selected = option_menu("Menu", ["Home","Top Charts","Explore Data","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})
    
# MENU 1 - HOME
    
if selected == "Home":
    st.image("dow.jpg")
    st.markdown("# :white[Lets Explore and Visualize Phonepe Data:mag:]")
    st.markdown("## :green[ Over Streamlit and Plotly]")
    col1,col2 = st.columns([3,2],gap="medium")
    with col1:
        st.write(" ")
        st.markdown("### :violet[Overview :] This project delivers a live geo visualization dashboard for Phonepe Pulse GitHub data, featuring 10+ dropdown options. Users can access and analyze the dynamically updated information stored in a MySQL database for informed decision-making.")
    with col2:
        st.image("Anz.jpg")

# MENU 2 - TOP CHARTS

if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    Type = st.sidebar.selectbox("**Type**", ("Insurance", "Transaction", "User"))
    colum1, colum2 = st.columns([1, 1.5], gap="large")
    
    with colum1:
        Year = st.slider("**Year**", min_value=2018, max_value=2023)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)

    with colum2:
        st.info(
            """
            #### From this menu we can get insights like :
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transactions and Total amount spent on Phonepe.
            - Top 10 State, District, Pincode based on Total Phonepe users and their app opening frequency.
            - Top 10 mobile brands and their percentage based on how many people use Phonepe.
            """, icon="🔍"
        )
        
# Top Charts - Insurance 
           
    if Type == "Insurance":
        col1,col2,col3 = st.columns([1,1,1],gap="small")
        
        with col1:
            st.markdown("### :violet[State]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_Insurance where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_Insurance where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_Insurance where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

# Top charts - Transaction
            
    if Type == "Transaction":
        col1, col2, col3 = st.columns([1, 1, 1], gap="small")

        with col1:
            st.markdown("### :violet[State]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from agg_Transaction where year = {Year} and quarter = {Quarter} group by state order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col2:
            st.markdown("### :violet[District]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
            else:
                mycursor.execute(f"select district , sum(Count) as Total_Count, sum(Amount) as Total from map_Transaction where year = {Year} and quarter = {Quarter} group by district order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Transactions_Count','Total_Amount'])

                fig = px.pie(df, values='Total_Amount',
                                names='District',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col3:
            st.markdown("### :violet[Pincode]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
            else:
                mycursor.execute(f"select pincode, sum(Transaction_count) as Total_Transactions_Count, sum(Transaction_amount) as Total from top_Transaction where year = {Year} and quarter = {Quarter} group by pincode order by Total desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Transactions_Count','Total_Amount'])
                fig = px.pie(df, values='Total_Amount',
                                names='Pincode',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Transactions_Count'],
                                labels={'Transactions_Count':'Transactions_Count'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

#Top chart User
            
    if Type == "User":
        col1,col2,col3,col4 = st.columns([2,2,2,2],gap="small")
        
        with col1:
            st.markdown("### :violet[Brand]")
            if Year == 2022 and Quarter in [2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [1,2,3,4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select brand, sum(count) as Total_Count, avg(percentage)*100 as Avg_Percentage from agg_user where year = {Year} and quarter = {Quarter} group by brand order by Total_Count desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Brand', 'Total_Users','Avg_Percentage'])
                fig = px.bar(df,
                             title='Top 10',
                             x="Total_Users",
                             y="Brand",
                             orientation='h',
                             color='Avg_Percentage',
                             color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)   
    
        with col2:
            st.markdown("### :violet[District]")
            if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select district, sum(Registered_User) as Total_Users, sum(app_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by district order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['District', 'Total_Users','Total_Appopens'])
                df.Total_Users = df.Total_Users.astype(float)
                fig = px.bar(df,
                            title='Top 10',
                            x="Total_Users",
                            y="District",
                            orientation='h',
                            color='Total_Users',
                            color_continuous_scale=px.colors.sequential.Agsunset)
                st.plotly_chart(fig,use_container_width=True)
              
        with col3:
            st.markdown("### :violet[Pincode]")
            if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select Pincode, sum(Registered_Users) as Total_Users from top_user where year = {Year} and quarter = {Quarter} group by Pincode order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['Pincode', 'Total_Users'])
                fig = px.pie(df,
                            values='Total_Users',
                            names='Pincode',
                            title='Top 10',
                            color_discrete_sequence=px.colors.sequential.Agsunset,
                            hover_data=['Total_Users'])
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)
            
        with col4:
            st.markdown("### :violet[State]")
            if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by Total_Users desc limit 10")
                df = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
                fig = px.pie(df, values='Total_Users',
                                names='State',
                                title='Top 10',
                                color_discrete_sequence=px.colors.sequential.Agsunset,
                                hover_data=['Total_Appopens'],
                                labels={'Total_Appopens':'Total_Appopens'})

                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig,use_container_width=True)

# MENU 3 - EXPLORE DATA

if selected == "Explore Data":
    Year = st.sidebar.slider ("**Year**", min_value=2018, max_value=2023)
    Quarter = st.sidebar.slider ("Quarter", min_value=1, max_value=4)
    Type = st.sidebar.selectbox ("**Type**", ("Insurance","Transactions", "Users"))
    col1,col2 = st.columns(2)

# EXPLORE DATA - Insurance
    if Type == "Insurance":
        
# Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.State = df2
                                            
                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_amount',
                        color_continuous_scale='Reds')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
# Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2019 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
            elif Year == 2020 and Quarter in [1]:
                st.markdown("#### No Data")
            elif Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(int)
                df1.State = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transactions',
                        color_continuous_scale='Reds')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
                        
# BAR CHART - TOP PAYMENT TYPE
            
        st.markdown("## :violet[Top Payment Type]")
        if Year == 2018 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2019 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2020 and Quarter in [1]:
            st.markdown("#### No Data")
        elif Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
        else:
            mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_insurance where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                        title='Transaction Types vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        if Year == 2018 and Quarter in [1,2,3,4]:
                st.markdown("#### No Data")
        elif Year == 2019 and Quarter in [1,2,3,4]:
            st.markdown("#### No Data")
        elif Year == 2020 and Quarter in [1]:
            st.markdown("#### No Data")
        elif Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
        else:
         
            mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_insurance where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig,use_container_width=True)

# EXPLORE DATA - TRANSACTIONS
    if Type == "Transactions":
        
# Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP 
        with col1:
            st.markdown("## :violet[Overall State Data - Transactions Amount]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.State = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_amount',
                        color_continuous_scale='sunset')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
# Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        with col2:
            
            st.markdown("## :violet[Overall State Data - Transactions Count]")
            if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
            else:
                mycursor.execute(f"select state, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} group by state order by state")
                df1 = pd.DataFrame(mycursor.fetchall(),columns= ['State', 'Total_Transactions', 'Total_amount'])
                df2 = pd.read_csv('Statenames.csv')
                df1.Total_Transactions = df1.Total_Transactions.astype(int)
                df1.State = df2

                fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                        featureidkey='properties.ST_NM',
                        locations='State',
                        color='Total_Transactions',
                        color_continuous_scale='sunset')

                fig.update_geos(fitbounds="locations", visible=False)
                st.plotly_chart(fig,use_container_width=True)
            
            
            
# BAR CHART - TOP PAYMENT TYPE
        st.markdown("## :violet[Top Payment Type]")
        if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
        else:
            mycursor.execute(f"select Transaction_type, sum(Transaction_count) as Total_Transactions, sum(Transaction_amount) as Total_amount from agg_transaction where year= {Year} and quarter = {Quarter} group by transaction_type order by Transaction_type")
            df = pd.DataFrame(mycursor.fetchall(), columns=['Transaction_type', 'Total_Transactions','Total_amount'])

            fig = px.bar(df,
                        title='Transaction Types vs Total_Transactions',
                        x="Transaction_type",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Cividis)
            st.plotly_chart(fig,use_container_width=False)
        
# BAR CHART TRANSACTIONS - DISTRICT WISE DATA            
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("# ")
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        if Year == 2023 and Quarter in [4]:
                st.markdown("#### No Data")
        else:
         
            mycursor.execute(f"select State, District,year,quarter, sum(count) as Total_Transactions, sum(amount) as Total_amount from map_transaction where year = {Year} and quarter = {Quarter} and State = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State','District','Year','Quarter',
                                                            'Total_Transactions','Total_amount'])
            fig = px.bar(df1,
                        title=selected_state,
                        x="District",
                        y="Total_Transactions",
                        orientation='v',
                        color='Total_amount',
                        color_continuous_scale=px.colors.sequential.Magma)
            st.plotly_chart(fig,use_container_width=True)
    
# EXPLORE DATA - USERS      
    if Type == "Users":
        
# Overall State Data - TOTAL APPOPENS - INDIA MAP
        st.markdown("## :violet[Overall State Data - User App opening frequency]")
        if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
        else:
            mycursor.execute(f"select state, sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} group by state order by state")
            df1 = pd.DataFrame(mycursor.fetchall(), columns=['State', 'Total_Users','Total_Appopens'])
            df2 = pd.read_csv('Statenames.csv')
            df1.Total_Appopens = df1.Total_Appopens.astype(float)
            df1.State = df2
            
            fig = px.choropleth(df1,geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='State',
                    color='Total_Appopens',
                    color_continuous_scale='Viridis')

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True)
            
# BAR CHART TOTAL UERS - DISTRICT WISE DATA 
        st.markdown("## :violet[Select any State to explore more]")
        selected_state = st.selectbox("",
                             ('andaman-&-nicobar-islands','andhra-pradesh','arunachal-pradesh','assam','bihar',
                              'chandigarh','chhattisgarh','dadra-&-nagar-haveli-&-daman-&-diu','delhi','goa','gujarat','haryana',
                              'himachal-pradesh','jammu-&-kashmir','jharkhand','karnataka','kerala','ladakh','lakshadweep',
                              'madhya-pradesh','maharashtra','manipur','meghalaya','mizoram',
                              'nagaland','odisha','puducherry','punjab','rajasthan','sikkim',
                              'tamil-nadu','telangana','tripura','uttar-pradesh','uttarakhand','west-bengal'),index=30)
        
        if Year == 2023 and Quarter in [4]:
                    st.markdown("#### No Data")
        else:
        
            mycursor.execute(f"select State,year,quarter,District,sum(Registered_user) as Total_Users, sum(App_opens) as Total_Appopens from map_user where year = {Year} and quarter = {Quarter} and state = '{selected_state}' group by State, District,year,quarter order by state,district")
            
            df = pd.DataFrame(mycursor.fetchall(), columns=['State','year', 'quarter', 'District', 'Total_Users','Total_Appopens'])
            df.Total_Users = df.Total_Users.astype(int)
            
            fig = px.bar(df,
                        title=selected_state,
                        x="District",
                        y="Total_Users",
                        orientation='v',
                        color='Total_Users',
                        color_continuous_scale=px.colors.sequential.Inferno)
            st.plotly_chart(fig,use_container_width=True)

# MENU 4 - ABOUT
if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### PhonePe Pulse offers real-time insights and visualizations, leveraging GitHub data for dynamic analytics within the PhonePe ecosystem. With customizable views and interactive dashboards, it provides a powerful and user-friendly solution for extracting, transforming, and visualizing data, enhancing decision-making capabilities.")
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is a leading digital payments platform in India, offering a range of services from mobile recharges to bill payments. Acquired by Flipkart in 2016, PhonePe is known for its user-friendly app and secure Unified Payments Interface (UPI) transactions, making it a widely used financial tool in the country.")
        
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.image("dow.jpg")