import sqlite3
import sys
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--field", type=str, default="", choices=["","title","link","tags"], help='Field to search by')
parser.add_argument("--value", type=str, default="", help="Value to search for (string matching)")

def get_all_ids(c):
    paper_ids = []
    for row in c.execute('''SELECT paper_id from papers'''):
        paper_ids.append(row[0])
    return paper_ids

def describe_paper(paper_id, c):
    c.execute('''SELECT paper_id, title, description, link FROM papers WHERE paper_id = %d''' % paper_id)
    paper_id, title, description, link = c.fetchone()
    tags = c.execute('''SELECT (tag) from tags WHERE paper_id = %d''' % paper_id)
    tags = ",".join([x[0] for x in tags])
    print("-"*100)
    print("Paper Id: %d" % paper_id)
    print("Title: %s" % title)
    print("Description: %s" % description)
    print("Link: %s" % link)    
    print("Tags: %s" % tags)
    print("-"*100)

def search_by_tags(value, c):
    ids = set()
    for row in c.execute('''SELECT paper_id FROM tags WHERE tag LIKE "%%%s%%"''' % value):
        ids.add(row[0])
    return list(ids)

def search_by_field(field, value, c):
    ids = []
    for row in c.execute('''SELECT paper_id FROM papers WHERE %s LIKE "%%%s%%" COLLATE NOCASE''' % (field, value)):
        ids.append(row[0])
    return ids

def search(field, value, c):
    if field == "tags":
        return search_by_tags(value, c)
    return search_by_field(field, value, c)

if __name__ == "__main__":
    args = parser.parse_args()
    conn = sqlite3.connect('cs242papers.db')
    c = conn.cursor()

    if args.field == "":
        paper_ids = get_all_ids(c)
    else:
        paper_ids = search(args.field, args.value, c)
    for paper_id in paper_ids:
        describe_paper(paper_id, c)

    conn.close()

    
