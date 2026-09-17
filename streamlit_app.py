import streamlit as st
from snowflake.snowpark import Session
from snowflake.snowpark.functions import col

name_on_order = st.text_input("Name for smoothie:")

st.title("🥤 Customize Your Smoothie! 🥤")
st.write("Choose the fruits you want in your custom Smoothie!")

cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("SMOOTHIES.PUBLIC.FRUIT_OPTIONS").select(col("FRUIT_NAME"))

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    my_dataframe
)

# st.dataframe(data=my_dataframe, use_container_width=True)

if ingredients_list:

    ingredients_string = ""

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen

    st.write(ingredients_string)

    my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                        values ('""" + ingredients_string + """','""" + name_on_order + """')"""

    st.write(my_insert_stmt)

    time_to_insert = st.button("Submit Order")

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered!', icon="✅")
