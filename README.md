# Neo4j-PyScripts

## Usage Notes
These scripts were used with the Neo4j Desktop application, with each database dedicated to a single analysis group. The JSON data used and expected is the output of [twarc](https://github.com/DocNow/twarc) users command. See _grabuser.sh_.

These scripts are designed to run under the following constraints:
```
CREATE CONSTRAINT ON (z:screen_name) ASSERT z.screen_name IS UNIQUE
```

The neo4j-accountcheck.py requires this to be run first:
```
CALL gds.alpha.eigenvector.write({
 nodeProjection: 'screen_name',
 relationshipProjection: 'FOLLOWING',
 normalization: 'max',
 writeProperty: 'eigenvector'
})
```

Usage Example:
```
user@WORKSTATION:~/Neo4j-PyScripts$ for f in data/*following.json; do echo $f;./json2nodes.py --input $f;done
user@WORKSTATION:~/Neo4j-PyScripts$ for f in data/*following.json; do echo $f;./json2relations.py --input $f;done

```

## Configuration
The username and password for access to Neo4J is a standard JSON file with the following format.
```
{
	"username":"neo4j",
	"password":"toomanysecrets"
}
```
This should be in _~/.neo4j_config_

## License
Copyright (C) 2021, Michigan State University.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
