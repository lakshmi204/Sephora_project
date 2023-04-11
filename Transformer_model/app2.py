# Author: mahalakshmianandh
# Date: 2023-03-25

import streamlit as st
# st.set_option('server.address', '0.0.0.0')

from transformer_model import ProductEmbedding


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/4465124/pexels-photo-4465124.jpeg?auto=compress&cs=tinysrgb&w=1260&h=750&dpr=1");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


product_embedding = ProductEmbedding(

    model_name="bert-base-uncased",
    collection_name="sephora_collections",
    embedding_size=768,
    recreate_collection=False,
    row_name="Skincare Concern Keyword",
    dropna=True,
    payloads=['Product Name'],
    limit=5)


def main():
    # set_background_image("/Users/mahalakshmianandh/Data 608/webpage/backgr.jpg")
    add_bg_from_url()
    st.title("Skin care recommender")

    options = ['liquid',
               'redness',
               'fine',
               'rich',
               'lush',
               'firmness',
               'melon',
               'uneven',
               'lotion',
               'blemishes',
               'skintone',
               'heavy',
               'spf',
               'spots',
               'sun',
               'fines',
               'hyperpigmentation',
               'inspired',
               'gel',
               'mask',
               'wrinkles',
               'spot',
               'tropical',
               'wipes',
               'creamgel',
               'serum',
               'balm',
               'full',
               'clean',
               'fresh',
               'formulation',
               'cream',
               'sheet',
               'loss',
               'texture',
               'spray',
               'elasticity',
               'acne',
               'winkles',
               'dark',
               'oiliness',
               'dryness',
               'desert',
               'flowers',
               'protection',
               'tone',
               'puffiness',
               'dullness',
               'wipe',
               'scent',
               'oil',
               'fruits',
               'scrub',
               'skin',
               'circles',
               'dulness',
               'powder',
               'pores',
               'lightweight',
               'lines',
               'foam']

    selected_options = st.multiselect('Select skincare concern keywords::', options)
    selected_values = []

    # Add the selected options to the list of selected values
    for option in selected_options:
        if option not in selected_values:
            selected_values.append(option)

    options = ["Vegan and Non Vegan", "Vegan", "Non Vegan"]
    choice = st.selectbox("Select an option", options)

    # Display an error message if no options have been selected
    if not selected_values:
        st.error('Please select at least one option.')


    # Text input field
    # user_input = st.text_input("Enter skincare concern keywords:")

    value = product_embedding.search(",".join(selected_values), query_filter=choice)
    # Button to process input
    if st.button("Submit"):
        # st.write(f"Selected option: {selected_option}")
        # st.write(f"Product Name: {value}")
        st.write(f"Product Names: {value}")

        # st.write("List of items:")
        # st.write(get_items(selected_option, user_input))


if __name__ == "__main__":
    main()
