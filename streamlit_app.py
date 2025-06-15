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

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'), col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df = my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop()


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

if ingredients_list:
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        search_on = pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        #st.write('The search value for ', fruit_chosen, ' is ', search_on, '.')
        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + search_on)
        fv_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
