from client_ui_components import App
import os.path as path

if __name__ == "__main__":
    h2_path = "../../Client/Cache/h2-1.4.200.jar"
    parser_path = "../../Client/LexerParser/main"
    app = App(lexer_parser_path=parser_path, h2_path=h2_path)
    app.mainloop()


