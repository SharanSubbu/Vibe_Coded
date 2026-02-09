import yaml

class Node:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def add_node(root, path, val):
    # Navigates L/R path to set a value
    curr = root
    for step in path.upper():
        if step == 'L':
            if not curr.left: curr.left = Node(None)
            curr = curr.left
        elif step == 'R':
            if not curr.right: curr.right = Node(None)
            curr = curr.right
    curr.val = val

def show(node, depth=0, pref="Root:"):
    # Visualizes the tree structure
    if not node: return
    print("  " * depth + f"{pref}{node.val}")
    if node.left or node.right:
        show(node.left, depth + 1, "L---")
        show(node.right, depth + 1, "R---")

def load_yaml(path):
    # Converts YAML file to Node objects
    with open(path, 'r') as f:
        data = yaml.safe_load(f)
    
    def parse(d):
        if not d: return None
        n = Node(d.get('value'))
        n.left = parse(d.get('left'))
        n.right = parse(d.get('right'))
        return n
    return parse(data)

def save_yaml(node, path):
    # Converts Node objects to YAML file
    def to_dict(n):
        if not n or n.val is None: return None
        res = {"value": n.val}
        if n.left: res["left"] = to_dict(n.left)
        if n.right: res["right"] = to_dict(n.right)
        return res

    with open(path, 'w') as f:
        yaml.dump(to_dict(node), f, sort_keys=False)