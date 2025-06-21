from sentence_transformers import SentenceTransformer
from sklearn.cluster import KMeans
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import os

# Read the data
df = pd.read_csv('eda_data.csv', on_bad_lines='skip')

from transformers import pipeline

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

result = classifier("wrongly coded", candidate_labels=["damaged", "mislabelled", "unknown"])
print(result["labels"][0])  # Output: likely "mislabelled"



# descriptions = df['description'].dropna().unique().tolist()
# model = SentenceTransformer('paraphrase-MiniLM-L12-v2')
# embeddings = model.encode(descriptions)

# kmeans = KMeans(n_clusters=10, random_state=42).fit(embeddings)
# clusters = kmeans.predict(embeddings)

# # Map original descriptions to clusters
# cluster_map = dict(zip(descriptions, clusters))
# df['desc_cluster'] = df['description'].map(cluster_map)


# for cluster_id in range(10):
#     print(f"\n--- Cluster {cluster_id} ---")
#     print(df[df['desc_cluster'] == cluster_id]['description'].value_counts().head(10))



# from sklearn.manifold import TSNE
# import matplotlib.pyplot as plt

# tsne = TSNE(n_components=2, random_state=42)
# embeds_2d = tsne.fit_transform(embeddings)

# plt.figure(figsize=(10, 7))
# sns.scatterplot(x=embeds_2d[:, 0], y=embeds_2d[:, 1], hue=clusters, palette="tab10")
# plt.title("t-SNE Visualization of Description Clusters")
# plt.xlabel("Component 1")
# plt.ylabel("Component 2")
# plt.show()
