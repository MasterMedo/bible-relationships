# Exploring bible relationships with [memgraph](https://memgraph.com)

## Preparing the dataset
Each line in the raw [dataset](https://data.world/bradys/bibledata-personrelationship/discuss/7z4ehvcn#sgi57e7l) by [Brady Stepheson](https://data.world/bradys) contains information about the relationship between two persons and the reference to the bible verse.

Cleaned dataset excerpt:
```
person_id_1,relationship,person_id_2,reference,
G-d_1,Creator,Adam_1,GEN 2:7,
Adam_1,husband,Eve_1,GEN 3:6,
Eve_1,wife,Adam_1,GEN 2:25,
Adam_1,father,Cain_1,GEN 4:1,
Cain_1,son,Adam_1,GEN 4:1,
```

We want to turn that data into something like:

![](./img/graph-excerpt.png)

To do that we need to translate each line in the file to a [cypher](https://en.wikipedia.org/wiki/Cypher_(query_language)) query. In pseudo-code that would be:

```
create NODE "G-d_1" if it doesn't exist
create NODE "Adam_1" if it doesn't exist
create RELATIONSHIP "Creator"
```

In cypher that looks like this:
```cypher
MERGE (a: Person {id: "G-d_1"})
MERGE (b: Person {id: "Adam_1"})
CREATE (a) - [r: RELATIONSHIP {type: "Creator"}] -> (b)
```
