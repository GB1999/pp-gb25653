package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

// Struct for JSON request
type Neo4jRequest struct {
	Query      string            `json:"query"`
	IsWrite    bool              `json:"isWrite"`
	Parameters map[string]string `json:"parameters"`
}

type JsonNotification struct {
	Code        string `json:"code"`
	Title       string `json:"title"`
	Description string `json:"description"`
}

// Function to convert notifications
func convertNotifications(notifications []neo4j.Notification) ([]JsonNotification, error) {
	var jsonNotifications []JsonNotification
	for _, n := range notifications {
		jsonNotif := JsonNotification{
			Code:        n.Code(),
			Title:       n.Title(),
			Description: n.Description(),
		}
		jsonNotifications = append(jsonNotifications, jsonNotif)
	}
	return jsonNotifications, nil
}

// Function to execute query using driver
func executeQuery(driver neo4j.DriverWithContext, request Neo4jRequest) ([]byte, error) {
	params := make(map[string]any)

	// convert request parameters to map
	for k, v := range request.Parameters {
		params[k] = v
	}

	result, err := neo4j.ExecuteQuery(context.Background(), driver, request.Query, params, neo4j.EagerResultTransformer, neo4j.ExecuteQueryWithDatabase("neo4j"))
	if err != nil {
		return nil, err
	}

	var jsonData []byte
	// if request is a write query, recursively call execute query
	// to return updated graph instead of null
	if request.IsWrite {
		readRequest := Neo4jRequest{"MATCH (n) OPTIONAL MATCH (n)-[r]-(m) RETURN n, r, m", false, request.Parameters}
		jsonData, err = executeQuery(driver, readRequest)
	} else {
		jsonData, err = json.Marshal(result.Records)
	}

	return jsonData, err
}

// Main function
func main() {
	driver, err := neo4j.NewDriverWithContext("neo4j://localhost:7687", neo4j.BasicAuth("neo4j", "NewSchool2308!", ""))
	if err != nil {
		log.Fatal(err)
	}
	defer driver.Close(context.Background())

	// create query endpoint for client and handle logic
	http.HandleFunc("/query", func(w http.ResponseWriter, r *http.Request) {
		var request Neo4jRequest

		// decode request body json to Neo4jRequest object (request)
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		// execute the query using neo4j driver and Neo4j request
		// record json response and any errors that occur
		jsonData, err := executeQuery(driver, request)
		if err != nil {
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}

		// write json response
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	})

	log.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
