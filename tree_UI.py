import tkinter as tk
from tkinter import ttk
from tkinter import *
import os
from tree import CustomTree


class FileSystemExplorer(CustomTree, tk.Tk):
    def __init__(self):
        super().__init__()
        # Configure the style
        style = ttk.Style()
        style.theme_use("clam")  # Choose a ttk theme
        style.configure("Treeview",
                        fieldbackground="silver",
                        foreground="black",
                        rowheight=25,
                        field_background="silver"
                        )  # Set background color
        style.map("Treeview", foreground=[('selected', 'blue')])  # Set selected item color

        # Set up treeview with columns
        self.treeview = ttk.Treeview(self.root)
        self.treeview.focus_set()
        self.treeview.heading("#0", text="File System", anchor=tk.W)
        # self.treeview.column("Size", anchor=tk.W, width=180)
        self.treeview.grid(row=0, column=0, columnspan=2, padx=10, pady=10)
        # self.treeview.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

        self.treeview_2 = ttk.Treeview(self.root)
        self.treeview_2.focus_set()
        self.treeview_2.heading("#0", text="Search", anchor=tk.W)
        self.treeview_2.grid(row=0, column=1, columnspan=4, padx=10, pady=10)

        self.entry_label = Label(text="Enter folder name:")
        self.entry_label.grid(row=1, column=0, padx=5, pady=5)

        self.search_label = Label(text="Search:")
        self.search_label.grid(row=2, column=0, padx=5, pady=5)
        # Create an Entry widget
        self.entry_widget = tk.Entry(self.root, width=30)
        self.entry_widget.grid(row=2, column=1, padx=5, pady=5)
        # self.entry.pack(padx=10, pady=10)

        # Create a Button to submit the entry
        self.submit_button = tk.Button(self.root, text="Search", command=self.search)
        self.submit_button.grid(row=2, column=2, padx=5, pady=5)
        # self.submit_button.pack()

        # Bind single-click event to get folder name
        # self.treeview.bind('<<TreeviewSelect>>', self.tree_click_event)
        self.treeview.bind('<1>', self.on_item_click)

        # Entry field for new folder or file
        self.entry_var = tk.StringVar()
        self.entry = ttk.Entry(self.root, textvariable=self.entry_var, width=30)
        self.entry.grid(row=1, column=1, padx=5, pady=5)
        # self.entry.pack(pady=5)

        self.path_list = []
        self.path = ""
        self.node_dict = {}  # Initialize the dictionary
        self.item_text = None
        # Buttons for creating new folder or file
        ttk.Button(self.root, text="Create Node", command=self.create_directory).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(self.root, text="Delete", command=self.delete).grid(row=1, column=3, padx=3, pady=5)
        # # Populate the tree with the file system pack(side=tk.LEFT, padx=5) pack(side=tk.LEFT, padx=6)
        # self.populate_tree(self.current_path)

    def create_directory(self):
        directory_name = self.entry_var.get()
        if directory_name:
            self.add_node(directory_name, self.item_text)
            self.populate_tree(self.root, parent="")

    def delete(self, parent=""):
        item_text = str(self.root.value)
        key = (parent, item_text)
        directory_node_id = self.node_dict.get(key)
        print(directory_node_id)
        self.delete_node(self.item_text)
        if directory_node_id:
            # Delete the directory node from the treeview
            self.treeview.delete(directory_node_id)

            # Remove the entry from the node_dict
            del self.node_dict[key]
            self.populate_tree(self.root, parent="")
        else:
            print("Directory not found:", self.item_text)

    def populate_tree(self, current_node, parent=""):
        item_text = str(current_node.value)
        key = (parent, item_text)

        # Check if the directory with the same name already exists
        existing_child = self.node_dict.get(key)

        if existing_child:
            # If the directory already exists, update its text
            self.treeview.item(existing_child, text=item_text)
        else:
            # If the directory doesn't exist, create a new node
            item_id = self.treeview.insert(parent, "end", text=item_text)
            self.node_dict[key] = item_id

        # Recursively populate children
        if current_node.children:
            for child in current_node.children:
                self.populate_tree(child, parent=self.node_dict[key])

    def on_item_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)

        if item:
            self.item_text = self.treeview.item(item, "text")
            # Your other code handling the selected item
        else:
            # No item selected, handle this case (optional)
            print("No item selected")

    def on_item_double_click(self, event):
        item = self.treeview.identify('item', event.x, event.y)

        if item:
            self.item_text = self.treeview.item(item, 'text')
            print("Selected item text:", self.item_text)
            # Populate the tree with the contents of the selected directory
            self.populate_tree(self.root, parent="")
        else:
            print("No item selected")

    def search(self):
        entered_text = self.entry_widget.get()
        self.treeview_2.delete(*self.treeview_2.get_children())
        if entered_text == "clear":
            self.treeview_2.delete(*self.treeview_2.get_children())
        else:
            result = self.dfs_search(self.root, entered_text)
            self.populate_search_tree(result, parent="")
            print(result.value)

    def dfs_search(self, current_node, target_file):
        if current_node is None:
            return None  # Target not found in the current subtree

        if current_node.value == target_file:
            if target_file not in self.path_list:
                self.path_list.append(current_node.value)
            return current_node  # Target file found

        # Recursively search in the child nodes (subdirectories)
        for child in current_node.children:
            result = self.dfs_search(child, target_file)
            if result:
                return result  # Target file found in one of the child subtrees

    def populate_search_tree(self, current_node, parent=""):
        item_text = str(current_node.value)
        key = (parent, item_text)

        # If the directory doesn't exist, create a new node
        item_id = self.treeview_2.insert(parent, "end", text=item_text)
        self.node_dict[key] = item_id

        # Recursively populate children
        if current_node.children:
            for child in current_node.children:
                self.populate_search_tree(child, parent=self.node_dict[key])


