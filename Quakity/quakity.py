import tkinter as tk
import customtkinter as ctk # Customizes the buttons accordingly
import webbrowser # Let user click on links the chatbot presented
from PIL import Image, ImageTk # To allow images in the app

class QuackityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Quackity")

        self.vent_count = 0 
        self.chat_state = "waiting_for_score" 
        
        # Using a try-except here because iconphoto is notorious for crashing if the path is slightly off
        try:
            self.icon_img = tk.PhotoImage(file="media/quak.png")
            self.root.iconphoto(False, self.icon_img)
        except:
            pass

        # Standard mobile-ish aspect ratio. Hardcoded fixed size to keep the UI from breaking.
        self.width, self.height = 300, 600
        self.root.geometry(f"{self.width}x{self.height}")
        self.root.resizable(False, False)
        self.root.configure(bg="#EED594")

        # Containerizing everything in a main frame makes it way easier to clear the screen later
        self.main_container = tk.Frame(self.root, bg="#EED594")
        self.main_container.pack(fill="both", expand=True)

        # Pre-loading assets to memory now so there's no lag when switching frames
        self.chick_img = self.load_image("media/chick.png", (160, 160))
        self.back_img = self.load_image("media/back.png", (45, 45))
        self.enter_img = self.load_image("media/enter.png", (45, 45))
        self.bot_icon = self.load_image("media/mascot.png", (40, 40)) 
        
        try:
            logo_raw = Image.open("media/Quackity!.png")
            logo_res = logo_raw.resize((140, 40), Image.Resampling.LANCZOS)
            self.logo_img = ImageTk.PhotoImage(logo_res)
        except:
            self.logo_img = None

        self.show_frame_1()

    def load_image(self, path, size):
        """Helper to handle PIL conversion without repeating code 10 times."""
        try:
            img = Image.open(path)
            img = img.resize(size, Image.Resampling.LANCZOS)
            return ImageTk.PhotoImage(img)
        except:
            return None

    def clear_screen(self):
        """Standard 'State Reset'—nuke all widgets in the main container."""
        for widget in self.main_container.winfo_children():
            widget.destroy()

    def show_frame_1(self):
        self.clear_screen()
        # Canvas is better for backgrounds because we can place widgets at specific coords
        canvas = tk.Canvas(self.main_container, width=self.width, height=self.height, highlightthickness=0)
        canvas.pack(fill="both", expand=True)
        
        try:
            self.bg_raw = Image.open("media/Frame 1.png")
            self.bg_res = self.bg_raw.resize((self.width, self.height), Image.Resampling.LANCZOS)
            self.bg_img = ImageTk.PhotoImage(self.bg_res)
            canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        except:
            pass

        btn = ctk.CTkButton(
            self.main_container, text="Chat Now", font=("Helvetica", 16, "bold"),
            fg_color="#8F693E", bg_color="#EED594", corner_radius=20,
            border_width=4, border_color="#765843", text_color="#FFF6DD",
            width=230, height=50, command=self.show_frame_2
        )
        # Using canvas window instead of .place() so it stays centered on the background
        canvas.create_window(150, 530, window=btn)

    def show_frame_2(self):
        self.clear_screen()
        # Top nav bar area
        self.header_frame = tk.Frame(self.main_container, bg="#F5A64B", height=80)
        self.header_frame.pack(fill="x", side="top")
        self.header_frame.pack_propagate(False) # Stop the frame from shrinking to the size of the logo

        back_btn = tk.Button(self.header_frame, image=self.back_img, bg="#F5A64B", 
                             activebackground="#F5A64B", borderwidth=0, cursor="hand2",
                             command=self.show_frame_1)
        back_btn.place(x=15, y=18)

        logo_label = tk.Label(self.header_frame, image=self.logo_img, bg="#F5A64B")
        logo_label.place(x=80, y=18)

        self.content_frame = tk.Frame(self.main_container, bg="#EED594")
        self.content_frame.pack(fill="both", expand=True)

        self.mascot = tk.Label(self.content_frame, image=self.chick_img, bg="#EED594")
        self.mascot.pack(pady=(40, 5)) 

        self.title_label = tk.Label(self.content_frame, text="QUACK!\nHow can I help you today?", 
                         font=("Helvetica", 14, "bold"), bg="#EED594", fg="#3E2723")
        self.title_label.pack(pady=5)

        self.grid_frame = tk.Frame(self.content_frame, bg="#EED594")
        self.grid_frame.pack(pady=(10, 20)) 

        # User will be choosing whichever service they want to receive in the chatbot
        # Usually, those who are in need of help dont usually have the right head-space
        # Putting the options upfront will make it convenient for the user
        options = [
            ("Pulse Check", self.show_pulse_check),
            ("Vent Space", self.show_vent_space),
            ("Mindful Tools", self.show_mindful_tools),           
            ("Instant Support", self.show_instant_support)
        ]

        # Use enumerate and modulo to build the 2x2 grid dynamically
        for i, (text, cmd) in enumerate(options):
            b = ctk.CTkButton(self.grid_frame, text=text, width=120, height=55, corner_radius=15,
                               fg_color="#8F693E", border_width=3, border_color="#765843",
                               text_color="#FFF6DD", font=("Helvetica", 11, "bold"),
                               command=cmd if cmd else None)
            b.grid(row=i//2, column=i%2, padx=8, pady=8)

    def setup_chat_ui(self):
        # We use a canvas + frame combo here to simulate a scrollable chat log
        self.chat_canvas = tk.Canvas(self.content_frame, bg="#EED594", highlightthickness=0)
        self.chat_canvas.pack(fill="both", expand=True, padx=10, pady=(10, 80))
        
        self.scroll_frame = tk.Frame(self.chat_canvas, bg="#EED594")
        self.chat_canvas.create_window((0,0), window=self.scroll_frame, anchor="nw", width=280)

        # Floating input field at the bottom using .place() for absolute positioning
        self.chat_entry = ctk.CTkEntry(self.content_frame, placeholder_text="What's on your mind?", 
                                       width=220, height=45, corner_radius=15, 
                                       fg_color="white", border_color="#765843", border_width=2)
        self.chat_entry.place(x=15, y=440)
        # Binding Return key so the user doesn't have to keep clicking the quack button
        self.chat_entry.bind("<Return>", lambda e: self.send_pulse_msg())

        self.enter_btn = tk.Button(self.content_frame, image=self.enter_img, bg="#EED594", 
                                   activebackground="#EED594", borderwidth=0, cursor="hand2",
                                   command=self.send_pulse_msg)
        self.enter_btn.place(x=242, y=440)

    def add_chat_bubble(self, text, is_bot=False):
        """Creates the chat message UI components."""
        bubble_frame = tk.Frame(self.scroll_frame, bg="#EED594")
        bubble_frame.pack(fill="x", pady=5)

        if is_bot:
            tk.Label(bubble_frame, image=self.bot_icon, bg="#EED594").pack(side="left", anchor="n", padx=5)
            
            # Simple hyperlink detection logic
            if "http" in text:
                lbl = tk.Label(bubble_frame, text=text, bg="white", fg="blue", cursor="hand2",
                               padx=10, pady=8, wraplength=180, justify="left", 
                               font=("Helvetica", 10, "underline"))
                try:
                    url = text.split("http")[-1].split()[0]
                    url = "http" + url
                    lbl.bind("<Button-1>", lambda e, u=url: webbrowser.open(u))
                except:
                    pass
            else:
                lbl = tk.Label(bubble_frame, text=text, bg="white", fg="#3E2723", padx=10, pady=8,
                               wraplength=180, justify="left", font=("Helvetica", 10))
            
            lbl.pack(side="left")
        else:
            lbl = tk.Label(bubble_frame, text=text, bg="white", fg="#3E2723", padx=10, pady=8,
                           wraplength=180, justify="right", font=("Helvetica", 10))
            lbl.pack(side="right", padx=10)

        # Force Tkinter to calculate the new height, then scroll to bottom automatically
        self.root.update_idletasks()
        self.chat_canvas.config(scrollregion=self.chat_canvas.bbox("all"))
        self.chat_canvas.yview_moveto(1.0)

    def send_pulse_msg(self):
        txt = self.chat_entry.get().strip()
        if not txt: return
        self.chat_entry.delete(0, tk.END)
        input_lower = txt.lower()

        # Keywords the chatbot will note down in order to know what steps to take next
        thanks_keywords = ["thank you", "thanks", "tysm", "thx", "okay thanks", "nice", "ok", "okay"]
        if any(key in input_lower for key in thanks_keywords):
            self.add_chat_bubble(txt, is_bot=False)

            # Once chat has been concluded, the app will go back to the main page in a few seconds after the parting message
            res = "You're very welcome! Quack! Take care of yourself. ✨"
            self.root.after(800, lambda: self.add_chat_bubble(res, is_bot=True))
            self.root.after(3000, self.show_frame_1)
            self.chat_state = "waiting_for_score"
            return

        # Simple state machine to keep track of where the conversation is
        if self.chat_state == "waiting_for_country":
            self.handle_country_response(txt)
        elif self.chat_state == "waiting_for_grounding":
            self.handle_grounding_response(txt)
        elif self.chat_state == "waiting_for_vent":
            self.handle_vent_response(txt)
        elif self.chat_state == "waiting_for_tool_choice":
            self.handle_tool_choice(txt)
        elif self.chat_state == "waiting_for_score":
            self.process_score_input(txt)

    def show_pulse_check(self):
        # Hide the landing page elements to make room for chat
        self.mascot.pack_forget()
        self.title_label.pack_forget()
        self.grid_frame.pack_forget()
        self.chat_state = "waiting_for_score"
        self.setup_chat_ui()
        self.add_chat_bubble("Quack! Let's do a quick pulse check. On a scale of 1 to 10.\n\n1 is feeling completely drained and 10 is feeling like you're on top of the world!", is_bot=True)

    # User answer will be evaluated. Each scale has an equivalent answer by the chatbot (depends on the severity of the situation)
    def process_score_input(self, txt):
        self.add_chat_bubble(txt, is_bot=False)
        try:
            score = int(txt)
            # Lowest score/highly vulnerable, user will type their country to reside in so that the chatbot can recommend them a hotline that'll help them further
            if 1 <= score <= 3:
                self.chat_state = "waiting_for_country" 
                res = "Quack... I'm concerned because you're feeling quite drained. I think you might need some instant support. ❤️"
                self.root.after(800, lambda: self.add_chat_bubble(res, is_bot=True))
                self.root.after(2000, lambda: self.add_chat_bubble("Which country do you currently reside in? I can find the right hotline for you.", is_bot=True))
            
            elif 4 <= score <= 5:
                res1 = "Quack! You're feeling a bit drained, but you're hanging in there. 🐥 Maybe some music can help you recharge?"
                self.root.after(800, lambda: self.add_chat_bubble(res1, is_bot=True))
                playlist_url = "https://open.spotify.com/playlist/5I59QZxSipVsZiQNBZCEMq?si=FZloI5Z_SoqTPFuA7TR3vg" 
                self.root.after(2300, lambda: self.add_chat_bubble(playlist_url, is_bot=True))
                res2 = "Let me know if that helps or if you need anything else! ❤️"
                self.root.after(3500, lambda: self.add_chat_bubble(res2, is_bot=True))
                self.chat_state = "waiting_for_grounding"

            elif 6 <= score <= 8:
                res1 = "Quack! You're doing alright, but you deserve a little breather. Why not step away from the screen for a bit? 🐥"
                self.root.after(800, lambda: self.add_chat_bubble(res1, is_bot=True))
                res2 = "Go for a short walk, grab a quick snack, or just have a glass of water. Your brain will thank you! 💧🍎"
                self.root.after(2300, lambda: self.add_chat_bubble(res2, is_bot=True))
                quote = "'Believe you can and you're halfway there.' - Theodore Roosevelt"
                res3 = f"Remember: {quote} ✨"
                self.root.after(3800, lambda: self.add_chat_bubble(res3, is_bot=True))
                self.chat_state = "waiting_for_grounding"
            
            elif 9 <= score <= 10:
                res1 = "QUACK!! You're absolutely crushing it today! That energy is infectious! 🚀✨"
                self.root.after(800, lambda: self.add_chat_bubble(res1, is_bot=True))
                res2 = "Since you're feeling so top-tier, now is the perfect time to tackle that one 'big' task you've been putting off. Go get 'em! 🐥"
                self.root.after(2300, lambda: self.add_chat_bubble(res2, is_bot=True))
                res3 = "Before you go, what's one thing that made you feel this awesome? Hold onto that feeling! ❤️"
                self.root.after(3800, lambda: self.add_chat_bubble(res3, is_bot=True))
                self.chat_state = "waiting_for_grounding"
            
            else:
                # In case user doesnt input a number or inputs a number below 1 and above 10
                res = "Quack? Please enter a number between 1 and 10!"
                self.root.after(800, lambda: self.add_chat_bubble(res, is_bot=True))
        except ValueError:
            # In case user inputs a text rather than a number in the conversation
            res = "I'm best at reading numbers 1-10 for this check. What's your score?"
            self.root.after(800, lambda: self.add_chat_bubble(res, is_bot=True))

    def handle_country_response(self, country_txt):
        self.add_chat_bubble(country_txt, is_bot=False)
        input_lower = country_txt.lower()
        # User keywords the chatbot has to look out for in order to know what to answer to them
        failure_keywords = ["it doesn't work", "it doesnt work", "its not working", "not working", "i cant"]
        isolation_keywords = ["im alone", "i am alone", "theres no one", "no"]
        
        if any(key in input_lower for key in failure_keywords):
            res = "Quack... I'm sorry that's not helping right now. Is there a friend, family member, or teacher you can talk to? ❤️"
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
        elif any(key in input_lower for key in isolation_keywords):
            res = "I hear you. Quack... are you having any trouble breathing at the moment? I'm right here with you. 🐥"
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
            self.chat_state = "waiting_for_grounding" 
        else:
            # The list of possible hotlines depending on where the user is from
            hotlines = {"uae": "800-4673 (HOPE)", "uk": "116 123", "usa": "988", "australia": "131114",
                        "india" : "888817666", "japan" : "110", "pakistan" : "115", "philippines" : "028969191"}
            hotline_info = hotlines.get(input_lower, "local emergency services")
            res = f"I've found a support line for you: {hotline_info}. Let me know if you can reach them! ❤️"
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
            self.chat_state = "waiting_for_grounding"

    def handle_grounding_response(self, txt):
        self.add_chat_bubble(txt, is_bot=False)
        input_lower = txt.lower()

        if "breathing" in input_lower:
            self.start_breathing_exercise()
            return 
        elif "journal" in input_lower or "prompt" in input_lower:
            self.send_journal_prompts()
            return 

        # Backup option in case the hotline doesnt work and the user needs immediate help
        rejection_keywords = ["no", "nope", "it doesnt work", "it doesn't work", "not helping", "i cant"]
        if any(key in input_lower for key in rejection_keywords):
            res = "I hear you. Quack. Sometimes we need a different approach. Would you like to try a quick 'Breathing Exercise' or perhaps some 'Journal Prompts' instead? 🐥"
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
            return

        res = "I'm glad to hear that. I'm right here if you need to talk again! ❤️"
        self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))

    # Chatbot automatically messages the user and instructs them proper breathing exercises to help stabilize them
    def start_breathing_exercise(self):
        # We use staggered .after() calls to create the pacing of a real exercise
        self.add_chat_bubble("Let's try to slow things down together. Focus on my words... 🐥", is_bot=True)
        self.root.after(3000, lambda: self.add_chat_bubble("Gently breathe in through your nose... 1... 2... 3... 4...", is_bot=True))
        self.root.after(7000, lambda: self.add_chat_bubble("Now hold it right there... 1... 2... 3... 4...", is_bot=True))
        self.root.after(11000, lambda: self.add_chat_bubble("And let it all out slowly through your mouth... 1... 2... 3... 4...", is_bot=True))
        self.root.after(15000, lambda: self.add_chat_bubble("How are you feeling now? Do you want to try again, or do you still feel a bit heavy? ❤️", is_bot=True))
        self.chat_state = "waiting_for_grounding"

    # In case user chooses the journal option
    def send_journal_prompts(self):
        opening = "Writing can be a powerful way to release what's inside. Here are a few prompts to get you started. Pick one that speaks to you: ✍️"
        prompts = (
            "• What is one thing you can control right now?\n"
            "• Describe your current feeling as a color or weather pattern.\n"
            "• What is a small thing that brought you peace today?\n"
            "• If your younger self saw you now, what would they be proud of?"
        )
        self.root.after(800, lambda: self.add_chat_bubble(opening, is_bot=True))
        self.root.after(2500, lambda: self.add_chat_bubble(prompts, is_bot=True))
        self.root.after(4000, lambda: self.add_chat_bubble("Whenever you're ready, feel free to start writing in your journal.\n\n You are stronger than you think, my friend. Quack!", is_bot=True))
        self.chat_state = "waiting_for_vent"

    def show_vent_space(self):
        self.mascot.pack_forget()
        self.title_label.pack_forget()
        self.grid_frame.pack_forget()
        self.chat_state = "waiting_for_vent"
        self.setup_chat_ui()
        self.add_chat_bubble("The floor is yours. Sometimes things feel lighter once they're written down. Whenever you're ready, tell me what's going on. 🐥", is_bot=True)

    def handle_vent_response(self, txt):
        self.add_chat_bubble(txt, is_bot=False)
        self.vent_count += 1
        low_txt = txt.lower()

        # If user suddenly starts mentioning triggering words that are signs of crisis, the chatbot immediately asks users for their location to provide hotlines
        crisis_keywords = ["die", "exist", "giving up", "give up", "not enough", "survive", "end it"]
        if any(key in low_txt for key in crisis_keywords):
            res = "Quack... I'm really concerned hearing that. You don't have to carry this alone. ❤️"
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
            self.root.after(2500, lambda: self.add_chat_bubble("Would you like me to find a support hotline for you? Just let me know which country you are in.", is_bot=True))
            self.chat_state = "waiting_for_country"
            return

        # Vent counter logic - nudge them back to a pulse check after a while
        if self.vent_count >= 5:
            res = "Thank you for sharing all of that with me. Quack! Now that you've let it out, let's do a quick pulse check."
            self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
            self.vent_count = 0 
            self.root.after(2500, lambda: self.add_chat_bubble("On a scale of 1 to 10, how are you feeling now?", is_bot=True))
            self.chat_state = "waiting_for_score" 
            return 

        if any(word in low_txt for word in ["tired", "exhausted", "burnout"]):
            res = "It sounds like you're carrying a lot. Please remember that resting isn't quitting; it's recharging. ☁️"
        elif any(word in low_txt for word in ["sad", "lonely", "hurt", "bad"]):
            res = "I'm so sorry you're feeling this way. It's okay to not be okay. I'm right here with you. ❤️"
        elif len(txt) > 50: 
            res = "Thank you for trusting me with that. Just getting it out of your head is a huge win. How do you feel now?"
        else:
            res = "I hear you. Thank you for sharing that with me. Is there anything else you want to get off your chest? 🐥"

        self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
        self.chat_state = "waiting_for_grounding"

    def show_mindful_tools(self):
        self.mascot.pack_forget()
        self.title_label.pack_forget()
        self.grid_frame.pack_forget()
        self.chat_state = "waiting_for_tool_choice"
        self.setup_chat_ui()
        opening = "Quack! Everyone has their own way of finding peace. Which of these would you like to explore?\n\n• Music\n• Self-help books\n• Podcasts\n• YouTube videos"
        self.add_chat_bubble(opening, is_bot=True)

    def handle_tool_choice(self, txt):
        self.add_chat_bubble(txt, is_bot=False)
        choice = txt.lower()
        res, link_msg = "", ""

        if "music" in choice:
            res = "Music is a great choice! I'd recommend some Lofi tracks to help you reset. 🎵"
            link_msg = "Here is a 2hr Lofi music you might like: https://www.youtube.com/watch?v=H0RjEffHzt8"
        elif "book" in choice:
            res = "I suggest 'The Things You Can See Only When You Slow Down'. 📖"
            link_msg = "https://www.goodreads.com/book/show/30780006-the-things-you-can-see-only-when-you-slow-down"
        elif "podcast" in choice:
            res = "Check out this playlist filled with self-help related podcasts! 🎧"
            link_msg = "Listen here on Spotify: https://open.spotify.com/playlist/2HvBlj5w3ZKNulkBAMcOn0?si=J23yW5b9SOKqgNs2VxHLzw"
        elif "youtube" in choice or "video" in choice:
            res = "A YouTube channel that has helped Quackity when he was struggling. 📺"
            link_msg = "This one is my favorite: https://www.youtube.com/@thezurkieshow"
        else:
            res = "Quack? I'm not sure about that. Try picking: Music, Books, Podcasts, or Videos! 🐥"

        self.root.after(1000, lambda: self.add_chat_bubble(res, is_bot=True))
        if link_msg:
            self.root.after(2500, lambda: self.add_chat_bubble(link_msg, is_bot=True))
        self.chat_state = "waiting_for_grounding"

    def show_instant_support(self):
        self.mascot.pack_forget()
        self.title_label.pack_forget()
        self.grid_frame.pack_forget()
        self.chat_state = "waiting_for_country"
        self.setup_chat_ui()
        self.add_chat_bubble("Quack! Please remember that you aren't alone. There are numerous hotlines all over the world to help you. ❤️", is_bot=True)
        self.root.after(1500, lambda: self.add_chat_bubble("Could you tell me which country you are in right now? 🐥", is_bot=True))

if __name__ == "__main__":
    # Standard boilerplate for starting the app loop
    root = tk.Tk()
    app = QuackityApp(root)
    root.mainloop()