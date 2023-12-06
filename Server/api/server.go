package api

import (
	"context"
	"encoding/json"
	"net/http"
	"fmt"
	"github.com/gorilla/mux"
	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

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

type Server struct {
	*mux.Router
	driver neo4j.DriverWithContext
}

func NewServer(url string, userName string, password string) *Server {
	driver, err := neo4j.NewDriverWithContext(url, neo4j.BasicAuth(userName, password, ""))
	if err != nil {
		panic(err)
	} else {
		s := &Server{
			Router: mux.NewRouter(),
			driver: driver,
		}
		s.routes()
		return s
	}

}

func (s *Server) routes() {
	s.HandleFunc("/query", s.submitQuery()).Methods("POST")
}

func (s *Server) submitQuery() http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var request Neo4jRequest
		
		// decode request body json to Neo4jRequest object (request)
		if err := json.NewDecoder(r.Body).Decode(&request); err != nil {
			http.Error(w, err.Error(), http.StatusBadRequest)
			return
		}

		fmt.Printf("Recieved %v\n", fmt.Sprint(request.Parameters))
		
		// execute the query using the provided neo4j driver and Neo4j request
		// record json response and any errors that occur
		jsonData, err := executeQuery(s.driver, request)
		if err != nil {
			fmt.Printf("Encountered Error: %v\n", fmt.Sprint(err.Error()))
			http.Error(w, err.Error(), http.StatusInternalServerError)
			return
		}
		fmt.Printf(string(jsonData))

		// write json response
		w.Header().Set("Content-Type", "application/json")
		w.Write(jsonData)
	}
}

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
