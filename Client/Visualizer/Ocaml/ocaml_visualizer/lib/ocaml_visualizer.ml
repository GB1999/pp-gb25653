(* ocaml_visualizer.ml *)
open Yojson.Basic.Util

type node = {
  name: string;
  age: int;
}

type edge = {
  from_id: string;
  to_id: string;
}

type graph = {
  nodes: (string, node) Hashtbl.t;
  edges: (string, edge) Hashtbl.t;
}

let load_json_file file_name =
  let json = Yojson.Basic.from_file file_name in
  let graph_json = member "Graph" json in
  let nodes_json = member "nodes" graph_json |> to_assoc in
  let edges_json = member "edges" graph_json |> to_assoc in
  let nodes = Hashtbl.create 100 in
  let edges = Hashtbl.create 100 in

  let parse_node node_json =
    let name = member "name" node_json |> to_string in
    let age = member "age" node_json |> to_int in
    { name; age }
  in

  let parse_edge edge_json =
    let from_id = member "from" edge_json |> to_string in
    let to_id = member "to" edge_json |> to_string in
    { from_id; to_id }
  in

  let () =
    List.iter (fun (id, node_json) ->
        let node = parse_node node_json in
        Hashtbl.add nodes id node
      ) nodes_json;
    List.iter (fun (id, edge_json) ->
        let edge = parse_edge edge_json in
        Hashtbl.add edges id edge
      ) edges_json
  in

  { nodes; edges }

let print_table graph =
Printf.printf "+-----------------+-----+--------------------------------+\n";
Printf.printf "|      Name       | Age |            Friends             |\n";
Printf.printf "+-----------------+-----+--------------------------------+\n";
Hashtbl.iter (fun id node ->
    let friends = Hashtbl.fold (fun _ edge acc ->
        if edge.from_id = id then
          let to_node = Hashtbl.find_opt graph.nodes edge.to_id in
          match to_node with
          | Some n -> n.name :: acc
          | None -> acc
        else
          acc
      ) graph.edges [] in
    Printf.printf "| %-15s | %-3d | %-30s |\n" node.name node.age (String.concat ", " friends);
  ) graph.nodes;
Printf.printf "+-----------------+-----+--------------------------------+\n"

let pretty_print_table graph =
  let max_name_length = ref 0 in
  let max_age_length = ref 0 in

  Hashtbl.iter (fun _ node ->
      max_name_length := max !max_name_length (String.length node.name);
      max_age_length := max !max_age_length (String.length (string_of_int node.age))
    ) graph.nodes;

  let column_widths = (!max_name_length + 2, !max_age_length + 2) in

  Printf.printf "+%s+%s+%s+\n"
    (String.make (fst column_widths + 2) '-')
    (String.make (snd column_widths + 2) '-')
    (String.make 40 '-');
  Printf.printf "| %-*s | %-*s | %-*s |\n" (fst column_widths) "Name" (snd column_widths) "Age" 40 "Friends";
  Printf.printf "+%s+%s+%s+\n"
    (String.make (fst column_widths + 2) '-')
    (String.make (snd column_widths + 2) '-')
    (String.make 40 '-');

  Hashtbl.iter (fun id node ->
      let friends = Hashtbl.fold (fun _ edge acc ->
          if edge.from_id = id then
            let to_node = Hashtbl.find_opt graph.nodes edge.to_id in
            match to_node with
            | Some n -> n.name :: acc
            | None -> acc
          else
            acc
        ) graph.edges [] in

      let name_lines = String.split_on_char ' ' node.name in
      let name_lines = List.fold_left (fun (lines, current_line) word ->
          let line = current_line ^ " " ^ word in
          if String.length line <= fst column_widths then
            (lines, line)
          else
            (current_line :: lines, word)
        ) ([], List.hd name_lines) (List.tl name_lines) in

      let name_lines = List.rev_append [node.name] (fst name_lines) in
      let name_lines = List.map (fun line -> Printf.sprintf "| %-*s | %-*d | %-40s |" (fst column_widths) line (snd column_widths) node.age (String.concat ", " friends)) name_lines in

      match name_lines with
      | [] -> ()
      | [line] ->
        Printf.printf "%s\n" line;
        Printf.printf "+%s+%s+%s+\n"
          (String.make (fst column_widths + 2) '-')
          (String.make (snd column_widths + 2) '-')
          (String.make 40 '-')
      | line :: rest ->
        Printf.printf "%s\n" line;
        List.iter (fun line -> Printf.printf "%s |\n" line) rest;
        Printf.printf "+%s+%s+%s+\n"
          (String.make (fst column_widths + 2) '-')
          (String.make (snd column_widths + 2) '-')
          (String.make 40 '-')
    ) graph.nodes

