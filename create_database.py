import sqlite3

if __name__ == "__main__":
    conn = sqlite3.connect('cs242papers.db')

    c = conn.cursor()

    # Create table
    c.execute('''CREATE TABLE papers
                 (paper_id INTEGER PRIMARY KEY AUTOINCREMENT, title text, description text, link text)''')

    # Create tags table
    c.execute('''CREATE TABLE tags
                (tag_id INTEGER PRIMARY KEY AUTOINCREMENT, paper_id INTEGER, tag text, FOREIGN KEY (paper_id) REFERENCES papers (paper_id))''')

    # Save (commit) the changes
    conn.commit()

    # We can also close the connection if we are done with it.
    # Just be sure any changes have been committed or they will be lost.
    conn.close()
