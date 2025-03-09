import tkinter as tk
from tkinter import messagebox

class Task:
    def __init__(self, title, priority, deadline, description, completed=False):
        self.title = title
        self.priority = priority
        self.deadline = deadline
        self.description = description
        self.completed = completed

    def __str__(self):
        return f"Task: {self.title}"
    
    def display_task(self):
        completed_str = "Completed" if self.completed else "Not completed"
        return f"Title: {self.title}, Priority: {self.priority}, Deadline: {self.deadline}, Description: {self.description}, {completed_str}"
    
    def mark_completed(self):
        self.completed = True
        print("Task marked as completed.")

    def mark_not_completed(self):
        self.completed = False
        print("Task marked as not completed.")

    def update_task(self, title=None, priority=None, deadline=None, description=None):
        if title:
            self.title = title
        if priority:
            self.priority = priority
        if deadline:
            self.deadline = deadline
        if description:
            self.description = description
        print("Task updated.")

class ToDoList:
    def __init__(self):
        self.tasks = []

    def add_task(self, task):
        self.tasks.append(task)
        print("Task added.")

    def remove_task(self, task):
        self.tasks.remove(task)
        print("Task removed.")

    def display_tasks(self):
        for task in self.tasks:
            print(task.display_task())
    
    def sort_tasks(self, by="priority"):
        if by == "priority":
            self.tasks.sort(key=lambda x: x.priority)
        elif by == "deadline":
            self.tasks.sort(key=lambda x: x.deadline)
        print("Tasks sorted.")

    def filter_tasks(self, by="completed"):
        if by == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif by == "not completed":
            filtered_tasks = [task for task in self.tasks if not task.completed]
        for task in filtered_tasks:
            print(task.display_task())

class ToDoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do Application")
        self.to_do_list = ToDoList()

        self.title_label = tk.Label(root, text="Title")
        self.title_label.pack()
        self.title_entry = tk.Entry(root)
        self.title_entry.pack()

        self.priority_label = tk.Label(root, text="Priority")
        self.priority_label.pack()
        self.priority_entry = tk.Entry(root)
        self.priority_entry.pack()

        self.deadline_label = tk.Label(root, text="Deadline")
        self.deadline_label.pack()
        self.deadline_entry = tk.Entry(root)
        self.deadline_entry.pack()

        self.description_label = tk.Label(root, text="Description")
        self.description_label.pack()
        self.description_entry = tk.Entry(root)
        self.description_entry.pack()

        self.add_button = tk.Button(root, text="Add Task", command=self.add_task)
        self.add_button.pack()

        self.sort_button = tk.Button(root, text="Sort Tasks by Priority", command=self.sort_tasks)
        self.sort_button.pack()

        self.tasks_listbox = tk.Listbox(root)
        self.tasks_listbox.pack()

    def add_task(self):
        title = self.title_entry.get()
        priority = int(self.priority_entry.get())
        deadline = self.deadline_entry.get()
        description = self.description_entry.get()
        task = Task(title, priority, deadline, description)
        self.to_do_list.add_task(task)
        messagebox.showinfo("Info", "Task added successfully")

    def sort_tasks(self):
        self.to_do_list.sort_tasks(by="priority")
        self.display_tasks()

if __name__ == "__main__":
    root = tk.Tk()
    app = ToDoApp(root)
    root.mainloop()