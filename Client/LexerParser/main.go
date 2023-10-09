// example1.go
package main

import (
	"Project/Client/parser"
	"os"

	"github.com/antlr/antlr4/runtime/Go/antlr"
)

func main() {
	var query string
	// Setup the input
	for _, arg := range os.Args[1:] {
		query += arg
	}

	is := antlr.NewInputStream(query)

	// Create the Lexer
	lexer := parser.NewCypherLexer(is)
	stream := antlr.NewCommonTokenStream(lexer, antlr.TokenDefaultChannel)
	cypherParser := parser.NewCypherParser(stream)

	antlr.ParseTreeWalkerDefault.Walk(&parser.BaseCypherListener{}, cypherParser.OC_Cypher())
}
