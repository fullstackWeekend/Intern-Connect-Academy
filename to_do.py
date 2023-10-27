import PySimpleGUI as sg

# Step 1: Set Theme
sg.theme('LightBrown12')

# Function to load tasks and due dates from a file
def load_tasks(filename):
    try:
        with open(filename, "r") as file:
            lines = file.read().splitlines()
            tasks = [line.split('\t')[0] for line in lines]
            due_dates = [line.split('\t')[1] if '\t' in line else "" for line in lines]
            return tasks, due_dates
    except FileNotFoundError:
        return [], []

# Function to save tasks and due dates to a file
def save_tasks(filename, tasks, due_dates):
    with open(filename, "w") as file:
        for task, due_date in zip(tasks, due_dates):
            file.write(f"{task}\t{due_date}\n")

# Define the layout of your To-Do app
layout = [
    [sg.Text("To-Do List", size=(20, 1), justification="center", font=("Any", 20))],
    [sg.InputText("", key="task", size=(30, 1), tooltip="Enter task"),
     sg.InputText("", key="due_date", size=(15, 1), tooltip="Enter due date"),
     sg.Button("Add")],
    [sg.Listbox(values=[], key="tasks", size=(30, 5),
                select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED),
     sg.Listbox(values=[], key="due_dates", size=(15, 5),
                select_mode=sg.LISTBOX_SELECT_MODE_EXTENDED)],
    [sg.Button("Delete"), sg.Button("Clear All"), sg.Button("Save"), sg.Button("Exit")]
]

# Create a window with your layout
window = sg.Window("To-Do List App", layout, finalize=True)
task_file = "tasks.txt"

# Load tasks and due dates from the file
tasks, due_dates = load_tasks(task_file)

# Update the listboxes with the loaded values
window["tasks"].update(values=tasks)
window["due_dates"].update(values=due_dates)

# Event loop
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED or event == "Exit":
        break

    if event == "Add" and (values["task"] or values["due_date"]):
        task = values["task"]
        due_date = values["due_date"]
        tasks.append(task)
        due_dates.append(due_date)
        window["tasks"].update(values=tasks)
        window["due_dates"].update(values=due_dates)
        window["task"].update(value="")
        window["due_date"].update(value="")

    if event == "Delete":
        selected_tasks = values["tasks"]
        selected_due_dates = values["due_dates"]
        for task in selected_tasks:
            index = tasks.index(task)
            tasks.pop(index)
            due_dates.pop(index)
        for due_date in selected_due_dates:
            index = due_dates.index(due_date)
            tasks.pop(index)
            due_dates.pop(index)
        window["tasks"].update(values=tasks)
        window["due_dates"].update(values=due_dates)

    if event == "Clear All":
        tasks = []
        due_dates = []
        window["tasks"].update(values=tasks)
        window["due_dates"].update(values=due_dates)

    if event == "Save":
        save_tasks(task_file, tasks, due_dates)

# Close the window when the loop exits
window.close()