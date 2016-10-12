import argparse
import sqlite3
from pprint import pprint

conn = sqlite3.connect('sub_db.db')
c = conn.cursor()

list_of_subs = []
subscribers = c.execute(" select * from subs; ")

parser = argparse.ArgumentParser(description='Number of Subscribers to Display')
parser.add_argument('integers', metavar='S', default= 10, type=int, help='how many subs')
args = parser.parse_args()
for subscriber in subscribers:
    list_of_subs.append(subscriber)


def printSubs(n):
    print('List of Subscribers'.center(55, '*'))
    for i in range(n):
        print(list_of_subs[i][0] + '  |  ' + list_of_subs[i][1] + ' | ' + list_of_subs[i][2])

printSubs(args.integers)

