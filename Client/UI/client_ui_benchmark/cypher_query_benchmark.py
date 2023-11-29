#!/Users/gagebenham/anaconda3/envs/Programming_Paradigms_Client_UI/bin python3
import sys
from pathlib import Path

# Get the absolute path to the directory where the script is located
current_dir = Path(__file__).resolve().parent

# Add the parent directory of 'client_ui_components' to sys.path
sys.path.append(str(current_dir.parent))

# Now you can import your module
from client_ui_components import QueryHandler



query_handler = QueryHandler(
        update_ui_callback=(()),  # Replace with your UI callback function
        h2_path="../../../Client/Cache/h2-1.4.200.jar",
        lexer_parser_path = "../../../Client/LexerParser/main"
    )

# clear the existing data
query_handler.clear_neo4j_graph()
query_arg = sys.argv[1]
query_handler.submit_query(query_arg)

for line in sys.stdin:
    print(query_handler.get_last_query_result())

