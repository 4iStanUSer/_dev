from ..helpers import Meta

class Node:

    def __init__(self, name, meta):
        self.id = 0
        self.name = name
        self.meta = Meta(meta[0], meta[1])
        self.parents = []
        self.children = []

    def add_node_by_path(self, path, metas, depth, new_nodes):
        node = None
        # Find node in children
        for child in self.children:
            if child.name == path[depth]:
                node = child
                break
        # Create new node
        if node is None:
            node = Node(path[depth], metas[depth])
            self.children.append(node)
            node.parents.append(self)
            new_nodes.append(node)
        if depth != len(path) - 1:
            return node.add_node_by_path(path, metas, depth + 1, new_nodes)
        else:
            return node

    def add_child(self, name, meta):
        if name in [x.name for x in self.children]:
            raise Exception
        new_child = Node(name, meta)
        self.children.append(new_child)
        new_child.parents.append(self)
        return new_child

    def get_node_by_path(self, path):
        # TODO Rewrite (DR)
        if len(path) == 0:
            return self
        elif self.children:
            for child in self.children:
                if child.name == path[0]:
                    res = child.get_node_by_path(path[1:])
                    if res:
                        return res
        return None

    def rename(self, new_name):
        pass

    def get_path(self, path):
        if self.name == 'root':
            return
        path.insert(0, self.name)
        if len(self.parents) != 1:
            raise Exception
        self.parents[0].get_path(path)
