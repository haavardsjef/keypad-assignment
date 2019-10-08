"""State machine"""

class State:

    def __init__(self, next_nodes, previous_node, key):
        self.next_nodes = next_nodes
        self.previous_node = previous_node
        self.key = key

    def input_key(self, key):
        next_node = None
        for node in self.next_nodes:
            if node.key == key:
                next_node = node
        if next_node is None:
            next_node = self.previous_node
        self = next_node

    def set_next_nodes(self, next_nodes):
        self.next_nodes = next_nodes

    def __str__(self):
        return str(self.key)


node1 = State(None, None, 2)
node2 = State(None, [node1], 1)
node1.set_next_nodes([node2])

print(node1)
node1.input_key(1)
print(node1)




input()
