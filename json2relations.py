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

import json
import argparse
import sys
import os
from neo4j import GraphDatabase

parser = argparse.ArgumentParser(description='JSON 2 Neo4J Relations', epilog='P.S. Trust The Plan')
parser.add_argument('--input', help='JSON File', type=argparse.FileType('rb'), default=sys.stdin, required=False)
args = parser.parse_args()

with open(os.path.expanduser('~/.neo4j_config'), 'r') as f:
	config = json.load(f)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(config['username'], config['password']))

q = "match (n1:screen_name), (n2:screen_name) where n1.screen_name=$n1 and n2.screen_name=$n2 merge (n1)-[:FOLLOWING]->(n2)"

fileparm = args.input.name.split('-')

with driver.session() as session:
    a = fileparm[0]
    for line in args.input:
        j = json.loads(line)
        tx = session.begin_transaction()
        tx.run(q, parameters={'n1':a, 'n2':j['screen_name']})
        tx.commit()
        tx.close()
driver.close()
