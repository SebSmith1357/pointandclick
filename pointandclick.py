pointandclick.py
import tkinter as tk
from tkinter import scrolledtext
from PIL import Image, ImageTk
import random

text_and_button_color = "white"

class MovieTicketAdventure:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Ticket Adventure")
        self.root.geometry("800x600")

        try:
            self.outside_bg_image = Image.open("outside_building.jpg")
            self.outside_bg_photo = ImageTk.PhotoImage(self.outside_bg_image.resize((800, 600)))
            self.party_bg_image = Image.open("party_background.jpg")
            self.party_bg_photo = ImageTk.PhotoImage(self.party_bg_image.resize((800, 600)))
            self.locked_bg_image = Image.open("locked_room.jpg")
            self.locked_bg_photo = ImageTk.PhotoImage(self.locked_bg_image.resize((800, 600)))
            self.ticket_bg_image = Image.open("ticket_room.jpg")
            self.ticket_bg_photo = ImageTk.PhotoImage(self.ticket_bg_image.resize((800, 600)))
            self.bg_label = tk.Label(root, image=self.outside_bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except FileNotFoundError as e:
            print(f"Background image not found: {e}. Using default background.")
            self.bg_label = None
            self.outside_bg_photo = None
            self.party_bg_photo = None
            self.locked_bg_photo = None
            self.ticket_bg_photo = None

        self.dialogue_history = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=60, height=3, bg=text_and_button_color)
        self.dialogue_history.place(relx=0.5, rely=0.75, anchor=tk.CENTER)

        self.choices = []
        self.choice_buttons = []
        self.current_node = "outside_building"
        self.has_key = False
        self.has_info = False
        self.tickets_found = False
        self.level = 1
        self.pin_entered = False
        self.pin_input = ""

        self.dialogue_tree = {
            "outside_building": {
                "text": "You arrive at the building. Sonic, Tails, Knuckles, Omega, and Rouge are standing outside. The building is locked.",
                "choices": [
                    {"text": "Talk to Sonic.", "next_node": "talk_sonic"},
                    {"text": "Talk to Tails.", "next_node": "talk_tails"},
                    {"text": "Talk to Knuckles.", "next_node": "talk_knuckles"},
                    {"text": "Talk to Omega.", "next_node": "talk_omega"},
                    {"text": "Talk to Rouge.", "next_node": "talk_rouge"},
                    {"text": "Interact with the keypad.", "next_node": "keypad"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "talk_sonic": {
                "text": "Sonic: We're locked out. No one has the key, and we can't remember the PIN.",
                "choices": [{"text": "Go back.", "next_node": "outside_building"}],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "talk_tails": {
                "text": "Tails: I think the PIN started with 6.",
                "choices": [{"text": "Go back.", "next_node": "outside_building"}],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "talk_knuckles": {
                "text": "Knuckles: This is frustrating! We're all locked out.",
                "choices": [{"text": "Go back.", "next_node": "outside_building"}],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "talk_omega": {
                "text": "Omega: Access denied. No key, PIN unknown.",
                "choices": [{"text": "Go back.", "next_node": "outside_building"}],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "talk_rouge": {
                "text": "Rouge: I think the PIN ended with 484.",
                "choices": [{"text": "Go back.", "next_node": "outside_building"}],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "keypad": {
                "text": "Enter the PIN: " + self.pin_input,
                "choices": [
                    {"text": "Enter", "next_node": "enter_pin"},
                    {"text": "Go back.", "next_node": "outside_building"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.outside_bg_photo)
            },
            "enter_pin": {
                "text": "Incorrect PIN." if self.pin_input != "6484" else "The door unlocks! You enter the building.",
                "choices": [{"text": "Enter the party.", "next_node": "entrance"} if self.pin_input == "6484" else {"text": "Go back.", "next_node": "keypad"}],
                "action": lambda: self.change_level(2) if self.pin_input == "6484" else None,
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo) if self.pin_input == "6484" else self.bg_label.config(image=self.outside_bg_photo),
            },
            "entrance": {
                "text": "You enter a lively party. Your mission: find movie tickets!",
                "choices": [
                    {"text": "Talk to someone.", "next_node": "talk_person"},
                    {"text": "Explore the room.", "next_node": "explore_room"},
                    {"text": "Try the secret room.", "next_node": "secret_room"} if self.has_key and self.has_info else {"text":"Try the secret room.","next_node":"locked_secret_room"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "talk_person": {
                "text": "You talk to a partygoer. They seem distracted.",
                "choices": [
                    {"text": "Ask about the tickets.", "next_node": "ask_tickets"},
                    {"text": "Look around while they're distracted.", "next_node": "look_distracted"},
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "explore_room": {
                "text": "You search the room. You see a locked door and a table with a note.",
                "choices": [
                    {"text": "Read the note.", "next_node": "read_note"},
                    {"text": "Try the locked door.", "next_node": "locked_door"},
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "ask_tickets": {
                "text": "They mention hearing someone talking about tickets in a 'secret room'.",
                "choices": [
                    {"text": "Try to learn more.", "next_node": "learn_more"},
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.self.party_bg_photo)
            },
            "look_distracted": {
                "text": "You find a shiny key under a cushion!",
                "choices": [
                    {"text": "Take the key.", "next_node": "take_key"},
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "read_note": {
                "text": "The note says: 'The tickets are hidden where the music plays loudest.'",
                "choices": [
                    {"text": "Remember the clue.", "next_node": "remember_clue"},
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "locked_door": {
                "text": "The door is locked.",
                "choices": [
                    {"text": "Go back.", "next_node": "explore_room"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "learn_more": {
                "text": "They don't remember much, but mention a 'key' is needed.",
                "choices": [
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "take_key": {
                "text": "You now have the key!",
                "choices": [
                    {"text": "Go back to the entrance.", "next_node": "entrance"}
                ],
                "action": lambda: setattr(self, "has_key", True),
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "remember_clue": {
                "text": "You now have a clue!",
                "choices": [
                    {"text": "Go back to the entrance.", "next_node": "entrance"}],
                "action": lambda: setattr(self, "has_info", True),
                "bg_change": lambda: self.bg_label.config(image=self.party_bg_photo)
            },
            "secret_room":{
                "text":"You enter a very loud room, there is a speaker system. Behind it, you see something shiny.",
                "choices": [
                    {"text":"Investigate the shiny object", "next_node":"investigate_shiny"},
                    {"text":"Leave the loud room", "next_node":"entrance"}
                ],
                "condition": lambda: self.has_key and self.has_info,
                "bg_change": lambda: self.bg_label.config(image=self.ticket_bg_photo),
            },
            "investigate_shiny":{
                "text": "You found the tickets! You win!",
                "choices": [],
                "action": lambda: setattr(self, "tickets_found", True),
                "bg_change": lambda: self.bg_label.config(image=self.ticket_bg_photo),
            },
            "locked_secret_room":{
                "text":"The door to the secret room is locked.",
                "choices":[
                    {"text":"Go back to the entrance", "next_node":"entrance"}
                ],
                "bg_change": lambda: self.bg_label.config(image=self.locked_bg_photo),
            },
        }

        self.root.bind("<Key>", self.handle_key_press)
        self.update_dialogue()

    def update_dialogue(self):
        self.dialogue_history.config(state=tk.NORMAL)
        self.dialogue_history.delete(1.0, tk.END)
        node = self.dialogue_tree[self.current_node]
        self.dialogue_history.insert(tk.END, node["text"] + "\n")
        self.dialogue_history.config(state=tk.DISABLED)
        self.dialogue_history.see(tk.END)

        for button in self.choice_buttons:
            button.destroy()
        self.choice_buttons = []

        num_choices = len(node["choices"])
        num_rows = (num_choices + 1) // 2
        start_y = 0.85 - (0.05 * (num_rows - 1) / 2)  # Increased starting y to move buttons down

        for i, choice in enumerate(node["choices"]):
            next_node = choice["next_node"]
            if "condition" in node and not node["condition"]():
                if next_node == "secret_room":
                    next_node = "locked_secret_room"
            button_text = choice["text"]
            button_width = max(len(button_text) + 2, 25)
            button = tk.Button(self.root, text=button_text, command=lambda next_node=next_node: self.make_choice(next_node), bg=text_and_button_color)
            self.choice_buttons.append(button)
            self.choice_buttons[-1].config(width=button_width)
            row = i // 2
            col = i % 2
            x_offset = 0.35 if col == 0 else 0.65  # Moved buttons closer horizontally
            self.choice_buttons[-1].place(relx=x_offset, rely=start_y + 0.05 * row, anchor=tk.CENTER)

    def make_choice(self, next_node):
        self.current_node = next_node
        if "action" in self.dialogue_tree[self.current_node]:
            self.dialogue_tree[self.current_node]["action"]()
        if "bg_change" in self.dialogue_tree[self.current_node]:
            self.dialogue_tree[self.current_node]["bg_change"]()
        else:
            if self.level == 1 and self.outside_bg_photo:
                self.bg_label.config(image=self.outside_bg_photo)
            elif self.level == 2 and self.party_bg_photo:
                self.bg_label.config(image=self.party_bg_photo)

        self.update_dialogue()

    def change_level(self, level):
        self.level = level
        if level == 2:
            self.current_node = "entrance"

    def handle_key_press(self, event):
        if self.current_node == "keypad":
            if event.char.isdigit():
                self.pin_input += event.char
                self.dialogue_tree["keypad"]["text"] = "Enter the PIN: " + self.pin_input
                self.update_dialogue()
            elif event.keysym == "Return":
                self.make_choice("enter_pin")
            elif event.keysym == "BackSpace":
                self.pin_input = self.pin_input[:-1]
                self.dialogue_tree["keypad"]["text"] = "Enter the PIN: " + self.pin_input
                self.update_dialogue()

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieTicketAdventure(root)
    root.mainloop()