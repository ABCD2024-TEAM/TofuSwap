import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
import itertools
import numpy as np
from matplotlib import font_manager
from Features.importDataset import getDataset
import os

from matplotlib import font_manager
my_font = font_manager.FontProperties(fname=os.path.join(os.path.dirname(os.path.abspath(__file__)), "../fonts/simhei.ttf"))

def visualize_network():
    df = getDataset()
    # Create a list of all ingredients
    all_ingredients = []

    for i in range(1, 7):
        col = f'材料{i}'
        all_ingredients.extend(df[col].tolist())


    all_ingredients = [item for item in all_ingredients if item != '' and not pd.isna(item)] #remove empty strings and nan dont know where nan come from

    unique_ingredients = list(set(all_ingredients)) #find how many unique ingredients for node


    # Create a co-occurrence matrix
    ingredient_pairs = defaultdict(int)

    # For each dish, count co-occurrences of ingredients
    for _, row in df.iterrows():
        # Get all non-empty ingredients for this dish
        dish_ingredients = []
        for i in range(1, 7):
            col_name = f'材料{i}'
            if col_name in df.columns:
                ing = row[col_name]
                if pd.notna(ing) and ing != '':
                    dish_ingredients.append(ing)
        
        # Count co-occurrences for all pairs in this dish
        for pair in itertools.combinations(dish_ingredients, 2):
            # Sort to ensure (A,B) is same as (B,A)
            sorted_pair = tuple(sorted(pair))
            ingredient_pairs[sorted_pair] += 1

    # Create a graph
    G = nx.Graph()

    plt.rcParams['font.family'] = ["SimHei"]
    plt.rcParams['axes.unicode_minus'] = False #title chinese font

    # Add nodes (ingredients)
    for ingredient in unique_ingredients:
        G.add_node(ingredient)

    # Add edges (co-occurrences)
    for pair, weight in ingredient_pairs.items():
        if weight >= 1:  # AI said to use >=2 but we can use >=1 to show all connections
            G.add_edge(pair[0], pair[1], weight=weight)

    # Calculate node degrees for sizing
    node_degrees = dict(G.degree())


    fig = plt.Figure(figsize=(16, 12))
    ax = fig.add_subplot(111)
    fig.patch.set_facecolor('#f7f2e7')
    pos = nx.spring_layout(G, k=1, iterations=50)

    # Draw the network
    nx.draw_networkx_nodes(G, pos, 
                        node_size=[v * 100 for v in node_degrees.values()],
                        node_color='lightblue',
                        alpha=0.7,
                        ax = ax
                        )

    nx.draw_networkx_edges(G, pos, 
                        edge_color='gray',
                        alpha=0.4,
                        width=[G[u][v]['weight']/5 for u, v in G.edges()],
                        ax = ax)

    nx.draw_networkx_labels(G, pos, 
                            font_size=12,
                            font_family=["SimHei"],
                            ax = ax)  # Use a font that supports Chinese characters

    ax.set_title('各項材料的親密程度 Closeness of each ingredient', fontsize=20)
    ax.axis('off')
    fig.tight_layout()
    return fig

# print(f"Total unique ingredients: {len(unique_ingredients)}") #check error should be 102

# # Get the top ingredient pairs by co-occurrence
# sorted_pairs = sorted(ingredient_pairs.items(), key=lambda x: x[1], reverse=True)

# print("\nTop ingredient pairs by co-occurrence:")
# for i, (pair, count) in enumerate(sorted_pairs[:20]):
#     print(f"{i+1}. {pair[0]} - {pair[1]}: {count} dishes")

# # Calculate centrality measures
# degree_centrality = nx.degree_centrality(G)
# betweenness_centrality = nx.betweenness_centrality(G)
# closeness_centrality = nx.closeness_centrality(G)

# # Get top ingredients by centrality
# print("\nMost central ingredients by degree:")
# for ingredient, centrality in sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
#     print(f"{ingredient}: {centrality:.3f}")

# print("\nMost central ingredients by betweenness:")
# for ingredient, centrality in sorted(betweenness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
#     print(f"{ingredient}: {centrality:.3f}")

# print("\nMost central ingredients by closeness:")
# for ingredient, centrality in sorted(closeness_centrality.items(), key=lambda x: x[1], reverse=True)[:10]:
#     print(f"{ingredient}: {centrality:.3f}")

