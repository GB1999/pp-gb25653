(* test_my_module.ml *)
open Alcotest
open Ocaml_visualizer

let () =
  let file_name = "test_graph.json" in 
  let graph = load_json_file file_name in

  let node_test () =
    let num_entries = Hashtbl.length graph.nodes in
    check int "Check Number of Nodes"  num_entries 10
  in

  let edge_test () =
    let num_entries = Hashtbl.length graph.edges in
    check int "Check Number of Edges"  num_entries 27
  in

  let suite =
    [ "Check Graph Nodes", `Quick, node_test;
      "Check Graph Edges", `Quick, edge_test
    ]
  in

  run "My Module Tests" ["Graph", suite]
