import psycopg2
import time

f = open("source.txt", 'r', encoding = 'utf-8')

contents = f.readlines()

paper = {
    "title" : "",
    "authors" : [],
    "year" : "",
    "venue" : "",
    "index" : "",
    "references" : [],
    "abstract" : ""
}

db = input("Enter Database name: ")
us = input("Enter username: ")
pw = input("Enter password: ")


conn = psycopg2.connect(database = db, user = us, password = pw, host = "127.0.0.1", port = "5432")
print ("Opened database successfully")

cur = conn.cursor()
start = time.time()
cur.execute(
    """
    CREATE TABLE PAPER (
        PAPER_ID INTEGER PRIMARY KEY,
        TITLE VARCHAR(1000),
        YEAR INTEGER,
        ABSTRACT VARCHAR(50000)
    );
"""
)
cur.execute(
    """
    CREATE TABLE AUTHORS (
        PAPER_ID INTEGER NOT NULL,
        AUTHOR_NAME VARCHAR(1000) NOT NULL,
        POSITION INTEGER,
        PRIMARY KEY (PAPER_ID, AUTHOR_NAME)
    );
"""
)
cur.execute(
    """
    CREATE TABLE VENUES (
        PAPER_ID INTEGER PRIMARY KEY,
        VENUE_NAME VARCHAR(10000)
    );
"""
)
cur.execute(
    """
    CREATE TABLE REF (
        PAPER_ID INTEGER NOT NULL,
        REFERENCE_ID INTEGER NOT NULL,
        PRIMARY KEY (PAPER_ID, REFERENCE_ID)
    );
"""
)

print("Table created successfully")
paper = {}
paper["abstract"] = ""
paper["authors"] = []
paper["references"] = []
paper["venue"] = ""

count = 0
for line in contents:
    if line == '\n':
        query = f"""
            INSERT INTO PAPER (PAPER_ID, TITLE, YEAR, ABSTRACT)
            VALUES ({paper["index"]}, '{paper["title"]}', {paper["year"]}, 
            """
        if len(paper["abstract"]) == 0:
            query += "NULL);"
        else:
            query += f"""'{paper["abstract"]}');"""
        
        cur.execute(query)

        pos = 0

        for author in paper["authors"]:
            cur.execute(f"""
            INSERT INTO AUTHORS (PAPER_ID, AUTHOR_NAME, POSITION)
            VALUES ({paper["index"]}, '{author}', {pos});
            """)
            pos += 1

        query = f"""
            INSERT INTO VENUES (PAPER_ID, VENUE_NAME)
            VALUES ({paper["index"]}, 
            """
        if len(paper["venue"]) == 0:
            query += "NULL);"
        else:
            query += f"""'{paper["venue"]}');"""

        cur.execute(query)
        
        for reference in paper["references"]:
            cur.execute(f"""
            INSERT INTO REF (PAPER_ID, REFERENCE_ID)
            VALUES ({paper["index"]}, '{reference}');
            """)

        count += 1
        paper = {}
        paper["abstract"] = ""
        paper["authors"] = []
        paper["references"] = []
        paper["venue"] = []
    line = line.strip()
    if line.startswith("#*"):
        line = line[2:]
        line = line.replace("'", "''")
        paper["title"] = line

    elif line.startswith("#t"):
        line = line[2:]
        paper["year"] = line

    elif line.startswith("#index"):
        line = line[6:]
        paper["index"] = line

    elif line.startswith("#!"):
        line = line[2:]
        line = line.replace("'", "''")
        paper["abstract"] = line

    elif line.startswith("#c"):
        line = line[2:]
        line = line.replace("'", "''")
        paper["venue"] = line

    elif line.startswith("#@"):
        authors = []
        line = line[2:]
        line = line.replace("'", "''")
        line = line.split(',')
        for author in line:
            if author not in paper["authors"]:
                if author != '':
                    paper["authors"].append(author)

    elif line.startswith("#%"):
        line = int(line[2:])
        if line not in paper["references"]:
            if line is not None:
                if line != paper["index"]:
                    paper["references"].append(line)
         
conn.commit()
cur.close()
end = time.time()
print(f"{count} records wrote into table")
print(f"Time taken: {end - start} seconds")
conn.close()