import pandas as pd
import numpy as np
import mgclient


def import_data(cursor):
    df = pd.read_csv('relationship.csv')
    for i, *_, a_id, type, b_id, category, _, notes in df.itertuples():
        kwargs = dict(
            a_id=a_id,
            b_id=b_id,
            a_name=a_id.rsplit('_', 1)[0],
            b_name=b_id.rsplit('_', 1)[0],
            type=type,
            category=category,
            notes=notes.replace('"', '`') if notes is not np.nan else ''
        )
        cursor.execute(import_query, kwargs)


import_query = """
merge (a: Person {id: $a_id})
set a.name = $a_name
merge (b: Person {id: $b_id})
set b.name = $b_name
create (a) - [:RELATIONSHIP {
    type: $type, category: $category, notes: $notes
}] -> (b)
"""

connection = mgclient.connect(host='192.168.0.20', port=7687, sslmode=mgclient.MG_SSLMODE_REQUIRE)
connection.autocommit = True
cursor = connection.cursor()
cursor.execute('match (a) detach delete a;')
cursor.execute('create constraint on (p: Person) assert p.id is unique;')
import_data(cursor)
