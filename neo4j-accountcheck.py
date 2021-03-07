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
# Expects the following query to be run first to populate eigenvector fields:
# 
# CALL gds.alpha.eigenvector.write({
#  nodeProjection: 'screen_name',
#  relationshipProjection: 'FOLLOWING',
#  normalization: 'max',
#  writeProperty: 'eigenvector'
# })

import json
import argparse
import sys
import os
from neo4j import GraphDatabase

parser = argparse.ArgumentParser(description='JSON 2 Neo4J', epilog='P.S. Trust The Plan')
parser.add_argument('--input', help='List of accounts', type=argparse.FileType('r'), default=sys.stdin, required=False)
args = parser.parse_args()

with open(os.path.expanduser('~/.neo4j_config'), 'r') as f:
	config = json.load(f)

driver = GraphDatabase.driver("neo4j://localhost:7687", auth=(config['username'], config['password']))

def check(driver, n):
    with driver.session() as session:
        tx = session.begin_transaction()
        r = tx.run("MATCH (n) where n.screen_name = $n return count(n) as count, n.eigenvector as eigenvector", parameters={'n':n}).data()
        #print(r)
        if len(r) > 0:
            return r[0]['eigenvector']
        else:
            return False
        tx.close()

d = []
r = []
for line in args.input:
    n = check(driver, line.strip())
    if n != False:
        r.append({"name":line.strip(), "eigenvector":float(n)})

while len(r) > 0:
    largest = {"name":"none", "eigenvector":0}
    k = 0
    x = 0
    for e in r:
        if e['eigenvector'] > largest['eigenvector']:
            largest = e.copy()
            k = x
        x += 1
    del r[k]
    d.append(largest)

for e in d:
    print(e)