# Import python packages
import streamlit as st
import requests
import pandas as pd
from snowflake.snowpark.functions import col

# Title
st.title(":cup_with_straw: Customize Your Smoothie! :cup_with_straw:")

st.write("Choose the fruits you want in your custom Smoothie!")

name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Snowflake Connection
cnx = st.connection("snowflake")
session = cnx.session()

# Fetch data from table - Ensure SEARCH_ON is included (Refer to image_a1947b.png)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))

# Convert the Snowpark Dataframe to a Pandas Dataframe (Refer to image_a191b2.png)
pd_df = my_dataframe.to_pandas()

# Multiselect dropdown
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string = ''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
        # Get the search value from the Pandas Dataframe (Refer to image_a19176.png)
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')

        st.subheader(fruit_chosen + ' Nutrition Information')
        
        # API call using the search_on variable (Refer to image_a19194.png)
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + search_on)
        
        if fruityvice_response.status_code == 200:
            st.dataframe(data=fruityvice_response.json(), use_container_width=True)
        else:
            st.error("The fruit was not found in the nutrition database.")
