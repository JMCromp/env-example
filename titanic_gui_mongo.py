import pandas as pd
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import scrolledtext
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sb
import pymongo
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

# Get DB URL from .env
db_connect = os.getenv("DATABASE_URL")
# Connect to MongoDB
client = MongoClient(db_connect)
db = client['Titanic-Data']
collection = db['Titanic-V1']

# If no object (JSON) data exists in collection
if collection.count_documents({}) == 0:
    # Load CSV
    titanic_data = pd.read_csv('train.csv')
    # Insert data into MongoDB
    collection.insert_many(titanic_data.to_dict('records'))

def get_data_from_mongodb():
    try:
        data = pd.DataFrame(list(collection.find()))
        print('Data retrieved from MongoDB')
        return data
    except Exception as e:
        print(f'Failed to retrieve data from MongoDB: {e}')
        return pd.DataFrame()
    
# Call get_data_from_mongodb
titanic_data = get_data_from_mongodb()

def connect_to_mongodb():
    try:
        client.server_info()
        console_output.insert(tk.END, 'Connected to MongoDB!\n')
    except Exception as e:
        console_output.insert(tk.END,'Failed to connect to MongoDB.\n')

# Function to add single column of data to dataset
def add_column_to_collection(collection_name, column_name, default_value=None):
    try:
        # First check to see if column already exists
        if column_name is db[collection_name].find_one({}):
            # If it does output message and exit function using return
            console_output.insert(tk.END, f"Column '{column_name} already exists in {collection_name}\n")
            return
        
        # If the column does not exist continue and do this
        db[collection_name].update_many({}, {'$set': {column_name: default_value}})
        # Confirm entry by outputting to the console output box
        console_output.insert(tk.END, f"Column '{column_name} successfully added to {collection_name}\n")
    except Exception as e:
        console_output.insert(tk.END, f"Error adding column '{column_name}' to collection '{collection_name}: {e}")

def clean_data(data):
    temp = data.drop('Cabin', axis=1) # drop the Cabin column
    temp = data.dropna() # drop missing values
    return temp

def create_graph(selected_graph_type, selected_first_feature, selected_second_feature, selected_colour_palette, cleaned_data, selected_bins):
    # set target figure size in inches
    plt.figure(figsize=(8, 6))
    #  use seaborn function to select palette from user selection
    sb.set_palette(selected_colour_palette)

    # conditonal test for chosen graph type
    if selected_graph_type == 'Bar Plot':
        if selected_second_feature:
            sb.countplot(x=selected_first_feature, data=cleaned_data, hue=selected_second_feature)
            plt.title(f'Bar Plot of {selected_first_feature} by {selected_second_feature}')
        else:
            sb.countplot(x=selected_first_feature, data=cleaned_data)
            plt.title(f'Bar Plot of {selected_first_feature}')
    elif selected_graph_type == 'Histogram':
        sb.histplot(cleaned_data[selected_first_feature], kde=True, bins=selected_bins)
        plt.title(f'Histogram of {selected_first_feature}')

    return plt

def generate_graph():
    # get references to user selections
    selected_graph_type = graph_type_var.get()
    selected_first_feature = first_feature_var.get()
    selected_second_feature = second_feature_var.get()
    selected_colour_palette = colour_palette_var.get()
    selected_bins = bins_entry.get()

    #  try and do this, otherwise accomodate for the error to prevent a crash
    try:
        selected_bins = int(selected_bins)
    except:
        messagebox.showerror("Error", "Number of bins must be an integer")
        # return will 'exit' the function early
        return

    # process and clean the data  using clean_data function
    # cleaned data is returned and stored in 'cleaned_data'
    cleaned_data = clean_data(titanic_data)

    plt = create_graph(selected_graph_type, selected_first_feature, selected_second_feature, selected_colour_palette, cleaned_data, selected_bins)

    for widget in graph_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    return

# GUI init
window = tk.Tk()
window.title("Titanic Data Analysis")

# Dropdown selection for graph type
graph_type_label = ttk.Label(window, text="Select graph type:")
graph_type_label.pack()
graph_types = ['Bar Plot', 'Histogram']
graph_type_var = tk.StringVar(window)
graph_type_var.set(graph_types[0])
graph_type_dropdown = ttk.Combobox(window, textvariable=graph_type_var, value=graph_types)
graph_type_dropdown.pack()

#  Dropdown to select first feature
first_feature_label = ttk.Label(window, text="Select first feature:")
first_feature_label.pack()
features = list(titanic_data.columns)
first_feature_var = tk.StringVar(window)
first_feature_var.set(features[0])
first_feature_dropdown = ttk.Combobox(window, textvariable=first_feature_var, value=features)
first_feature_dropdown.pack()

# Dropdown to select second feature
second_feature_label = ttk.Label(window, text="Select second feature:")
second_feature_label.pack()
features_with_blank = [''] + features
second_feature_var = tk.StringVar(window)
second_feature_var.set(features_with_blank[0])
second_feature_dropdown = ttk.Combobox(window, textvariable=second_feature_var, values=features_with_blank)
second_feature_dropdown.pack()

# Input box for bins
bins_label =  ttk.Label(window, text="Number of bins:")
bins_label.pack()
bins_entry = ttk.Entry(window)
bins_entry.pack()
bins_entry.insert(0, 0)

#  Dropdown for colour palette selection
colour_palette_label = ttk.Label(window, text="Select colour palette:")
colour_palette_label.pack()
colour_palettes = ['viridis', 'deep', 'muted', 'pastel', 'bright', 'dark', 'colorblind', 'Set1', 'Set2', 'coolwarm']
colour_palette_var = tk.StringVar(window)
colour_palette_var.set(colour_palettes[0])
colour_palette_dropdown = ttk.Combobox(window, textvariable=colour_palette_var, value=colour_palettes)
colour_palette_dropdown.pack()

# Create a frame to act as a canvas
graph_frame = ttk.Frame(window)
graph_frame.pack()

# Button to generate  graphs
generate_button = ttk.Button(window, text="Generate Graph", command=generate_graph)
generate_button.pack()

# Create frame for terminal output
console_frame = ttk.Frame(window)
console_frame.pack()

console_label = ttk.Label(console_frame, text="Console output:")
console_label.pack()

console_output = scrolledtext.ScrolledText(console_frame, wrap=tk.WORD, width=40, height=10)
console_output.pack()

# Connect button for MongoDB
connect_button = ttk.Button(window, text="Connect  to MongoDB", command=connect_to_mongodb)
connect_button.pack()

# TESTING PURPOSES
add_column_to_collection("Titanic-V1", "Test", 1)

# GUI render
window.mainloop()