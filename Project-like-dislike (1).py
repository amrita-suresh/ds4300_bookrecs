#!/usr/bin/env python
# coding: utf-8

# In[29]:


# import Neo4J-Python connector
from py2neo import Graph
# set up graph
graph = Graph("http://localhost:7474/", auth=("neo4j", "Ilb4mlds"))


# In[31]:


import pandas as pd
import numpy as np


# ## Strategy 3: Like and Dislike
# Find all the users that like and hate the same books and return their liked book

# In[167]:


# create a dataframe that includes all books that is likened by the users that has same like_book and dislike book 
# as you
def find_user_by_like_dislike(like_book, dislike_book):
    # get all the users that has the like and dislike book
    query = '''MATCH (b0:BX_Book{title:"'''  + dislike_book + '''"}) <- [r0:HATED] - (u:BX_User)-[r:LOVE]->(b:BX_Book{title:"''' + like_book + '''"}) RETURN u.ID'''
    print(query)
    #id_results = graph.run('''MATCH (b0:BX_Book{title:"'''  + dislike_book + '''"}) <- [r0:HATED] - (u:BX_User)-[r:LOVE]->(b:BX_Book{title:"''' + like_book + "'}) RETURN u.ID").data()
    id_results = graph.run(query).data()
    data = pd.DataFrame(id_results)
    bookDF =[]
    # go through the list of userID, then run a cypher query to get all the book that the users like 
    # and put it in a dataframe format
    for index, row in data.iterrows():
        q = "Match (u:BX_User{ID:" + str(row[0]) + "})-[r:LOVE]->(b:BX_Book)-[:WRITTEN_BY]->(a:Author) RETURN  b.title AS Title, r.BRating AS Rating ,a.AName as Author"
        book_result= graph.run(q).data()
        d = pd.DataFrame(book_result)
        bookDF.append(d)
    # pull out the df from list and create a frequency count and a score accordingly
    if len(bookDF) != 0:
        bookDF2 = bookDF[0]
        bookDF2['Freq'] =  bookDF2['Title'].groupby(bookDF2['Title']).transform('count')
        bookDF2['Score'] =bookDF2['Freq'] * bookDF2['Rating']
        return bookDF2[['Title', 'Author', 'Score']]
    return []

# Example
find_user_by_like_dislike("Fahrenheit 451", "Animal Farm")


# like_book and dislike_book -> printing x recomendations
def like_dislike_rec(like_book, dislike_book, x):
    dataDF = find_user_by_like_dislike(like_book, dislike_book)
    if len(dataDF) != 0:
        df = dataDF.sort_values(by=["Score"], ascending=False)
        count = 1
        result_str = ""
   
        for i, row in df.iterrows():
            if i < x:
                result_str += (str(count) + ". " + row["Title"] + " - " + row["Author"] + '\n') 
                count +=1
        return print(result_str)
    return print("Not enough information to provide a rec! Sorry!")


# In[152]:


like_dislike_rec("Fahrenheit 451", "Animal Farm", 8)


# In[156]:


like_dislike_rec("Scarlet Letter", "Tess of the D'Urbervilles (Wordsworth Classics)", 8)


# In[165]:


like_dislike_rec("Scarlet Letter", "Great Expectations", 8)


# In[168]:


like_dislike_rec("Their Eyes Were Watching God", "The Wind Done Gone: A Novel", 8)


# In[ ]:




