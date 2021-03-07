#!/bin/python3

# Copyright (C) 2021, Michigan State University.
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# Notes:
# Is designed to be run under -> "CREATE CONSTRAINT ON (z:screen_name) ASSERT z.screen_name IS UNIQUE"

import json
import argparse
import sys
import os
from neo4j import GraphDatabase

parser = argparse.ArgumentParser(description='JSON to Neo4J Nodes', epilog='P.S. Trust The Plan')
parser.add_argument('--input', help='JSON File, or stdin if not specified', type=argparse.FileType('rb'), default=sys.stdin, required=False)
args = parser.parse_args()

with open(os.path.expanduser('~/.neo4j_config'), 'r') as f:
	config = json.load(f)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(config['username'], config['password']))

q = "UNWIND $batch as z MERGE (n:screen_name {screen_name:z.screen_name}) ON CREATE SET n = z"

nodes = []
for line in args.input:
    j = json.loads(line)
    n = {'id': j['id'], 'screen_name': j['screen_name'], 'statuses_count': j['statuses_count'], 'description': j['description'], 'url': j['url'], 'verified': j['verified'], 'favourites_count': j['favourites_count'], 'followers_count': j['followers_count'], 'friends_count': j['friends_count'], 'name': j['name'], 'location': j['location'], 'protected': j['protected'], 'created_at': j['created_at']}
    nodes.append(n)

if len(nodes)>0:
    with driver.session() as session:
        tx = session.begin_transaction()
        tx.run(q, batch=nodes)
        tx.commit()
        tx.close()
