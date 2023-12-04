package test

import (
	"Server/GoServer/api"
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSubmitQueryHandler(t *testing.T) {
	// Create a new instance of the server with a mock Neo4j driver
	server := api.NewServer("neo4j://localhost:7687", "neo4j", "NewSchool2308!")

	// Create a test HTTP request
	requestBody := []byte(`{
		"query": "MATCH (n) RETURN n",
		"isWrite": false,
		"parameters": {"param1": "value1"}
	}`)

	req, err := http.NewRequest("POST", "/query", bytes.NewBuffer(requestBody))
	if err != nil {
		t.Fatal(err)
	}

	// Create a test HTTP response recorder
	rr := httptest.NewRecorder()

	// Call the submitQuery handler
	server.ServeHTTP(rr, req)

	// Check the response status code
	if rr.Code != http.StatusOK {
		t.Errorf("Expected status code %d, got %d", http.StatusOK, rr.Code)
	}

	// Parse the response JSON
	var response []byte
	if err := json.NewDecoder(rr.Body).Decode(&response); err != nil {
		t.Errorf("Failed to decode response JSON: %v", err)
	}

	// Perform additional assertions on the response data if needed
}
