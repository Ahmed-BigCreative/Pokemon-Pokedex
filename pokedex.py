import pandas as pd
import tkinter as tk

# get pokemon info
df = pd.read_csv("pokemon_data.csv")

# displays pokemon information
def display_pokemon_info(pokemon):
    stats = pokemon[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]]
    type_2 = pokemon["Type 2"] if pd.notna(pokemon["Type 2"]) else "None"
    result_text = (
        f"Name: {pokemon['Name']}\n"
        f"Type: {pokemon['Type 1']}/{type_2}\n"
        f"HP: {stats['HP']}, Attack: {stats['Attack']}, Defense: {stats['Defense']}\n"
        f"Sp. Atk: {stats['Sp. Atk']}, Sp. Def: {stats['Sp. Def']}, Speed: {stats['Speed']}"
    )
    label_result.config(text=result_text)

# searches pokemon bu name
def search_by_name():
    name = entry_name.get().strip().lower()
    result = df[df["Name"].str.lower().str.contains(name, na=False)]
    if not result.empty:
        display_pokemon_info(result.iloc[0])
    else:
        label_result.config(text="No Pokemon found by that name.")

# search for pokemon by type
def search_by_type():
    p_type = entry_type.get().strip().capitalize()
    result = df[(df["Type 1"] == p_type) | (df["Type 2"] == p_type)]
    if not result.empty:
        display_pokemon_info(result.iloc[0])
    else:
        label_result.config(text=f"No Pokemon found with type '{p_type}'.")

# pokemon lsit selection
def on_pokemon_select(event):
    selected_index = listbox_pokemon.curselection()
    if selected_index:
        selected_pokemon = df.iloc[selected_index[0]]
        display_pokemon_info(selected_pokemon)

# Create main Window
root = tk.Tk()
root.title("Simple Pokedex")
root.geometry("500x700")

tk.Label(root, text="Simple Pokedex", font=("Arial", 18, "bold")).pack(pady=10)

# Name Search
tk.Label(root, text="Enter Pokemon Name:").pack()
entry_name = tk.Entry(root)
entry_name.pack(pady=5)
tk.Button(root, text="Search by Name", command=search_by_name).pack(pady=5)

# Type Searching
tk.Label(root, text="Enter Pokemon Type (e.g., Fire, Water):").pack()
entry_type = tk.Entry(root)
entry_type.pack(pady=5)
tk.Button(root, text="Search by Type", command=search_by_type).pack(pady=5)

# stats
label_result = tk.Label(root, text="", font=("Arial", 12), justify="left", wraplength=450)
label_result.pack(pady=10)

# pokeom list
tk.Label(root, text="Select a Pokemon from the list:").pack(anchor=tk.W)
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

listbox_pokemon = tk.Listbox(root, yscrollcommand=scrollbar.set, height=15)
listbox_pokemon.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
scrollbar.config(command=listbox_pokemon.yview)

for name in df["Name"]:
    listbox_pokemon.insert(tk.END, name)

listbox_pokemon.bind("<<ListboxSelect>>", on_pokemon_select)

# runner
root.mainloop()