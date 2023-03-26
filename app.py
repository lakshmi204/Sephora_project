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
             background-image: url("https://img.freepik.com/free-photo/macadamia-body-lotion-skin-cream_1150-42810.jpg?w=2000&t=st=1679455710~exp=1679456310~hmac=7c9409da933ec8b4d789b06b46ba0c169bec5fb08d81183a97f8099d57ae5d7c");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
         unsafe_allow_html=True
     )
product_embedding =  ProductEmbedding(

    model_name="bert-base-uncased",
    collection_name="sephora_collections",
    embedding_size=768,
    recreate_collection=False,
    row_name="Skincare Concern Keyword",
    dropna=True,
    payloads = ['Product Name'],
    limit=5)

def main():
    # set_background_image("/Users/mahalakshmianandh/Data 608/webpage/backgr.jpg")
    add_bg_from_url()
    st.title("Skin care recommender")

    # Dropdown menu
    # options = ["Moisturizer", "Eyecare", "Sunscreen"]
    # selected_option = st.selectbox("Product Type:", options)
    #
    # # Dropdown menu
    # options = ["Dry", "Oily", "Combination"]
    # selected_option = st.selectbox("Skin Type:", options)
    #
    # # Dropdown menu
    # options = ["Dryness", "Dullness", "Wrinkles"]
    # selected_option = st.selectbox("Skin Care Concern:", options)

    # Text input field
    user_input = st.text_input("Enter skincare concern keywords:")


    value = product_embedding.search(user_input)
    # Button to process input
    if st.button("Submit"):
        # st.write(f"Selected option: {selected_option}")
        st.write(f"Product Name: {value}")
        # st.write("List of items:")
        #st.write(get_items(selected_option, user_input))


if __name__ == "__main__":
    main()