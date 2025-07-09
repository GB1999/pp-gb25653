
```markdown
## 🎓 Final Project – Programming Paradigms  
**CS 345 – The University of Texas at Austin**

---

## 📌 Overview

This repository contains the final project for **Programming Paradigms (CS 345)** at The University of Texas at Austin. The project centers on building a modular toolchain for processing and evaluating **Cypher queries**, the graph query language used in systems like Neo4j.

Through this project, we explored a combination of programming paradigms—including declarative, functional, and object-oriented approaches—by implementing:

- A custom lexer and parser for Cypher using **ANTLR** and **Go**
- A benchmarking suite for performance evaluation of generated queries
- A foundational UI layer for navigating query sets or results

---

## 🎯 Purpose and Learning Goals

The project demonstrates how core principles from the course can be applied to:

- **Language parsing and generation**  
- **Query optimization and benchmarking**  
- **Concurrency and modular design in Go**  
- **Tooling for domain-specific languages**

It serves as a practical application of multiple paradigms, showing how compiler concepts and evaluation logic can be adapted to real-world graph querying problems.

---

## 🧱 Project Structure

```

Client/
├── Benchmark/        # Scripts for generating and evaluating Cypher query performance
├── Cache/            # Dependency jars, including H2 database
├── LexerParser/      # Go-based Cypher grammar parser using ANTLR
└── UI/               # Prototype user interface and related files

````

---

## ⚙️ Technologies & Paradigms

- **Go (Golang)** – Emphasizing concurrency and procedural control
- **ANTLR** – Parser generation from formal grammar definitions
- **Cypher** – Declarative graph query language
- **Shell Scripting** – Automating benchmark routines

---

## 🚀 Getting Started

### 1. Lexer/Parser

```bash
cd Client/LexerParser/
go run main.go
````

> Ensure [Go](https://golang.org/dl/) and [ANTLR](https://www.antlr.org/) are installed.

### 2. Benchmarking

```bash
cd Client/Benchmark/
./query_benchmark.sh
```

> Dependencies such as `requirements.txt` are included for reproducibility.

---

## 🧠 Reflections

This project provided an opportunity to explore language design, parsing strategies, and runtime performance in the context of graph databases. It reinforced course concepts through practical implementation and helped demonstrate the value of combining different paradigms for building robust, extensible systems.

---

## 📁 Notes

* Some paths may require editing based on your local machine.
* `.DS_Store` files can be ignored or deleted on non-macOS systems.
* Future extensions might include a query visualizer or Neo4j integration.


