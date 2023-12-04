import tkinter
import tkinter.messagebox
import customtkinter
from .query_handler import QueryHandler

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

class App(customtkinter.CTk):
    def __init__(self, lexer_parser_path, h2_path):
        super().__init__()
        #set callback in query handler to update ui
        self.query_handler = QueryHandler(self.update_textbox, lexer_parser_path=lexer_parser_path, h2_path=h2_path)

        # configure window
        self.title("CustomTkinter complex_example.py")
        self.geometry(f"{1100}x{580}")
        self.user_input = tkinter.StringVar()
        self.response_text = tkinter.StringVar()

        # configure grid layout (4x4)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure((2, 3), weight=0)
        self.grid_rowconfigure((0, 1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, columnspan=4, sticky="nsew")
        self.sidebar_frame.grid_columnconfigure(4, weight=1)

        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Cypher Client", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=0, column=5, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=0, column=6, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=0, column=7, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=0, column=8, padx=20, pady=(10, 20))

        # create main entry and button
        self.entry = customtkinter.CTkEntry(self, textvariable=self.user_input, placeholder_text="Enter a query")
        self.entry.grid(row=3, column=1, columnspan=2, padx=(20, 0), pady=(20, 20), sticky="nsew")
        self.entry.bind('<Return>', self.on_submit)

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.bind("<Button-1>", self.on_submit)

        self.clear_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Clear Database")
        self.clear_button.grid(row=1, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.clear_button.bind("<Button-1>", self.on_clear)

        self.refresh_button = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2,
                                                    text_color=("gray10", "#DCE4EE"), text="Refresh")
        self.refresh_button.grid(row=2, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.refresh_button.bind("<Button-1>", self.on_refresh)

        # create textbox
        self.response_label = customtkinter.CTkLabel(self, text="Response",font=customtkinter.CTkFont(size=16, weight="bold"))
        self.response_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="w")

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew", columnspan=3)
        self.textbox.tag_config("error", foreground="red")
        self.textbox.tag_config("cached", underline=True)
        self.textbox.tag_config("success", foreground="green")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0",  "Enter a query for the Cypher\n\n" )

    def update_textbox(self, index, text, tags):
        self.textbox.insert(index, text, tags)

    def on_submit(self, event):
        query = self.user_input.get()
        print("QUERY" + str(query))
        self.query_handler.submit_query(query)

    def on_clear(self, event):
        self.query_handler.clear_neo4j_graph()

    def on_refresh(self, event):
        self.query_handler.submit_query("MATCH (n) OPTIONAL MATCH (n)-[r]-(m) RETURN n, r, m")

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")