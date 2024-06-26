#!/usr/bin/env python3

import requests
import json
from faker import Faker


APIHOST = "http://library.demo.local"
LOGIN = "cisco"
PASSWORD = "Cisco123!"

def getAuthToken():
    authCreds = (LOGIN, PASSWORD)
    r = requests.post(
        f"{APIHOST}/api/v1/loginViaBasic", 
        auth = authCreds
    )
    if r.status_code == 200:
        return r.json()["token"]
    else:
        raise Exception(f"Status code {r.status_code} and text {r.text}, while trying to Auth.")

def addBook(book, apiKey):
    r = requests.post(
        f"{APIHOST}/api/v1/books", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
        data = json.dumps(book)
    )
    if r.status_code == 200:
        print(f"Book {book} added.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book {book}.")

# Get the Auth Token Key
apiKey = getAuthToken()

def deleteBook(num, apiKey):
    r = requests.delete(
        f"{APIHOST}/api/v1/books/{num}", 
        headers = {
            "Content-type": "application/json",
            "X-API-Key": apiKey
            },
    )
    if r.status_code == 200:
        print(f"Book {r.text} deleted.")
    else:
        raise Exception(f"Error code {r.status_code} and text {r.text}, while trying to add book.")

def deleteBooks(apiKey):
    for i in range(0, 4):
        deleteBook(i, apiKey)

# Using the faker module, generate random "fake" books
fake = Faker()
deleteBooks(apiKey)
for i in range(0, 25):
    fakeTitle = fake.catch_phrase()
    fakeAuthor = fake.name()
    fakeISBN = fake.isbn13()
    book = {"id":i, "title": fakeTitle, "author": fakeAuthor, "isbn": fakeISBN}
    # add the new random "fake" book using the API
    addBook(book, apiKey) 
