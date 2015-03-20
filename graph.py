import networkx as nx
import pymongo
from test import forceatlas2_layout
import matplotlib.pyplot as plt

connection = pymongo.Connection()
db = connection.graph
users = db.users


def get_relationships_graph():
    user_ids = users.find().distinct("user_id")
    main_graph = nx.Graph()
    for user in users.find(timeout=False):
        del user['_id']
        attributes = {
            "first_name": user['first_name'],
            "last_name": user['last_name'],
            "photo": user['photo_50']
        }
        main_graph.add_node(user['user_id'], **attributes)
    for user_id in user_ids:
        user = users.find_one({"user_id": user_id})
        for another_user_id in user_ids:
            if user_id == another_user_id: continue
            if user['friends']:
                if another_user_id in user['friends']: main_graph.add_edge(user_id, another_user_id)
    return main_graph

if __name__ == "__main__":
    g = get_relationships_graph()
    nx.write_gexf(g, 'test.gexf')
    positions = forceatlas2_layout(g, linlog=False, nohubs=False, iterations=100)
    labels = {node[0]: "%s %s" % (node[1]['first_name'], node[1]['last_name']) for node in g.nodes_iter(data=True)}
    nx.draw(g, positions)
    nx.draw_networkx_labels(g, positions, labels)
    plt.show()

