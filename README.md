📌 Overview
This project was developed as the final submission for Programming Paradigm at The University of Texas at Austin. It explores the intersection of language design, parsing, and query optimization through the implementation of a Cypher query processing toolchain. The system includes a lexer/parser, benchmarking suite, and a lightweight user interface.

🎯 Purpose and Learning Goals
The primary goal of this project was to apply principles from the course—including functional, object-oriented, and declarative programming paradigms—to a real-world use case involving:

Language processing using parser generators and Go

Programmatic query analysis with custom lexer/parser for Cypher

Benchmark-driven evaluation of query patterns and performance

Separation of concerns across modular client components (parser, benchmarking tools, UI)

This project emphasizes modular design, practical use of external tools (ANTLR), and the ability to extend language tooling for domain-specific applications like graph databases.

🧱 Project Structure
bash
Copy
Edit
Client/
├── Benchmark/        # Scripts for generating and testing Cypher query performance
├── Cache/            # Supporting libraries (e.g. H2 JARs)
├── LexerParser/      # Cypher grammar parser written in Go using ANTLR
└── UI/               # Early-stage interface and supporting UX files
⚙️ Technologies & Paradigms
Go (Golang) – Chosen for its concurrency model and functional idioms

ANTLR – Used to define and generate the Cypher grammar parser

Shell Scripting – For automating benchmarks and task execution

Cypher – Graph query language, used as the testbed for parsing and analysis

🚀 Running the Project
To explore the components:

Lexer/Parser

Navigate to Client/LexerParser/

Run: go run main.go (ensure Go and ANTLR are properly installed)

Benchmarking

Navigate to Client/Benchmark/

Use query_benchmark.sh to run performance tests on generated queries

⚠️ Note: This project was built and tested in a local environment—some paths or dependencies may need configuration for other systems.

🧠 Reflections
This project allowed us to synthesize course concepts through the lens of a domain-specific toolchain. It involved functional parsing logic, concurrency principles in Go, and real-world applications of declarative query languages.
