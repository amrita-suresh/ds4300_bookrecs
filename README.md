# Book Recommendations Engine with Neo4j

For our final project for Large-Scale Information Storage & Retrieval, we created a book recommendations engine using the Neo4j graph database. We tried out a few different recommendations algorithms and are allowing you, the user, to choose the algorithm you want to use to find your next favorite book.
We started off by loading an existing dataset of hundreds of thousands of books, users, and reviews to our database. This formed the foundation on which we developed the algorithms. We then created a basic user interface to allow new users to create profiles for which book recommendations would be made. (In a perfect world, we would use the enterprise version of Neo4j to be able to return a book directly from the database to the webpage, but as that is beyond the scope of this class, we are instead returning Cypher queries that can be entered into a locally hosted server).
We learned a lot from this project and hope you will too!

# Try it out!
Use the following steps to try out our product yourself.
- Download Neo4j and start the local server on your computer.
- Download the 3 CSV files found at the link http://www2.informatik.uni-freiburg.de/~cziegler/BX/
- Move the files to your Neo4j .imports folder.
- Copy-paste into your Neo4j browser the Cypher commands from script.txt to load the data and create the relationships.
- Fill out your profile on https://amrita-suresh.github.io/ds4300_bookrecs/ and click the submit button corresponding to the algorithm you want to use to find a book recommendation.
- Copy-paste the resulting output into your Neo4j browser to find your next favorite book!