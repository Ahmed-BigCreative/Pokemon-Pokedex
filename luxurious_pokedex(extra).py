import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import tkinter as tk

# Load Pokémon dataset
df = pd.read_csv("pokemon_data.csv")

# Function to plot the spider chart for Pokémon stats
def plot_spider_chart(pokemon_name, stats):
    categories = ["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]
    values = stats.values.flatten().tolist()
    values += values[:1]  # Close the polygon
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False).tolist()
    angles += angles[:1]

    plt.figure(figsize=(6, 6), facecolor="#2e2e2e")
    ax = plt.subplot(111, polar=True)
    ax.set_facecolor("#2e2e2e")
    ax.plot(angles, values, color="gold")
    ax.fill(angles, values, alpha=0.3, color="gold")
    ax.set_yticklabels(range(0, int(max(values) + 20), 20), color="white")
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, color="white", fontsize=12)
    plt.title(f"{pokemon_name} Stats", color="white", fontsize=16, y=1.1)
    plt.show(block=False)

# Function to display Pokémon information
def display_pokemon_info(pokemon):
    stats = pokemon[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]]
    label_result.config(
        text=f"Found: {pokemon['Name']} ({pokemon['Type 1']}/{pokemon['Type 2']})\n"
             f"HP: {stats['HP']} | Attack: {stats['Attack']} | Defense: {stats['Defense']}\n"
             f"Sp. Atk: {stats['Sp. Atk']} | Sp. Def: {stats['Sp. Def']} | Speed: {stats['Speed']}"
    )
    plot_spider_chart(pokemon["Name"], stats)

# Function to search Pokémon by name
def search_by_name(event=None):
    name = entry_name.get().strip().lower()
    result = df[df["Name"].str.lower().str.contains(name, na=False)]
    if not result.empty:
        display_pokemon_info(result.iloc[0])
    else:
        label_result.config(text="No Pokemon found by that name.")

# Function to search Pokémon by type
def search_by_type(event=None):
    p_type = entry_type.get().strip().capitalize()
    result = df[(df["Type 1"] == p_type) | (df["Type 2"] == p_type)]
    if not result.empty:
        display_pokemon_info(result.iloc[0])
    else:
        label_result.config(text=f"No Pokemon found with type '{p_type}'.")

# Function to handle Pokémon selection from the list
def on_pokemon_select(event):
    selected_index = listbox_pokemon.curselection()
    if selected_index:
        selected_pokemon = df.iloc[selected_index[0]]
        display_pokemon_info(selected_pokemon)

# Create main window
root = tk.Tk()
root.title("Luxurious Pokedex")
root.geometry("600x800")
root.config(bg="#1e1e1e")

# Title label
tk.Label(root, text="Luxurious Pokedex", font=("Helvetica", 24, "bold"), fg="gold", bg="#1e1e1e").pack(pady=10)

# Welcome message
welcome_message = (
    "Welcome to Luxurious Pokedex!\n"
    "I had more help with this version and wanted to experiment and play around a little bit. (outside of my task)\n"
    "This version boasts:\n"
    " - Better UI Theme\n"
    " - Better Readability & Fonts\n"
    " - A dedicated Spider Graph for Each Pokémon\n"
    "Thank You!"
)
tk.Label(root, text=welcome_message, font=("Helvetica", 12), fg="lightgray", bg="#1e1e1e", justify="left", anchor="nw", wraplength=550).pack(pady=5, padx=20, anchor="nw")

# Search by name section
frame_name = tk.Frame(root, bg="#1e1e1e")
frame_name.pack(pady=5, fill=tk.X, padx=20)
tk.Label(frame_name, text="Enter Pokemon Name:", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
entry_name = tk.Entry(frame_name, width=20, bg="#333", fg="white", insertbackground="white")
entry_name.pack(side=tk.LEFT, padx=10)
tk.Button(frame_name, text="Search", command=search_by_name, bg="#444", fg="white").pack(side=tk.LEFT)
entry_name.bind("<Return>", search_by_name)

# Search by type section
frame_type = tk.Frame(root, bg="#1e1e1e")
frame_type.pack(pady=5, fill=tk.X, padx=20)
tk.Label(frame_type, text="Enter Pokemon Type (e.g., Fire, Water):", fg="white", bg="#1e1e1e").pack(side=tk.LEFT)
entry_type = tk.Entry(frame_type, width=20, bg="#333", fg="white", insertbackground="white")
entry_type.pack(side=tk.LEFT, padx=10)
tk.Button(frame_type, text="Search", command=search_by_type, bg="#444", fg="white").pack(side=tk.LEFT)
entry_type.bind("<Return>", search_by_type)

# Pokémon stats result display
label_result = tk.Label(root, text="", font=("Helvetica", 14), wraplength=550, fg="white", bg="#1e1e1e", justify="left")
label_result.pack(pady=10, padx=20)

# Scrollable list of Pokémon names
frame_list = tk.Frame(root, bg="#1e1e1e")
frame_list.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
tk.Label(frame_list, text="Select a Pokemon from the list:", font=("Helvetica", 14), fg="white", bg="#1e1e1e").pack(anchor=tk.W)
scrollbar = tk.Scrollbar(frame_list)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
listbox_pokemon = tk.Listbox(frame_list, yscrollcommand=scrollbar.set, height=10, font=("Helvetica", 12), bg="#333", fg="white")
listbox_pokemon.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.config(command=listbox_pokemon.yview)

# Populate the listbox with Pokémon names
for name in df["Name"]:
    listbox_pokemon.insert(tk.END, name)
listbox_pokemon.bind("<<ListboxSelect>>", on_pokemon_select)

# Run the app
root.mainloop()
