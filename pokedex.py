import pandas as pd
import tkinter as tk

# get pokemon info from dataframe
df = pd.read_csv("pokemon_data.csv")

# displays pokemon information
def display_pokemon_info(pokemon):
    stats = pokemon[["HP", "Attack", "Defense", "Sp. Atk", "Sp. Def", "Speed"]] #gets info from dataframe - key stats
    type_2 = pokemon["Type 2"] if pd.notna(pokemon["Type 2"]) else "None" # types for pokemon, none if they only have 1 attribute
    result_text = ( # makes it into string so its readable
        f"Name: {pokemon['Name']}\n"
        f"Type: {pokemon['Type 1']}/{type_2}\n"
        f"HP: {stats['HP']}, Attack: {stats['Attack']}, Defense: {stats['Defense']}\n"
        f"Sp. Atk: {stats['Sp. Atk']}, Sp. Def: {stats['Sp. Def']}, Speed: {stats['Speed']}"
    )
    label_result.config(text=result_text) #display

# searches pokemon bu name
def search_by_name():
    name = entry_name.get().strip().lower() # gets the name and removes extra characters
    result = df[df["Name"].str.lower().str.contains(name, na=False)] # gets pokemon with similar name
    if not result.empty:
        display_pokemon_info(result.iloc[0]) #displays the first result for the matching name
    else:
        label_result.config(text="No Pokemon found by that name.") # the error message

# search for pokemon by type
def search_by_type():
    p_type = entry_type.get().strip().capitalize() #search for the pokemon by typing their type
    result = df[(df["Type 1"] == p_type) | (df["Type 2"] == p_type)] # pokemon with either type 1 /2 of this
    if not result.empty:
        display_pokemon_info(result.iloc[0]) # shows the pokemon
    else:
        label_result.config(text=f"No Pokemon found with type '{p_type}'.") # error if none are found

# pokemon lsit selection
def on_pokemon_select(event):
    selected_index = listbox_pokemon.curselection()
    if selected_index:
        selected_pokemon = df.iloc[selected_index[0]] #gets pokemon from dataframe
        display_pokemon_info(selected_pokemon)

# Create main Window
root = tk.Tk() #window
root.title("Simple Pokedex")
root.geometry("500x700") #window size

tk.Label(root, text="Simple Pokedex", font=("Arial", 18, "bold")).pack(pady=10) # label with placement

# Name Search
tk.Label(root, text="Enter Pokemon Name:").pack() #label with prompts to enter pokemon name
entry_name = tk.Entry(root)
entry_name.pack(pady=5)
tk.Button(root, text="Search by Name", command=search_by_name).pack(pady=5) #button for search by name

# Type Searching
tk.Label(root, text="Enter Pokemon Type (e.g., Fire, Water):").pack() #label with prompt for pokemon type
entry_type = tk.Entry(root)
entry_type.pack(pady=5)
tk.Button(root, text="Search by Type", command=search_by_type).pack(pady=5) # button for that search

# stats
label_result = tk.Label(root, text="", font=("Arial", 12), justify="left", wraplength=450) #label for stats
label_result.pack(pady=10)

# pokeom list
tk.Label(root, text="Select a Pokemon from the list:").pack(anchor=tk.W) # label for the pokemon lsit
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y) #adds scrollbar

listbox_pokemon = tk.Listbox(root, yscrollcommand=scrollbar.set, height=15) #portrays pokemon names
listbox_pokemon.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
scrollbar.config(command=listbox_pokemon.yview) #links scrollbar to list

for name in df["Name"]:
    listbox_pokemon.insert(tk.END, name) #adds the pokemon to the list

listbox_pokemon.bind("<<ListboxSelect>>", on_pokemon_select)  #binds pokemon to the selected places so its information appears when you click on its name

# runner
root.mainloop() #tkinker gui
