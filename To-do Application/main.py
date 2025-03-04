class Task():
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

class ToDoList():
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

# Create tasks
task1 = Task("Task 1", 1, "2021-12-31", "Description 1")
task2 = Task("Task 2", 2, "2021-12-30", "Description 2")
task3 = Task("Task 3", 3, "2021-12-29", "Description 3")
task4 = Task("Task 4", 4, "2021-12-28", "Description 4")
task5 = Task("Task 5", 5, "2021-12-27", "Description 5")

# Create a ToDoList object
to_do_list = ToDoList()

# Add tasks to the list
to_do_list.add_task(task1)
to_do_list.add_task(task2)   

# Display tasks
to_do_list.display_tasks()

# Sort tasks by priority
to_do_list.sort_tasks(by="priority")

# Display sorted tasks
to_do_list.display_tasks()