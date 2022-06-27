# DB-Gen-from-raw-data
Creating a relational database from raw data (ER diagram -> relational schema) and performing advanced queries on the database.

* The raw data had details of 629814 scientific papers in total.
* We designed the ER diagram based on the data given and the relations we found to be good.
* We used the website https://erdplus.com/ to generate the ER Diagram and the Relational Schema of our proposed database.
* We used python to write a parser which will read from the source file and insert them into the database. We used the psycopg2 module of python to write into the databse.
* After populating the database, we came up with some advanced SQL queries to be executed on the database.
