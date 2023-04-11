# Author: mahalakshmianandh
# Date: 2023-03-25
import os

from transformers import AutoTokenizer, AutoModel
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import pandas as pd
import tqdm


class ProductEmbedding:
    def __init__(self, file_name=None, model_name=None, collection_name=None, embedding_size=None,
                 recreate_collection=None, limit=None, row_name=None,
                 dropna=None, payloads=None):
        """

        :param file_name:
        :param model_name:
        :param collection_name:
        :param embedding_size:
        :param recreate_collection:
        :param limit:
        :param row_name:
        :param dropna:
        :param payloads:
        """
        if not os.path.exists('./model'):
            os.makedirs('./model')
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, cache_dir='./model')
        self.model = AutoModel.from_pretrained(model_name, cache_dir='./model')
        self.file_name = file_name
        self.data = None
        self.client = QdrantClient(host="192.168.1.70", port=6333)
        self.collection_name = collection_name
        self.limit = limit
        self.row_name = row_name
        self.dropna = dropna
        self.payloads = payloads
        if recreate_collection:
            self.client.recreate_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=embedding_size, distance=Distance.COSINE),
            )

    def get_embedding(self, text):
        input_ids = self.tokenizer.encode(text, return_tensors='pt')
        embeddings = self.model(input_ids)[0].tolist()[0][0]
        return embeddings

    def insert_data(self):
        if self.data is None:
            self.read_data()
        if self.dropna:
            self.data = self.data[self.data[self.row_name].notna()]
        for idx, row in tqdm.tqdm(self.data.iterrows()):
            embedding = self.get_embedding(row[self.row_name])
            payloads = {}
            for i in self.payloads:
                value = row[i]
                if isinstance(value, str) and '.csv' in value:
                    value = value.split('_')[0]
                payloads[f'{i}'] = value
            self.client.upsert(collection_name=self.collection_name, points=[PointStruct(id=idx + 1,
                                                                                         vector=embedding,
                                                                                         payload=payloads
                                                                                         )])

    def search(self, text, query_filter):
        if query_filter == 'Non Vegan':
            filter_value = 0
            hits = self.client.search(
                query_vector=self.get_embedding(text),
                collection_name=self.collection_name,
                query_filter=Filter(
                    should=[
                        FieldCondition(key="vegan", match=MatchValue(value=filter_value)),
                    ]
                ),
                append_payload=True,
                limit=self.limit
            )
        elif query_filter == 'Vegan':
            filter_value = 1
            hits = self.client.search(
                query_vector=self.get_embedding(text),
                collection_name=self.collection_name,
                query_filter=Filter(
                    should=[
                        FieldCondition(key="vegan", match=MatchValue(value=filter_value)),
                    ]
                ),
                append_payload=True,
                limit=self.limit
            )

        else:
            filter_value = 2
            hits = self.client.search(
                query_vector=self.get_embedding(text),
                collection_name=self.collection_name,
                append_payload=True,
                limit=self.limit
            )


        return [h.payload['Product Name'] for h in hits]

    def read_data(self):
        """

        :return:
        """
        self.data = pd.read_csv(self.file_name, sep='\t')


if __name__ == '__main__':
    search = False
    product_embedding = ProductEmbedding(
        # file_name=["dataset/sephora_cleaned_dataset_updated.csv", "dataset/sephora_cleaned_dataset.csv", "Brand_Name"],
        file_name="dataset/sephora_cleaned_dataset_updated.csv",
        model_name="bert-base-uncased",
        collection_name="sephora_collections",
        embedding_size=768,
        recreate_collection=True if not search else False,
        row_name="Skincare Concern Keyw ord",
        dropna=True,
        payloads=['Product Name', 'vegan', 'Types'],
        limit=5)
    if search:
        print(product_embedding.search(text="fine,lines,wrinkles,dryness,loss,firmness,elasticity", query_filter='Non Vegan'))
    else:
        product_embedding.insert_data()
