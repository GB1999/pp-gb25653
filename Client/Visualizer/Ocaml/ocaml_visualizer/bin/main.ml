open Ocaml_visualizer
(* create instance of graph using load_json and print it using print_table*)
let () =
  let file_name = "../../graph.json" in
  let graph = load_json_file file_name in
  print_table graph
