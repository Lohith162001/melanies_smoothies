# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Title and Instructions
st.title(f":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write("""Choose the fruits you want in your custom Smoothie!""")

# Get name for the smoothie
name_on_order = st.text_input('Name on Smoothie:')
st.write('The name on your Smoothie will be:', name_on_order)

# Get session and fruit options
cnx = st.connection("snowflake", type="snowflake")
session = cnx.session()  
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))

# Let user pick fruits
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
)

# Only show button if there's a smoothie name and ingredients
if name_on_order and ingredients_list:
    ingredients_string = ' '.join(ingredients_list)  # Cleaner than using a loop

    if st.button('Submit Order'):
        # Build and run the INSERT statement
        insert_stmt = f"""
        insert into smoothies.public.orders(ingredients, name_on_order)
        values ('{ingredients_string}', '{name_on_order}')
        """
        session.sql(insert_stmt).collect()
        st.success(f'✅ Your Smoothie is ordered, {name_on_order}!')

import requests
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")
st.text(smoothiefroot_response)

