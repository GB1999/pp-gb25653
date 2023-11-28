open Ocaml_visualizer
let () =
  let file_name = "../../graph.json" in
  let graph = load_json_file file_name in
  print_table graph
