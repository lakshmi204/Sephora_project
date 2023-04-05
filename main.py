import streamlit as st
# st.set_option('server.address', '0.0.0.0')

from Knn_model import test_function
import pandas as pd
import os

def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://images.pexels.com/photos/5928039/pexels-photo-5928039.jpeg");
             background-attachment: fill;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )

path=r'dataset'
data_for_model = pd.read_csv(os.path.join(path,r'sephora_cleaned_dataset.csv'))

#test_funct = test_function(data_for_model, Oily=1,Acne = 1)

def main():

    add_bg_from_url()
    #st.markdown("<h1 style='text-align: center; font-family: Arial, sans-serif; font-size: 48px; color: #008080; letter-spacing: 2px; text-shadow: 2px 2px 2px #808080;'>Sephora Skin Care Recommender</h1>", unsafe_allow_html=True)
    st.markdown(
        "<h1 style='text-align: center; font-family: Arial, sans-serif; font-size: 40px; letter-spacing: -1px; text-shadow: 2px 2px 2px; color: black;'>Skin Care Recommender</h1>",
        unsafe_allow_html=True)
    #st.title("Skin Care Recommender")
    # options = ['Without Parabens',
    #            'Without Sulfates',
    #            'Vegan',
    #            'Clean at Sephora',
    #            'CrueltyFree', 'Oil Free',
    #            'Fragrance Free','Alcohol Free', 'Gluten Free', 'Normal', 'Dry', 'Oily', 'Combination',
    #            'Sensitive', 'Dryness', 'Uneven Texture', 'Wrinkles', 'Pores',
    #            'Oiliness', 'Acne', 'Blemishes']

    options1 = ['Dryness', 'Uneven Texture', 'Wrinkles', 'Pores',
               'Oiliness', 'Acne', 'Blemishes']
    options2 = ['Without Parabens',
               'Without Sulfates',
               'Vegan',
               'Clean at Sephora',
               'CrueltyFree', 'Oil Free',
               'Fragrance Free','Alcohol Free', 'Gluten Free']
    options3 =['Normal', 'Dry', 'Oily', 'Combination',
               'Sensitive']



    #selected_options = st.multiselect("**Select Criteria:**", options)
    selected_options3 = st.multiselect("**Select Skin Type**", options3)
    selected_options1 = st.multiselect("**Select Skin Concerns**", options1)
    selected_options2 = st.multiselect("**Select Highlights**", options2)
    #selected_options3 = st.multiselect("**Select Skin Type**", options3)

    #selected_options = {i: 1 for i in selected_options}
    selected_options = {i: 1 for i in selected_options1 + selected_options2 + selected_options3}

    # Button to process input
    if st.button("Submit"):
        if not selected_options:
            st.error('Please select at least one option.')
        else:
            value = test_function(data_for_model, **selected_options)
            if value is None:
                st.warning('No products for the selected parameters, please change your selections.')

            else:

                types = value['Type'].unique()
                for i in types:

                    st.write(f"<h2 style='color:black;'> {i} </h2>", unsafe_allow_html=True)


                    df = value[value['Type'] == i]
                    del df['Type']

                    # convert the URL column to hyperlinks
                    # df['Link'] = df['Link'].apply(lambda url: f'<a href="{url}">Link</a>')
                    df['Product Name'] = df.apply(lambda row: f'<a href="{row["Link"]}" style="color:black">{row["Product Name"]}</a>', axis=1)
                    del df['Link']

                    # apply CSS styling to make the table translucent
                    st.markdown(
                        """
                        <style>
                        .transparent-table {
                            background-color: #fff;
        background-color: rgba(255,255,255,0.5);
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # display the dataframe with hyperlinks and translucent table
                    st.markdown(df.to_html(escape=False, classes='transparent-table',index=False), unsafe_allow_html=True)
                    #df = df.to_html(index=False)

                    # display the dataframe with hyperlinks
                    # st.write(df.to_html(escape=False), unsafe_allow_html=True)
                    #
                    # # Convert the DataFrame to an HTML table without the index column
                    #html_table = df.to_html(index=False)
                    #
                    # # Add custom CSS for a translucent table
                    # # apply CSS styling to make the table transparent
                    # st.markdown(
                    #     f"""
                    #     <style>
                    #         .transparent {{
                    #             background-color: transparent !important;
                    #         }}
                    #     </style>
                    #     """,
                    #     unsafe_allow_html=True
                    # )
                    #
                    #
                    #
                    # # display the HTML table
                    # st.markdown(html_table, unsafe_allow_html=True)
                    #
                    # # Wrap the table in a div with a custom class
                    # #translucent_table = f'<table id="Main table" style="background-color:#FFFF0080;">{html_table}</table>'
                    #
                    # # Display the translucent HTML table in Streamlit
                    # #st.write(translucent_table, unsafe_allow_html=True)

                    st.write('\n')
                    st.write('\n')
                    st.write('\n')
            # st.table(value)


if __name__ == "__main__":
    main()