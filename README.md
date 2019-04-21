# Book Recommendations Engine with Neo4j

For our final project for Large-Scale Information Storage & Retrieval, we created a book recommendations engine using the Neo4j graph database. We tried out a few different recommendations algorithms and are allowing you, the user, to choose the algorithm you want to use to find your next favorite book.
We started off by loading an existing dataset of hundreds of thousands of books, users, and reviews to our database. This formed the foundation on which we developed the algorithms. We then created a basic user interface to allow new users to create profiles for which book recommendations would be made. (In a perfect world, we would use the enterprise version of Neo4j to be able to return a book directly from the database to the webpage, but as that is beyond the scope of this class, we are instead returning Cypher queries and Python code that can be entered into a locally hosted server).
Our algorithms range from simple to complex. In the simple algorithms, we calculate scores for each book using basic arithmetic and return the books ranked by top score. In the more complex algorithms, we use matrix factorization and other methods to find the best matches for the given profile.
We learned a lot from this project and hope you will too!

## Try it out!
Use the following steps to try out our product yourself.
- Download Neo4j and start the local server on your computer.
- Download the 3 CSV files found at the link http://www2.informatik.uni-freiburg.de/~cziegler/BX/
- Move the files to your Neo4j imports folder (if downloaded with homebrew).
- Copy-paste into your Neo4j browser the Cypher commands from "script.txt" to load the data and create the relationships.
- Install the py2neo driver with `pip install py2neo`. Use your favorite Python IDE to open and run the file "book_recs.py" and "Project_like_dislike.py".
- Fill out your profile on https://amrita-suresh.github.io/ds4300_bookrecs/ and click the submit button corresponding to the algorithm you want to use to find a book recommendation.
- Copy-paste the resulting output into your Neo4j browser or Python IDE (depending on the algorithm) to find your next favorite book!

## Walkthrough of the files
- `script.txt` contains the Cypher commands to set up the Neo4j database
- `Book Rec Algorithms.ipynb` contains the Python code for books-liked and authors-liked collaborative filtering algorithms, as well as the matrix factorization code. The results of matrix factorization can be found at this link: https://colab.research.google.com/drive/1JLhJMTDZyTbtNz0uzlHCALbLBfhwyXPo
- `Project_like_dislike.py` contains the Python code for the like-and-dislike collaborative filtering algorithm.