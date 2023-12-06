package main

import (
	"Server/GoServer/api"
	"log"
	"net/http"
)

func main() {
	log.Println("Server starting on port 8080...")

	server := api.NewServer("neo4j://localhost:7687", "neo4j", "neo4j_pass")
	err := http.ListenAndServe(":8080", server)
	if err != nil {
		panic(err)
	}
}
