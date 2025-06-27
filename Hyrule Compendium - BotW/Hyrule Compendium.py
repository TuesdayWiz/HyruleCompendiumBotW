import requests, json
from io import BytesIO
from tkinter import Tk, N, E, S, W, StringVar, IntVar, Toplevel
from tkinter.ttk import Button, Label, Frame
from functools import partial
from PIL import ImageTk, Image

# TODO: - Figure out error with common_locations_list variable

# Defines the URL needed to perform API calls
base_url = 'https://botw-compendium.herokuapp.com/api/v3/compendium/entry/'

# Defines the categories and offsets from 0 needed to reach their ID ranges
offsets = {
    "creatures": [0, 82, 8, 4],
    "monsters": [83, 163, 6, 4],
    "materials": [164, 199, 11, 2],
    "equipment": [200, 383, 10, 8],
    "treasure": [384, 389, 4, 0]
}

# Keeps track of the category currently being looked at
global current_category
current_category = 'creatures'

# Creates a dictionary of item IDs and names 
ids = {}
with open('ids.json') as i_file:
    ids = json.load(i_file)

# Defines the function that the buttons use
def button_func(button_id):
    """Performs the API call, makes a new window, and displays the information requested 
    based on the button that is pressed, the page number, and the offset from the beginning of the list

    Args:
        button_id (integer): The ID (1-25) of the button
    """
    total_button_id = (button_id + (25 * (page.get() - 1))) + offsets[current_category][0]
    data = requests.get(base_url + str(total_button_id)).json()['data']
    #print(data)
    
    # Opens and configures the sub-window
    info_win = Toplevel(root)
    info_win.title(f"{data['name'].capitalize()}")
    info_win.iconbitmap('botw_icon.ico')
    mainframe_new = Frame(info_win, padding="3 3 12 12")
    mainframe_new.grid(column=0, row=0, sticky=(N, W, E, S))
    info_win.columnconfigure(0, weight=1)
    info_win.rowconfigure(0, weight=1)
    
    # Exit button
    def get_rekt():
        """Destroys the subwindow (needs to be a function for a button to call it)
        """
        info_win.destroy()
    
    exit_button = Button(mainframe_new, text='Back', command=get_rekt)
    exit_button.grid(row=4, column=2)
    
    # Gets the picture and (hopefully) displays it
    compendium_img_data = requests.get(data['image']).content
    compendium_img = ImageTk.PhotoImage(Image.open(BytesIO(compendium_img_data)))
    image_label = Label(mainframe_new, image=compendium_img)
    image_label.grid(row=0, column=2)
    
    #---------- Display the info (this one's a doozy) ----------#
    # Universal variables
    category = Label(mainframe_new, text=f"Category: {data['category']}")
    common_locations_list = data['common_locations']
    common_locations = ''
    for l in common_locations_list:
        common_locations += f"{l} "
    common_locations = common_locations[0:-1]
    common_locations_label = Label(mainframe_new, textvariable=common_locations)
    description = Label(mainframe_new, text=f"Description: {data['description']}", wraplength=150)
    name = Label(mainframe_new, text=f"Name: {data['name']}")
    
    category.grid(row=1, column=3)
    common_locations_label.grid(row=2, column=1)
    description.grid(row=1, column=2)
    name.grid(row=1, column=1)
    
    # Per-category variables
    if current_category == 'creatures':
        cooking_effect = ''
        cooking_effect_label = Label(mainframe_new, textvariable=cooking_effect)
        is_edible = False
        edible_label = Label(mainframe_new, textvariable=is_edible)
        hearts_recovered = 0
        hearts_label = Label(mainframe_new, textvariable=hearts_recovered)
        if data['edible'] == 'true':
            is_edible = True
            hearts_recovered = data['hearts_recovered']
            cooking_effect = f"Cooking effect: {data['cooking_effect']}"
            
            cooking_effect_label.grid(row=3, column=1)
            edible_label.grid(row=2, column=3)
            hearts_label.grid(row=3, column=2)
        else:
            edible_label.grid(row=3, column=2)
    elif current_category == 'equipment':
        attack = Label(mainframe_new, text=f"Attack: {data['properties']['attack']}")
        defense = Label(mainframe_new, text=f"Defense: {data['properties']['defense']}")
           
        attack.grid(row=3, column=1)
        defense.grid(row=3, column=3)
    elif current_category == 'materials':
        cooking_effect = Label(mainframe_new, text=f"Cooking effect: {data['cooking_effect']}")
        hearts_recovered = Label(mainframe_new, text=f"Hearts recovered: {data['hearts_recovered']}")
        
        cooking_effect.grid(row=2, column=1)
        hearts_recovered.grid(row=3, column=2)
    elif current_category == 'monsters':
        drops_list = data['drops']
        drops = ''
        for d in drops_list:
            drops += f"{d}, "
        drops = drops[0:-2]
        drops_label = Label(mainframe_new, text=f"Drops: {drops}")
        
        drops_label.grid(row=2, column=2)
    elif current_category == 'treasure':
        drops_list = data['drops']
        drops = ''
        for d in drops_list:
            drops += f"{d}, "
        drops = drops[0:-2]
        drops_label = Label(mainframe_new, text=f"Drops: {drops}")
        
        drops_label.grid(row=2, column=2)
    
    info_win.mainloop()
    

#Sets up the tkinter window
root = Tk()
root.title('Hyrule Compendium - Breath of the Wild')
root.iconbitmap('compendium.ico')   # Icon by Sympnoiaicon on Flaticon.com

# Sets up the grid for use in positioning
mainframe = Frame(root, padding="3 3 12 12")
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Keeps track of the "page" of buttons that is being shown
page = IntVar(value=1)
global total_pages
total_pages = (offsets[current_category][3])

# Creates and defines the buttons, labels, and functions for use with the page system
def place_buttons():
    """Places the grid of selector buttons, as well as the buttons and labels used for paging, onto
    the window.
    Used as a "reset"
    """
    for y in range(2, 7):
        for x in range(0, 5):
            button_num = ((y - 2) * 5) + (x + 1)
            list(button_dict.keys())[button_num - 1].grid(row=y, column=x, sticky=(N, W, E, S))
    back_button.grid(row=7, column=0)
    forward_button.grid(row=7, column=4)
    page_num.grid(row=7, column=1, columnspan=3)

def update_window():
    """Updates the labels on the buttons, as well as which buttons are seen if on the final page
    of a category.
    """
    buttons = list(button_dict.keys())
    for i in list(button_dict.keys()):
        index = list(button_dict.keys()).index(i) + 1
        try:
            button_dict[i].set(ids[str((index + (25 * (page.get() - 1))) + offsets[current_category][0])])
        except:
            pass
    
    place_buttons()
        
        
    if page.get() == total_pages:
        for i in range(offsets[current_category][2], 25):
            buttons[i].grid_forget()
    
    if current_category == 'treasure':
        for j in range (4, 25):
            buttons[j].grid_forget()
        back_button.grid_forget()
        forward_button.grid_forget()
        page_num.grid_forget()

def decrease_page():
    """Decreases the page count and handles looping
    """
    if page.get() == 1:
        page.set(total_pages)
    else:
        page.set(page.get() - 1)
    
    update_window()

def increase_page():
    """Increases the page count and handles looping
    """
    if page.get() == total_pages:
        page.set(1)
    else:
        page.set(page.get() + 1)
    
    update_window()

back_button = Button(mainframe, text='<--', command=decrease_page)
forward_button = Button(mainframe, text='-->', command=increase_page)
page_num = Label(mainframe, textvariable=page)

back_button.grid(row=7, column=0)
forward_button.grid(row=7, column=4)
page_num.grid(row=7, column=1, columnspan=3)

# Creates and places the buttons used to switch between the various categories
def switch_category(category):
    """Handles switching between categories and all the stuff that needs to change with it
    (page numbers, offsets, etc.)

    Args:
        category (int): The index into the list "offsets" that the requested category is at
    """
    global current_category
    global total_pages
    current_category = list(offsets.keys())[category]
    total_pages = offsets[current_category][3]
    page.set(1)
    update_window()

cat1 = Button(mainframe, text='Creatures', command=lambda: switch_category(0))
cat2 = Button(mainframe, text='Monsters', command=lambda: switch_category(1))
cat3 = Button(mainframe, text='Materials', command=lambda: switch_category(2))
cat4 = Button(mainframe, text='Equipment', command=lambda: switch_category(3))
cat5 = Button(mainframe, text='Treasure', command=lambda: switch_category(4))

cat1.grid(row=8, column=0)
cat2.grid(row=8, column=1)
cat3.grid(row=8, column=2)
cat4.grid(row=8, column=3)
cat5.grid(row=8, column=4)

# Creates and places the labels for the title and subtitle
title_font = ("Courier New", 20, "bold")
subtitle_font = ("Courier New", 15)
title = Label(mainframe, text='Hyrule Compendium', font=title_font)
subtitle = Label(mainframe, text='Look through the various creatures and items from The Legend of Zelda: Breath of the Wild!', font=subtitle_font)

title.grid(row=0, column=1, columnspan=3)
subtitle.grid(row=1, column=0, columnspan=5)

# Creates the buttons and their labels and adds them to the grid
button_dict = {}
button_font = ("Courier New", 10)
#   NOTE: This really isn't the safest thing to do here, but it's not affected by user input and it means I don't have to make a million labels and a million buttons manually
for y in range(2, 7):
    for x in range(0, 5):
        button_num = ((y - 2) * 5) + (x + 1)
        #print(button_num)
        # Creates the labels for the buttons and adds them to an ordered list of the label objects
        globals()[f'text{button_num}'] = StringVar(value=ids[str(button_num)])
        
        # Creates the buttons themselves and adds them to a list of the button objects
        globals()[f'button{button_num}'] = Button(mainframe, textvariable=globals()[f'text{button_num}'], command=partial(
            button_func, button_num
        ))
        
        # Adds the buttons, their IDs, and their labels to a dictionary
        button_dict.update({globals()[f'button{button_num}']: globals()[f'text{button_num}']})
        
        # Adds the buttons to the grid based on their positions
        globals()[f'button{button_num}'].grid(row=y, column=x, sticky=(N, W, E, S))

# Runs the window loop so it stays open
root.mainloop()