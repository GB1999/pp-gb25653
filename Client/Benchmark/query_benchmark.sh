#!/bin/bash

# Run the Python script
echo "Running the Python script"

# Python Environment
"/home/ubuntu/anaconda3/envs/UI/bin/python3"

# File containing the queries
QUERY_FILE="generated_queries.txt"

# Python script to execute queries
PYTHON_SCRIPT="/home/ubuntu/Documents/pp-gb25653/Client/UI/client_ui_benchmark/cypher_query_benchmark.py"

# Check if the query file exists
if [ ! -f "$QUERY_FILE" ]; then
    echo "Query file does not exist."
    exit 1
fi

# Initialize variables for timing
total_time=0
count=0

# Process each query
while IFS= read -r query
do
    # Measure the time for each query
    start_time=$(date +%s.%N)
    
    # Send query to the Python script
    echo "$query" | $PYTHON_ENVIRONMENT $PYTHON_SCRIPT
    
    end_time=$(date +%s.%N)
    
    # Calculate time taken for this query
    query_time=$(echo "$end_time - $start_time" | bc)
    total_time=$(echo "$total_time + $query_time" | bc)
    
    count=$((count+1))

    # Optional: Display time for each query
    echo "Query $count time: $query_time seconds"
done < "$QUERY_FILE"

# Calculate average time per query
if [ $count -gt 0 ]; then
    avg_time=$(echo "$total_time / $count" | bc -l)
    echo "Total time for $count queries: $total_time seconds"
    echo "Average time per query: $avg_time seconds"
else
    echo "No queries were processed."
fi
