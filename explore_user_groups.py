import os
import pandas as pd
import functions as fu
import settings as se
import numpy as np
from sklearn.cluster import AgglomerativeClustering
from scipy.cluster.hierarchy import dendrogram, linkage
import matplotlib.pyplot as plt


# Text-embedding-based clustering for LLM-summarizing:
# https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
def generate_embedding(_key_data):
    output_file_name = f"embedding_{se.file_name}"

    # check if the text embedding already exists
    if os.path.exists(f"llm_summarizing/exploration/{output_file_name}"):
        print(f"\nFile {output_file_name} already exists. Skipping embedding generation.\n")
        return

    # read the user data from csv
    data = pd.read_csv(f"data/{se.file_name}", delimiter=";")

    # select the specific user data
    user_data = data[_key_data].copy()

    # combine all columns into a single column for creating text embedding
    user_data["combined"] = user_data.apply(lambda row: '. '.join(row.values.astype(str)), axis=1)

    # generate text embedding per combined user data and store it to a new column.
    print("\n### Generating text embeddings. Please wait ... ###\n")
    user_data["embedding"] = user_data["combined"].apply(fu.text_embedding)

    # save the result
    user_data.to_csv(f"llm_summarizing/exploration/{output_file_name}", index=False)
    print("\n### Done. Text embedding generated ###\n")


def hierarchy_clustering(_num_cluster):
    input_file_name = f"embedding_{se.file_name}"
    output_file_name = f"clustering_{_num_cluster}_{se.file_name}"

    # check if the text embedding already exists
    if os.path.exists(f"llm_summarizing/exploration/{output_file_name}"):
        print(f"\nFile {output_file_name} already exists. Skipping embedding generation.\n")
        return

    # Load the dataframe
    df = pd.read_csv(f"llm_summarizing/exploration/{input_file_name}")

    # convert string to numpy array
    embeddings = np.vstack(df["embedding"].apply(eval).apply(np.array).values)

    # Normalize the embeddings to unit length
    embeddings = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)

    # Perform hierarchical clustering
    clustering_model = AgglomerativeClustering(n_clusters=_num_cluster, linkage='ward')
    clustering_model.fit(embeddings)
    cluster_assignment = clustering_model.labels_

    # Store the cluster result as csv file
    df["cluster"] = cluster_assignment
    df.to_csv(f"llm_summarizing/exploration/{output_file_name}", index=False)

    # create a new dataset with cluster result
    user_data = pd.read_csv(f"data/{se.file_name}", delimiter=";")
    user_data["user_group"] = cluster_assignment
    user_data.to_csv(f"llm_summarizing/exploration/grouped_{se.file_name}", index=False)
    print("\n### Done. Grouped user data. ###\n")


def plot_dendrogram(_num_cluster):
    # Load the dataframe
    input_file_name = f"clustering_{_num_cluster}_{se.file_name}"
    df = pd.read_csv(f"llm_summarizing/exploration/{input_file_name}")

    # convert string to numpy array
    embeddings = np.vstack(df["embedding"].apply(eval).apply(np.array).values)
    cluster_assignment = df["cluster"].values

    # perform hierarchical linkage for the dendrogram
    linked = linkage(embeddings, 'ward')

    # compute the threshold for the given number of clusters
    num_samples = len(embeddings)
    threshold_index = num_samples - _num_cluster
    max_distance = linked[threshold_index, 2]

    # Plot the dendrogram
    plt.figure(figsize=(10, 7))
    dendrogram(linked, orientation='top', distance_sort='descending', show_leaf_counts=True, color_threshold=max_distance)

    # Show the graph
    plt.xlabel('User responses')
    plt.ylabel('Distances')
    plt.title(f'Hierarchical Clustering with {num_group} user groups.')
    plt.show()

    plt.savefig(f"llm_summarizing/exploration/dendrogram_group_size_{_num_cluster}.pdf", bbox_inches="tight")


def summarize(_num_groups):
    # Prepare user data
    user_data = pd.read_csv(f"llm_summarizing/exploration/grouped_{se.file_name}")

    # Generate a summarize per grouped user data
    for group_num in range(_num_groups):
        print(f"\n### Generating a summary of user group {group_num + 1}/{_num_groups} ... ###\n")

        # prepare user data per group
        grouped_data = user_data[user_data["user_group"] == group_num]
        grouped_data = grouped_data.drop(columns=["user_group"])
        grouped_data_list = grouped_data.values.tolist()

        prompt = [
            {
                "role": "user",
                "content": f"Here is a group of user data:\n{grouped_data_list}\n\n"
                           f"Write a one-paragraph summarize of archetypal characteristics of the user group.\n"
            }
        ]

        # get input
        input_prompt = prompt[0]["content"]

        # compute output
        output = fu.chat_completion(prompt)

        # Display output
        print("\n### Output ###\n")
        print(output, "\n")

        # save output
        with open(f"llm_summarizing/exploration/user_group_{group_num}.txt", "w") as text_file:
            text_file.write(output)

    print(f"\n### Done. Summarized user groups. ###\n")


if __name__ == "__main__":
    # The name of user data that contains key characteristics for creating user groups.
    # (i.e., the column names from "synthetic_responses.csv")
    key_data = ["child_expect", "child_need"]

    # The number of user groups to create.
    num_group = 3

    # Create user groups
    generate_embedding(key_data)
    hierarchy_clustering(num_group)

    # Summarize each user group
    summarize(num_group)

    # Hierarchy clustering visualization
    plot_dendrogram(num_group)
