package main

import (
	"context"
	"encoding/json"
	"log"
	"net/http"
	"strings"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

// Struct for JSON request
type Neo4jRequest struct {
	Query      string            `json:"query"`
	Parameters map[string]string `json:"parameters"`
}

type JsonNotification struct {
	// Define fields based on what you need from neo4j.Notification
	// For example:
	Code        string `json:"code"`
	Title       string `json:"title"`
	Description string `json:"description"`
	// Add other fields as required
}

func convertNotifications(notifications []neo4j.Notification) ([]JsonNotification, error) {
	var jsonNotifications []JsonNotification

	for _, n := range notifications {
		// Create an instance of JsonNotification and fill it with data from the notification
		// This is where you extract the fields you need from each neo4j.Notification
		jsonNotif := JsonNotification{
			Code:        n.Code(),
			Title:       n.Title(),
			Description: n.Description(),
		}
		jsonNotifications = append(jsonNotifications, jsonNotif)
	}

	return jsonNotifications, nil
}

// Function to execute read query and return nodes as JSON
func executeReadQuery(session neo4j.SessionWithContext, request Neo4jRequest) ([]byte, error) {
	// Convert parameters to map[string]any
	params := make(map[string]any)
	for k, v := range request.Parameters {
		params[k] = v
	}

	nodes, err := session.ExecuteRead(context.Background(),
		func(tx neo4j.ManagedTransaction) (any, error) {
			result, err := tx.Run(context.Background(), request.Query, params)
			if err != nil {
				return nil, err
			}
			records, err := result.Collect(context.Background())
			if err != nil {
				return nil, err
			}
			return records, nil
		})
	if err != nil {
		return nil, err
	}

	// Convert the results to JSON
	jsonData, err := json.Marshal(nodes)
	if err != nil {
		return nil, err
	}

	return jsonData, nil
}

// Function to execute write query and return result summary
func executeWriteQuery(session neo4j.SessionWithContext, request Neo4jRequest) (neo4j.ResultSummary, error) {
	// Convert parameters to map[string]any
	params := make(map[string]any)
	for k, v := range request.Parameters {
		params[k] = v
	}

	var summary neo4j.ResultSummary
	_, err := session.ExecuteWrite(context.Background(),
		func(tx neo4j.ManagedTransaction) (any, error) {
			result, err := tx.Run(context.Background(), request.Query, params)
			if err != nil {
				return nil, err
			}
			summary, err = result.Consume(context.Background())
			if err != nil {
				return nil, err
			}
			return summary, nil
		})

	return summary, err
}

// Helper function to detect write queries (CREATE, MERGE, DELETE, etc.)
func isWriteQuery(query string) bool {
	writeKeywords := []string{"CREATE", "MERGE", "SET", "DELETE", "REMOVE", "DETACH DELETE", "CALL"}
	for _, keyword := range writeKeywords {
		if strings.Contains(strings.ToUpper(query), keyword) {
			return true
		}
	}
	return false
}

// Main function
func main() {
	// Connect to Neo4j
	driver, err := neo4j.NewDriverWithContext("neo4j://localhost:7687", neo4j.BasicAuth("neo4j", "NewSchool2308!", ""))
	if err != nil {
		log.Fatal(err)
	}
	defer driver.Close(context.Background())

	// Create a session
	session := driver.NewSession(context.Background(), neo4j.SessionConfig{DatabaseName: "neo4j"})
	defer session.Close(context.Background())

	// Start HTTP server and handle requests
	http.HandleFunc("/query", func(w http.ResponseWriter, r *http.Request) {
		var request Neo4jRequest
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		// Call appropriate function based on the type of query
		if isWriteQuery(request.Query) {
			summary, err := executeWriteQuery(session, request)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			notifs, _ := convertNotifications(summary.Notifications())
			json.NewEncoder(w).Encode(notifs)

		} else {
			jsonData, err := executeReadQuery(session, request)
			if err != nil {
				http.Error(w, err.Error(), http.StatusInternalServerError)
				return
			}
			// Return nodes as JSON
			w.Header().Set("Content-Type", "application/json")
			w.Write(jsonData)
		}
	})

	log.Println("Server starting on port 8080...")
	log.Fatal(http.ListenAndServe(":8080", nil))
}
