class TreeNode:
    def __init__(self, value):
        self.value = value
        self.children = []
        self.parent = None


class CustomTree:
    def __init__(self):
        self.root = None

    def add_node(self, new_value, parent_value):
        if not self.root:
            # Tree is empty, create root
            self.root = TreeNode(new_value)
        else:
            parent_node = self._find_node(self.root, parent_value)
            if parent_node:
                child = TreeNode(new_value)
                child.parent = self
                parent_node.children.append(child)
            else:
                print(f"Parent node with value {parent_value} not found.")

    def delete_node(self, target_value):
        if not self.root:
            print("Tree is empty.")
            return

        if self.root.value == target_value:
            # If the root is the target, set the tree to empty
            self.root = None
            return

        parent_node, target_node = self._find_parent_and_node(self.root, target_value)
        if parent_node and target_node:
            parent_node.children.remove(target_node)
            for child in parent_node.children:
                print(child.value)
        else:
            print(f"Node with value {target_value} not found.")

    def _find_node(self, current_node, target_value):
        if current_node.value == target_value:
            return current_node

        for child in current_node.children:
            result = self._find_node(child, target_value)
            if result:
                return result

    def _find_parent_and_node(self, current_node, target_value, parent_node=None):
        if current_node.value == target_value:
            return parent_node, current_node

        for child in current_node.children:
            result = self._find_parent_and_node(child, target_value, current_node)
            if result:
                return result

    def display_tree(self, current_node=None, indent=0):
        if not current_node:
            current_node = self.root

        print("  " * indent + f"- {current_node.value}")

        for child in current_node.children:
            self.display_tree(child, indent + 1)



