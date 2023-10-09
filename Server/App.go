package main

import (
	"context"

	"github.com/neo4j/neo4j-go-driver/v5/neo4j"
)

type App struct {
	NeoDriver neo4j.DriverWithContext
	Context   context.Context
}