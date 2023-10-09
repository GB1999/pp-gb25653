# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.


def hash(str):
    hash_val = 0
    for index in range(0, len(str)):
        hash_val += ord(str[index])

    return hash_val

print(hash("sb43278"))
print(hash("gb25653")%2)