# import Neo4J-Python connector
from py2neo import Graph
# set up graph
graph = Graph("bolt://localhost:11001", auth=("neo4j", "password"))

# Method #1: Book Recs based on Title
# Find all user id'S that like a given book (like = rating of 8+)
def find_similar_users(book_title):
    id_results = graph.run("MATCH (b:BX_Book{title: '" + str(book_title) + "'})<-[r:LIKE]-(u:BX_User) RETURN u.ID ").data()
    return id_results

# example
ex1_users = find_similar_users('To Kill a Mockingbird')
ex1_users
      

# Given a list of users, find all books that they like and make a dataframe of the book names and ratings
def find_books_from_users(user_list):
    book_results = []
    for user in user_list:
        book_results.append(graph.run("MATCH (n:Author)<-[:WRITTEN_BY]-(b:BX_Book)<-[r:LIKE]-(u:BX_User{ID:" + 
                                      str(user["u.ID"]) + "}) RETURN b.title, n.AName, r.BRating").data())
    return book_results

# example
ex1_books = find_books_from_users(ex1_users)
ex1_books


# creating a dataframe from the book and rating info using pandas
import pandas as pd
import numpy as np

# book title -> data frame
# uses previous functions to find books liked by users who liked input book
# finds amount of reviews each book has and the sum of them 
def make_df(book_title):
    # creating the list of books liked by users who like the same book
    books = find_books_from_users(find_similar_users(book_title))
    # initializing data list
    data_dict = {}
    # looping through list of list of dictionaries of book tiles/ratings
    for user_data in books:
        for book in user_data:
            # filter out book title input
            if book['b.title'] != book_title:
                title = book['b.title']
                rating = int(book['r.BRating'])
                author = book['n.AName']
                # fix '&' not showing up correctly
                title = title.replace("&amp;", "&")
                # addressing duplicate books
                if title not in data_dict.keys():
                    data_dict[title] = [rating, author] 
                else: 
                    # rating column will be total ratings
                    data_dict[title] = [data_dict[title][0] + rating, author]            
    # setting up 
    book_names = []
    authors = []
    ratings = []
    for k,v in data_dict.items():
        book_names.append(k)
        authors.append(v[0])
        ratings.append(v[1])
    data = []
    data.append(book_names)
    data.append(authors)
    data.append(ratings)
    df = pd.DataFrame(data).T
    df.columns = ["Title", "Ratings", "Author"]
    # sort by total ratings
    sorted_df = df.sort_values(by=['Ratings'], ascending=[False])
    return sorted_df
        
df_results = make_df("The Color of Magic")[0:10]
df_results


# string, int -> list
# book title, # of results desired -> list of recomended titles 
def review_weight_recomend(book_title, number_results):
    df = make_df(book_title)
    results = []
    for index, rows in df.iterrows():
        results.append([rows[0], rows[2]])
    return results[0:number_results]
          
print(review_weight_recomend("The Color of Magic", 5))


# Prints out the recomendations in a semi-pleasing manner 
def print_book_recs(book_title, number_results):
    result_list = review_weight_recomend(book_title, number_results)
    count = 1
    end_result = []
    for result in result_list:
        str_result = (str(count) + ". " + result[0] + " - " + result[1])
        end_result.append(str_result)
        count +=1
    return print('\n'.join(end_result))
        
print_book_recs("The Color of Magic", 10)

# Method #2: Book Recs based on Author

# Find all book written by author
# author name -> list of books
def find_book_by_auth(auth_name):
    id_results = graph.run("MATCH (a:Author{AName: '" + auth_name + "'})<-[r:WRITTEN_BY]-(b:BX_Book)<-[r2:LIKE] \
                            -(u:BX_User)-[r3:LIKE]->(b2:BX_Book)-[r4:WRITTEN_BY]->(a2:Author) \
                            RETURN a2.AName as Author, b2.title as Title, r3.BRating AS Rating, \
                            count(b2.ISBN) as Count order by count(b2.ISBN) desc").data()
    return id_results


# author name -> printing x recomendations
def simple_author_recs(auth_name, x):
    data = pd.DataFrame(find_book_by_auth(auth_name))
    df = pd.DataFrame(data, columns=['Author','Count', 'Rating', 'Score', 'Title'])
    df['Author'] = data["Author"]
    df["Count"] = data["Count"]
    df["Rating"] = data["Rating"]
    df["Score"] = df["Count"] * df["Rating"]
    df["Title"] = data["Title"]
    df = df.sort_values(by=["Score"], ascending=False)
    count = 1
    result_str = ""
    for i, row in df.iterrows():
        if i < x:
            result_str += (str(count) + ". " + row["Title"] + " - " + row["Author"] + '\n') 
            count +=1
    return print(result_str)

# example
simple_author_recs("John Green", 5)

# Methods 1 and 2 Driver:
def get_recomendation(fav, fav_type, amount=5):
    if fav_type == "author":
        return simple_author_recs(fav, amount)
    if fav_type == "book":
        return print_book_recs(fav, amount)
    else: 
        return "Please put in a valid type"


 # example for author
get_recomendation("John Green", "author")
# example for book
get_recomendation("The Color of Magic", "book", 10)