import pytest
from faker import Faker
from client_ui_components import QueryHandler  # Replace with actual module name
import random
@pytest.fixture
def query_handler():
    return QueryHandler(
        update_ui_callback=(mock_callback),  # Replace with your UI callback function
        h2_path="../../../Client/Cache/h2-1.4.200.jar",
        lexer_parser_path = "../../../Client/LexerParser/main"
    )

def write_query_to_file(query, file_path='generated_queries.txt'):
    with open(file_path, 'a') as file:
        file.write(query + '\n')

def test_create_100_people(query_handler):
    fake = Faker()

    # clear the existing data
    query_handler.clear_neo4j_graph()
    people =[]

    # generate and submit queries for 100 random people using Faker
    for i in range(100):
        name = fake.name()
        age = fake.random_int(min=18, max=100)
        person_id = f"Person_{fake.uuid4()}"  # Unique identifier for each person
        people.append({'name': name, 'id': person_id})
        create_query = f'CREATE (:Person {{name: "{name}", age: {age}}});'
        write_query_to_file(create_query)
        query_handler.submit_query(create_query)

    # perform a read query to count the number of people
    count_query = 'MATCH (p:Person) RETURN count(p) as total;'
    query_handler.submit_query(count_query)

    # assign friendships
    for person in people:
        number_of_friends = random.randint(1, 5)  # Each person will have 1 to 5 friends
        friends = random.sample([p for p in people if p != person], number_of_friends)

        for friend in friends:
            create_friendship_query = 'MATCH (a:Person {{name: "{0}"}}), (b:Person {{name: "{1}"}}) CREATE (a)-[:Friend]->(b);'.format(
                person['name'], friend['name'])
            query_handler.submit_query(create_friendship_query)

    # perform a read query to count the number of people
    count_people_query = 'MATCH (p:Person) RETURN count(p) as total;'
    query_handler.submit_query(count_people_query)

    # Extract the count result
    # Replace with actual method to retrieve results from your query handler
    count_people_result = query_handler.get_last_query_result()

    # Assert that the count of people is 100
    assert count_people_result == 100



    # Extract the count result
    # Replace with actual method to retrieve results from your query handler
    count_result = query_handler.get_last_query_result()

    # Assert that the count of people is 100
    assert count_result == 100

def mock_callback(num, response, tags):
    pass
