# Author: mahalakshmianandh
# Date: 2023-03-31

# Author: mahalakshmianandh
# Date: 2023-03-29

import os
import glob
import numpy as np
import pandas as pd
import pickle
from sklearn.neighbors import NearestNeighbors

import warnings

warnings.filterwarnings("ignore")


def filter_dataset(dataset, **kwargs):
    filtered_dataset = dataset
    for col, val in kwargs.items():
        filtered_dataset = filtered_dataset[filtered_dataset[col] == val]
    return filtered_dataset


def test_function(dataset, **kwargs):
    filtered_dataset = dataset
    for col, val in kwargs.items():
        filtered_dataset = filtered_dataset[filtered_dataset[col] == val]
    knn_data = filtered_dataset[['index','Brand_Name','Product_Name','Types','Price','Size_ml','Rating','Reviews', 'Prize_size_ratio',"Bayesian_Average","Link"]]
    knn_data["Link"] = knn_data["Link"].replace(np.nan, "Not Available")
#     types_list = knn_data.Types.unique()
#     types_list = types_list.tolist()
    types_list = ["Cleaners","Toners","FaceSerum","Eyecare","Moisturizers","Sunscreen","Masks","FacialPeels","Exfoliators","Makeupremovers"]
    output = []
    error_message = "No products for the selected parameters, please change your selections."
    if len(knn_data) == 0:
        return None
    else:
        for t in types_list:
            print(t,"Recommendations\n")
            model_data = knn_data[knn_data['Types'] == t]

            from sklearn.model_selection import train_test_split

            X = model_data.drop(['index','Brand_Name','Product_Name','Types','Price','Size_ml','Rating','Prize_size_ratio','Link'], axis=1)
            y = model_data['index']

            train_X = X
            train_y = y

            if len(X.index) == 0:
                continue
                # return None

            else:
                #train_X, test_X, train_y, test_y = train_test_split(X, y, test_size=0.2, random_state=42)
                if len(X.index) == 1:
                    k = len(X.index)
                elif len(X.index) < 5:
                    k = len(X.index) - 1
                else:
                    k = 5

                knn_model = NearestNeighbors(n_neighbors=k)
                knn_model.fit(train_X)

                product_index = model_data['Bayesian_Average'].idxmax()

                distances, indices = knn_model.kneighbors(train_X.loc[product_index, :].values.reshape(1, -1))

        #         print('Giving Recommendation for', model_data.loc[product_index]['Product_Name'])
                check = []
                for i in range(1, k+1):
                    test = train_y.iloc[indices[0][i-1]]
                    if test in check:
                        continue;
                    else:
                        output.append([t, model_data.loc[model_data['index'] == test].values[0][1],
                                       model_data.loc[model_data['index'] == test].values[0][2],
                                       round(model_data.loc[model_data['index'] == test].values[0][9], 2, ),
                                       model_data.loc[model_data['index'] == test].values[0][10],
                                       "${:.0f}".format(model_data.loc[model_data['index'] == test].values[0][4])
                                       ])
                    check.append(test)
        print("\n\n")
        output = pd.DataFrame(output)

        output.columns = ['Type', 'Brand', 'Product Name', 'Rating', 'Link','Price']
        output = output.reset_index(drop=True)
        return output


if __name__ == '__main__':
    path = r'dataset'
    data_for_model = pd.read_csv(os.path.join(path, r'sephora_cleaned_dataset.csv'))
    #selected_options = {'Vegan': 1, 'Without Sulfates': 1}
    # selected_options = {'Vegan': 1, 'Fragrance Free': 1}
    selected_options = {'Vegan': 1}
    # selected_options = {'Vegan': 1, 'Uneven Texture': 1}
    #selected_options = {'Without Sulfates': 1, 'CrueltyFree':1,'Fragrance Free': 1, 'Oil Free': 1, 'Alcohol Free':1}
    # selected_options = {'Vegan': 1, 'Clean at Sephora': 1}
    # selected_options = {'Vegan': 1, 'Oil Free': 1}
    # selected_options = {'Vegan': 1, 'Normal': 1}
    # selected_options = {'Vegan': 1, 'Combination': 1}
    print(test_function(data_for_model, **selected_options))
