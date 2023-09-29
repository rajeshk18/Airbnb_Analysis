import pandas as pd
import pymongo
import streamlit as st
import plotly.express as px
from streamlit_option_menu import option_menu
from PIL import Image

# Setting up page configuration
icon = Image.open("airbnb.png")
st.set_page_config(page_title="Airbnb Data Visualization | By Rajesh Kanna A",
                   page_icon=icon,
                   layout="wide",
                   initial_sidebar_state="expanded",
                   menu_items={'About': """# This dashboard app is created by *Rajesh Kanna A*!
                                        Data read from mongodb atlas"""}
                   )

# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home", "Overview", "Explore"],
                           icons=["house", "graph-up-arrow", "bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#FF5A5F"}}
                           )

# CREATING CONNECTION WITH MONGODB ATLAS AND RETRIEVING THE DATA
client = pymongo.MongoClient(
    f"mongodb+srv://arajeshkanna82:Fk6J7mlSqHtKgJkH@cluster0.bpgxdos.mongodb.net/?retryWrites=true&w=majority")
db = client.airbnb
col = db.ny19


# READING THE CLEANED DATAFRAME
df = pd.read_csv('Airbnb_data.csv')
col1, col2 = st.columns([0.13, 0.87], gap='small')
col1.image("ICN.png", width=150)
col2.title(":red[Welcome to AirBnB Dashboard]")

# HOME PAGE
if selected == "Home":
    # Title Image

    st.markdown("## :blue[Domain] : Travel Industry, Property Management and Tourism")
    st.markdown("## :blue[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
    st.markdown(
        "## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, "
        "develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, "
        "availability patterns, and location-based trends. ")

# OVERVIEW PAGE
if selected == "Overview":

    selected_tab = option_menu(None, ["Raw Data", "Insights"],

                               default_index=0,
                               orientation="horizontal",
                               styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px",
                                                    "--hover-color": "#FF5A5F"},
                                       "nav-link-selected": {"background-color": "#FF5A5F"}})

                               # styles={"nav-link": {"font-size": "30px", "text-align": "centre", "margin": "0px",
                               #                      "--hover-color": "#6495ED"},
                               #         "icon": {"font-size": "30px"},
                               #         "container": {"max-width": "6000px"},
                               #         "nav-link-selected": {"background-color": "#6495ED"}})
    #
    # # RAW DATA TAB
    if selected_tab == "Raw Data":
        #     # RAW DATA
        if st.button("Click to view Raw data"):
            st.write(col.find_one())
        if st.button("Click to view Dataframe"):
            st.write(col.find_one())
            st.write(df)

    if selected_tab == "Insights":
        # INSIGHTS TAB
        # if st.button("click to view data insights"):
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
        prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()),
                                      sorted(df.Property_type.unique()))
        room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
        price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')

        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["Property_type"]).size().reset_index(name="Listings").sort_values(
                by='Listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='Listings',
                         y='Property_type',
                         orientation='h',
                         color='Property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["Host_name"]).size().reset_index(name="Listings").sort_values(by='Listings',
                                                                                                         ascending=False)[
                  :10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='Listings',
                         y='Host_name',
                         orientation='h',
                         color='Host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["Room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='Room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['Country'], as_index=False)['Name'].count().rename(
                columns={'Name': 'Total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='Country',
                                locationmode='country names',
                                color='Total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)

# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")

    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a Country', sorted(df.Country.unique()), sorted(df.Country.unique()))
    prop = st.sidebar.multiselect('Select Property_type', sorted(df.Property_type.unique()),
                                  sorted(df.Property_type.unique()))
    room = st.sidebar.multiselect('Select Room_type', sorted(df.Room_type.unique()), sorted(df.Room_type.unique()))
    price = st.slider('Select Price', df.Price.min(), df.Price.max(), (df.Price.min(), df.Price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'Country in {country} & Room_type in {room} & Property_type in {prop} & Price >= {price[0]} & Price <= {price[1]}'

    # HEADING 1
    st.markdown("## :red[Price Analysis]")

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')

    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('Room_type', as_index=False)['Price'].mean().sort_values(by='Price')
        fig = px.bar(data_frame=pr_df,
                     x='Room_type',
                     y='Price',
                     color='Price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        # HEADING 2
        st.markdown("## :red[Availability Analysis]")

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='Room_type',
                     y='Availability_365',
                     color='Room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country', as_index=False)['Price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Price',
                             hover_data=['Price'],
                             locationmode='country names',
                             size='Price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('Country', as_index=False)['Availability_365'].mean()
        country_df.Availability_365 = country_df.Availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='Country',
                             color='Availability_365',
                             hover_data=['Availability_365'],
                             locationmode='country names',
                             size='Availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)
