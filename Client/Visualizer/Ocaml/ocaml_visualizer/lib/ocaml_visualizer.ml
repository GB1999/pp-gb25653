(* ocaml_visualizer.ml *)
open Yojson.Basic.Util

(* define types for graph *)
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

(* load json from graph.json file using YoJson *)
let load_json_file file_name =
  let json = Yojson.Basic.from_file file_name in
  (* extract graph from json *)
  let graph_json = member "Graph" json in
  (* extract nodes/edges from graph_json and pipe the extracted JSON data to the to_assoc function. *)
  (* to store them as a association list *)
  let nodes_json = member "nodes" graph_json |> to_assoc in
  let edges_json = member "edges" graph_json |> to_assoc in
  let nodes = Hashtbl.create 100 in
  let edges = Hashtbl.create 100 in

  (* define parse_node function to parse individual node_json to records *)
  let parse_node node_json =
    let name = member "name" node_json |> to_string in
    let age = member "age" node_json |> to_int in
    { name; age }
  in

  (* define parse_edge function to parse individual edge_json to records *)
  let parse_edge edge_json =
    let from_id = member "from" edge_json |> to_string in
    let to_id = member "to" edge_json |> to_string in
    { from_id; to_id }
  in

  (* iterate through the nodes_json and convert each node to a record *)
  (* store each record with its associated id the nodes hashtbl *)
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

(* Define visualizer function *)
let print_table graph =
  (* Print column headings *)
  Printf.printf "+-----------------+-----+------------------------+\n";
  Printf.printf "|      Name       | Age |       Friends          |\n";
  Printf.printf "+-----------------+-----+------------------------+\n";
  (* Initialize variables for calculating the average age *)
  let total_age = ref 0 in
  let total_nodes = ref 0 in
  (* Iterate over each node and apply an anonymous function *)
  Hashtbl.iter (fun id node ->
      (* Initialize variables to hold the current node's friends' ages *)
      let friend_ages = ref [] in
      (* Iterate over edges, ignoring key value *)
      let friends = Hashtbl.fold (fun _ edge acc ->
          (* Check if edge.from_id is the same as the current node id *)
          if edge.from_id = id then
            (* If so, find the corresponding node for edge.to_id *)
            let to_node = Hashtbl.find_opt graph.nodes edge.to_id in
            match to_node with
            (* If to_node is Some node n, add name to friends accumulator list *)
            | Some n ->
              (* Update the friend's age list *)
              friend_ages := n.age :: !friend_ages;
              n.name :: acc
            | None -> acc
          else
            acc
        ) graph.edges [] in
      (* Update the total age and total number of nodes *)
      total_age := !total_age + node.age;
      total_nodes := !total_nodes + 1;
      (* Print formatted string of the given node's name, age, and friends (as comma-separated list) *)
      Printf.printf "| %-30s | %-3d | %-80s |\n" node.name node.age (String.concat ", " friends);
    ) graph.nodes;
  (* Calculate and print the overall average age *)
  let overall_average_age =
    if !total_nodes = 0 then 0
    else !total_age / !total_nodes
  in
  Printf.printf "+-----------------+-----+------------------------+\n";
  Printf.printf "| Overall Average |     |                        |\n";
  Printf.printf "|       Age       | %-3d |                        |\n" overall_average_age;
  Printf.printf "+-----------------+-----+------------------------+\n"
