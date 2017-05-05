
class Tree:

    def __init__(self):
        self.tree = {}
        self.root = None

    def build_in_breath(self,  path, dict=None, order=0):
        """
            Fill tree

            :param dict:
            :type dict:
            :param path:
            :type path:
            :param order:
            :type order:
            :return:
            :rtype:
            """
        if dict is None:
            dict = self.tree

        if order < len(path):
            key = path[order]
            if key not in dict.keys():
                dict[key] = {}
            order += 1
            self.build_in_breath(dict[key], path, order)

    def build_in_depth(self, path, oder):
        pass

    def get_by_path(self, path, root=None, order=0):

        if root==None:
            root = self.tree
        while order < len(path):

            key = path[order]
            order += 1
            next_iter = root[key]
            if next_iter is None:
                return None
            self.build_in_breath(next_iter, path, order)

        if order == len(path):
            return next_iter

    def get_by_level(self, path):
        pass