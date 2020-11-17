import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--title", type=str, required=True, help='Paper title')
parser.add_argument("--link", type=str, required=True, help='Paper links')
parser.add_argument("--tags", type=str, default="", help='Paper tags (comma separated)')
parser.add_argument("--description", type=str, default="", help='Paper description')

if __name__ == "__main__":
    args = parser.parse_args()
    conn = sqlite3.connect('cs242papers.db')
    c = conn.cursor()

    # Insert main paper details
    c.execute('''INSERT INTO papers (title, link, description) VALUES ("%s","%s","%s")''' % (args.title, args.link, args.description))
    paper_id = c.lastrowid

    # Links
    for tag in args.tags.strip().split(","):
        if tag.strip() == "":
            continue
        c.execute('''INSERT INTO tags (paper_id, tag) VALUES (%d,"%s")''' % (paper_id, tag))

    conn.commit()
    conn.close()

    
