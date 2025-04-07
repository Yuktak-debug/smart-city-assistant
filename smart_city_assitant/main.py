import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import heapq
import os
import networkx as nx
import tkinter as tk
from tkinter import messagebox


# Step 1: City Graph Data
city_graph = {
    'Home': [('Supermarket', 4), ('Hospital', 2), ('School', 9), ('Library', 7)],
    'Supermarket': [('Home', 4), ('School', 5), ('Mall', 6)],
    'Hospital': [('Home', 2), ('Airport', 10), ('Stadium', 5)],
    'School': [('Supermarket', 5), ('Airport', 3), ('Home', 9), ('Mall', 4), ('Library', 6)],
    'Airport': [('Hospital', 10), ('School', 3), ('Stadium', 8)],
    'Mall': [('Supermarket', 6), ('School', 4)],
    'Stadium': [('Airport', 8), ('Hospital', 5)],
    'Library': [('Home', 7), ('School', 6)]
}

location_types = {
    'Home': 'home',
    'Supermarket': 'shop',
    'Hospital': 'hospital',
    'School': 'school',
    'Airport': 'airport',
    'Mall': 'shop',
    'Stadium': 'stadium',
    'Library': 'library'
}

icon_paths = {
    'home': 'icons\icons8-home-64.png',
    'shop': 'icons\icons8-shop-64.png',
    'hospital': 'icons\icons8-hospital-48.png',
    'school': 'icons\icons8-school-48.png',
    'airport': 'icons\icons8-airport-100.png',
    'mall': 'icons\icons8-mall-64.png',
    'stadium': 'icons\icons8-stadium-48.png',
    'library': 'icons\icons8-library-48.png'
}

# Step 2: Dijkstra Algorithm
def dijkstra(graph, start, end):
    distances = {node: float('inf') for node in graph}
    distances[start] = 0
    previous = {node: None for node in graph}
    queue = [(0, start)]

    while queue:
        current_distance, current_node = heapq.heappop(queue)

        if current_node == end:
            break

        for neighbor, weight in graph[current_node]:
            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous[neighbor] = current_node
                heapq.heappush(queue, (distance, neighbor))

    path = []
    current = end
    while current is not None:
        path.append(current)
        current = previous[current]
    path.reverse()
    return path, distances[end]

# Step 3: Load and Return Icon
def get_icon(path, zoom=0.22):
    return OffsetImage(plt.imread(path), zoom=zoom)

# Step 4: Visualization Function
def visualize_graph_with_path(graph, source, destination):
    G = nx.Graph()
    for node in graph:
        for neighbor, weight in graph[node]:
            G.add_edge(node, neighbor, weight=weight)

    pos = nx.spring_layout(G, seed=42)
    shortest_path, cost = dijkstra(graph, source, destination)
    path_edges = list(zip(shortest_path, shortest_path[1:]))

    plt.figure(figsize=(10, 7))
    nx.draw(G, pos, node_size=0, with_labels=False)
    nx.draw_networkx_edges(G, pos, edge_color='lightgray', width=2)
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color='blue', width=4)

    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

    ax = plt.gca()

    for node in G.nodes:
        loc_type = location_types.get(node)
        icon_path = icon_paths.get(loc_type)
        if icon_path and os.path.exists(icon_path):
            img = get_icon(icon_path, zoom=0.50)
            ab = AnnotationBbox(img, pos[node], frameon=False)
            ax.add_artist(ab)
        else:
            plt.text(pos[node][0], pos[node][1], node, fontsize=10, ha='center')

    path_str = " ➜ ".join(shortest_path)
    plt.title(f"Shortest Path from {source} to {destination}:\n{path_str} (Cost: {cost})", fontsize=13)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

# Step 5: GUI Input with Tkinter
def open_input_gui():
    def on_submit():
        source = source_entry.get().strip().title()
        destination = destination_entry.get().strip().title()

        if source not in city_graph or destination not in city_graph:
            messagebox.showerror("Error", "Invalid source or destination.")
            return

        visualize_graph_with_path(city_graph, source, destination)

    root = tk.Tk()
    root.title("Smart City Path Finder")

    tk.Label(root, text="Enter Source:").grid(row=0, column=0, padx=10, pady=5)
    source_entry = tk.Entry(root)
    source_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(root, text="Enter Destination:").grid(row=1, column=0, padx=10, pady=5)
    destination_entry = tk.Entry(root)
    destination_entry.grid(row=1, column=1, padx=10, pady=5)

    submit_btn = tk.Button(root, text="Show Path", command=on_submit)
    submit_btn.grid(row=2, column=0, columnspan=2, pady=10)

    root.mainloop()

# Step 6: Run the App
open_input_gui()
