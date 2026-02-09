from tree_logic.core import Node, add_node, show, load_yaml, save_yaml

def run_demo():
    # 1. Manual Creation
    print("\n...Creating Tree...",end="\n\n")
    root = Node(10)
    add_node(root, "L", 5)
    add_node(root, "R", 15)
    add_node(root, "LL", 3)
    add_node(root, "RR", 18)
    show(root)

    # 2. Save to YAML
    print("\n...Saving to output.yaml...",end="\n")
    save_yaml(root, "output.yaml")

    # 3. Load from YAML
    print("\n...Loading from test.yaml...",end="\n\n")
    # Ensure test.yaml exists in your folder before running
    yaml_tree = load_yaml("test.yaml")
    show(yaml_tree)

if __name__ == "__main__":
    run_demo()