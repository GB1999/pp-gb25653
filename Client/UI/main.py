import tkinter
import tkinter.messagebox
import customtkinter
import os
import subprocess
from cache_handler import CacheHandler
import requests
import json

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.cache_hander = CacheHandler()
        self.cache_hander.connect(user="sa", password="",
                                  jar_dir="/Users/gagebenham/Documents/ECE-382V/Project/Client/Cache/h2-1.4.200.jar")

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
        self.entry.bind('<Return>', command=self.submit_query)

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text="Submit")
        self.main_button_1.grid(row=3, column=3, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.main_button_1.bind(sequence="<Button-1>", command=self.submit_query)

        # create textbox
        self.response_label = customtkinter.CTkLabel(self, text="Response",font=customtkinter.CTkFont(size=16, weight="bold"))
        self.response_label.grid(row=0, column=1, padx=20, pady=(20, 10), sticky="w")

        self.textbox = customtkinter.CTkTextbox(self, width=250)
        self.textbox.grid(row=1, column=1, padx=(20, 0), pady=(20, 20), sticky="nsew", columnspan=3)
        self.textbox.tag_config("error", foreground="red")
        self.textbox.tag_config("success", foreground="green")

        # set default values
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")
        self.textbox.insert("0.0",  "Enter a query for the Cypher\n\n" )





    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def submit_query(self, _):
        query = self.user_input.get()
        output = subprocess.run(["/Users/gagebenham/Documents/ECE-382V/Project/Client/LexerParser/main", query], capture_output=True, text=True)
        if (output.stderr):
            self.textbox.insert("0.0", output.stderr,tags=["error"])
        else:
            if (self.check_cache("success")):
                try:
                    response = self.send_neo4j_query("{0}".format(query))
                    # Check if the request was successful (status code 200)
                    if response.status_code == 200:
                        # Parse the response content as needed
                        result = response.text
                        tag = "success"
                    else:
                        result = f"HTTP Error {response.status_code}: {response.text}"
                        tag = "error"



                except Exception as e:
                    result = (f"An error occurred: {str(e)}")
                    tag = "error"

                self.textbox.insert("0.0", f"{result}\n", tags=[tag])



    def check_cache(self, response):
        # self.cache_hander.ch.execute("")
        return True

    def send_neo4j_query(self, neo4j_query):
            # Create a dictionary with the neo4j query as the payload
            payload = {"query": neo4j_query}
            json_data = json.dumps(payload)

            # Send an HTTP POST request to the specified URL
            response = requests.post("http://localhost:8080/query", data=json_data)

            return response



    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()


