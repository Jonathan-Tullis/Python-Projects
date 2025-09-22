from tkinter import *
from tkinter import messagebox

# Player and Room Setup
player_state = {
    "location": "entrance",
    "inventory": [],
    "escaped": False
}

rooms = {
    "entrance": {
        "description": "You're at the dark entrance of a dungeon. A torch flickers nearby.",
        "exits": {"north": "hallway"},
        "items": []
    },
    "hallway": {
        "description": "A long hallway with damp walls.",
        "exits": {"south": "entrance", "east": "armory", "north": "throne_room"},
        "items": ["sword"]
    },
    "armory": {
        "description": "The old armory. There’s a locked chest here.",
        "exits": {"west": "hallway"},
        "items": ["key"]
    },
    "throne_room": {
        "description": "The final room. A massive door leads out of the dungeon.",
        "exits": {"south": "hallway"},
        "items": [],
        "requires": "key"
    }
}

# Game Logic
def move(direction):
    current = player_state["location"]
    if direction in rooms[current]["exits"]:
        next_room = rooms[current]["exits"][direction]
        required_item = rooms[next_room].get("requires")
        if required_item and required_item not in player_state["inventory"]:
            return f"You need the {required_item} to enter {next_room}."
        player_state["location"] = next_room
        return describe_room(next_room)
    return "You can't go that way."

# Room transition logic for testing
def move_to_room(current_room, choice):
    transitions = {
        "start": {"Go Left": "armory", "Go Right": "beast_room"},
        "armory": {"Go Back": "start", "Go Forward": "dragon_lair"},
        "beast_room": {"Retreat": "start"},
        "dragon_lair": {"Escape": "exit"}
    }
    return transitions.get(current_room, {}).get(choice, None)

def describe_room(name):
    room = rooms[name]
    desc = room["description"]

    # Check if items are already picked up
    visible_items = [item for item in room["items"] if item not in player_state["inventory"]]

    if visible_items:
        desc += f"\nYou see: {', '.join(visible_items)}"
    return desc

def pick_up_item():
    room = rooms[player_state["location"]]
    for item in list(room["items"]):
        if item not in player_state["inventory"]:
            room["items"].remove(item)
            player_state["inventory"].append(item)
            return f"You picked up the {item}."
    return "There's nothing to pick up."

# Inventory handling for tests
def add_to_inventory(inventory, item):
    if item not in inventory:
        inventory.append(item)

def remove_from_inventory(inventory, item):
    if item in inventory:
        inventory.remove(item)

def try_escape():
    if player_state["location"] == "throne_room" and "key" in player_state["inventory"]:
        player_state["escaped"] = True
        return "You unlocked the door and escaped the dungeon! You win!"
    return "You can't escape yet."

# GUI
def update_log(text):
    log.config(state=NORMAL)
    log.insert(END, text + "\n\n")
    log.config(state=DISABLED)
    log.yview(END)

def handle_move(direction):
    result = move(direction)
    update_log(result)

def handle_pickup():
    result = pick_up_item()
    update_log(result)

def handle_escape():
    result = try_escape()
    update_log(result)
    if player_state["escaped"]:
        messagebox.showinfo("Victory", "You escaped the dungeon!")
        root.quit()

# ... (all your existing code above stays the same)

def start_game():
    update_log(describe_room(player_state["location"]))

# Only run the GUI if this file is executed directly
if __name__ == "__main__":
    root = Tk()
    root.title("Dungeon Escape")
    root.geometry("500x400")

    log = Text(root, wrap=WORD, state=DISABLED, height=15)
    log.pack(pady=10, padx=10)

    frame = Frame(root)
    frame.pack()

    Button(frame, text="Go North", command=lambda: handle_move("north")).grid(row=0, column=1)
    Button(frame, text="Go South", command=lambda: handle_move("south")).grid(row=2, column=1)
    Button(frame, text="Go East", command=lambda: handle_move("east")).grid(row=1, column=2)
    Button(frame, text="Go West", command=lambda: handle_move("west")).grid(row=1, column=0)
    Button(root, text="Pick Up Item", command=handle_pickup).pack(pady=5)
    Button(root, text="Try to Escape", command=handle_escape).pack(pady=5)

    start_game()
    root.mainloop()
