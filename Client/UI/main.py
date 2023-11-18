from app import App
from query_handler import QueryHandler
from h2_cache import H2Cache

if __name__ == "__main__":
    h2_path = "/Users/gagebenham/Documents/ECE-382V/Project/Client/Cache/h2-1.4.200.jar"
    parser_path = "/Users/gagebenham/Documents/ECE-382V/Project/Client/LexerParser/main"
    app = App(lexer_parser_path=parser_path, h2_path=h2_path)
    app.mainloop()


