from iap.common.helper import Meta, is_equal_meta

class Node:

    def __init__(self, name, meta):
        """Initialisation of Node object
        Args:

            (sting): name - name of node
            (list ot tuple): meta - meta data for node, (dimension, level)
        Attributed:

            id: identification for node
            name: node's name
            meta: node's meta data
            paretn: list of node's parent on highes level
            children: list of node's children on bottom level

        """

        self.id = 0
        self.name = name
        self.meta = Meta(meta[0], meta[1])
        self.parents = []
        self.children = []


    def add_node_by_path(self, path, metas, depth, new_nodes):
        """Recursive function that initialise new node and add node to tree hierarcy
        coresponding to the path and metas

            Args:
                (list): list of node name in specific path in tree
                (list): list of Meta object, meta datas of node's in path
                (int): depth of node's level, default value 0
                (list): list of new node's

        :param path:
        :param metas:
        :param depth:
        :param new_nodes:
        :return:

        """

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
        """Add child'node for current object:
            Args:
                (string): name of new node
                (Meta): meta data of new node

        :param name:
        :param meta:
        :return:

        """

        if name in [x.name for x in self.children]:
            raise Exception
        new_child = Node(name, meta)
        self.children.append(new_child)
        new_child.parents.append(self)
        return new_child


    def get_node_by_path(self, path):
        """Get node by specific path

            Args:
                (list): path - list of node's name in path
            Return:
                (Node): founded node

        :param path:
        :return:

        """

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
        """Change name of current node into new

            Args:
                (string): new_name - new name of current node

        :param new_name:
        :return:

        """
        self.name = new_name


    def get_path(self, path, metas):
        """Get path of current node
        Recursively moving to top parent fill arg path and metas

        Args:
            (list): path - list of node name
            (list): metas - list of meta data

        :param path:
        :param metas:
        :return:

        """

        if self.name == 'root':
            return
        path.insert(0, self.name)
        metas.insert(0, self.meta)
        if len(self.parents) != 1:
            raise Exception
        self.parents[0].get_path(path, metas)


    def get_children_by_meta(self, meta_filter, nodes_ids):
        """Get all children of current node that require meta data filter,
            recursively filling node_ids argument.
        Args:
            (list): meta_filter - list of meta data
            (list): list of node's id that satisfy meta data criteria

        :param meta_filter:
        :param nodes_ids:
        :return:

        """

        for child in self.children:
            if is_equal_meta(child.meta, meta_filter):
                nodes_ids.append(child.id)
            child.get_children_by_meta(meta_filter, nodes_ids)
        return


    def get_parent_by_meta(self, meta_filter):
        """Get parent of current node that require meta data filter,
            recursively filling node_ids argument.

        Args:
            (list): meta_filter - list of meta data

        Return:
            (Node): parent of current node thar satisfy input criteria

        :param meta_filter:
        :return:

        """

        for parent in self.parents:
            if is_equal_meta(parent.meta, meta_filter):
                return parent
            res = parent.get_parent_by_meta(meta_filter)
            if res is not None:
                return res
        return None
