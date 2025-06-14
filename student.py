#student.py
import tkinter as tk
import os
from tkinter import messagebox

# File to store student data
DATA_FILE = "student_data.txt"

# Function to load existing student data
def load_data():
    students = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():  # Skip empty lines
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            name = parts[0]
                            student_id = parts[1]
                            students.append((name, student_id))
        except Exception as e:
            print(f"Error loading data: {e}")
    return students

# Function to save student data
def save_data(data):
    with open(DATA_FILE, "w") as file:
        for name, student_id in data:
            file.write(f"{name},{student_id}\n")

def run(students_data=None, selected_index=None):
    # Load existing student data if not provided
    if students_data is None:
        students_data = load_data()
    
    # Store the original index for update operations
    original_index = selected_index
    
    app = tk.Tk()
    app.geometry("400x400+400+100")
    app.config(bg='lightblue')
    app.title("StuInfo")

    def add_student():
        name = stu_name.get()
        student_id = stu_id.get()

        if name and student_id:  # Check if fields are not empty
            if original_index is not None:
                # Update existing student
                students_data[original_index] = (name, student_id)
                status_label.config(text="Student updated successfully!")
            else:
                # Add new student
                students_data.append((name, student_id))
                status_label.config(text="Student added successfully!")
            
            # Save data immediately
            save_data(students_data)
            # Clear the entry fields after adding
            stu_name.set("")
            stu_id.set("")
        else:
            status_label.config(text="Please fill in all fields!")

    def open_view_window():
        app.withdraw()  # Hide instead of destroying
        import student_view
        student_view.run(students_data, app)

    def clear_list():
        # Clear the data file and the students_data list
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all student data?"):
            students_data.clear()  # Clear the in-memory list
            save_data(students_data)  # Save empty list to file (clears the file)
            status_label.config(text="All student data cleared!")

    def save_update():
        # Get data from form
        name = stu_name.get()
        student_id = stu_id.get()
        
        if name and student_id:
            if original_index is not None and 0 <= original_index < len(students_data):
                # Update the existing student
                students_data[original_index] = (name, student_id)
                save_data(students_data)
                status_label.config(text="Student updated successfully!")
                
                # Open the view window with updated data
                app.withdraw()
                import student_view
                student_view.run(students_data, app)
            else:
                status_label.config(text="Select a valid student to update!")
        else:
            status_label.config(text="Please fill in all fields!")

    label1 = tk.Label(app, text="Student Name: ", font=('arial', 20, 'bold'), bg='lightblue')
    label1.place(relx=0.1, rely=0.1)

    stu_name = tk.StringVar()
    entry1 = tk.Entry(app, textvariable=stu_name, font=('arial', 20, 'bold'), bg='white', fg='black')
    entry1.place(relx=0.5, rely=0.1, relwidth=0.4)

    label2 = tk.Label(app, text="Student ID: ", font=('arial', 20, 'bold'), bg='lightblue')
    label2.place(relx=0.1, rely=0.2)

    stu_id = tk.StringVar()
    entry2 = tk.Entry(app, textvariable=stu_id, font=('arial', 20, 'bold'), bg='white', fg='black')
    entry2.place(relx=0.5, rely=0.2, relwidth=0.4)

    button_add = tk.Button(app, text="Add", font=('arial', 20, 'bold'), command=add_student)
    button_add.place(relx=0.1, rely=0.3, relwidth=0.2)

    button_view = tk.Button(app, text="View Information", font=('arial', 20, 'bold'), command=open_view_window)
    button_view.place(relx=0.4, rely=0.3, relwidth=0.2)

    button_clear = tk.Button(app, text="Clear", font=('arial', 20, 'bold'), command=clear_list)
    button_clear.place(relx=0.7, rely=0.3, relwidth=0.2)

    status_label = tk.Label(app, text="", font=('arial', 14), bg='lightblue')
    status_label.place(relx=0.1, rely=0.4, relwidth=0.8)

    button_update = tk.Button(app, text="Update Save", font=('arial', 20, 'bold'), command=save_update)
    button_update.place(relx=0.4, rely=0.5, relwidth=0.2)

    # If we're in update mode, pre-fill the fields
    if original_index is not None and 0 <= original_index < len(students_data):
        name, student_id = students_data[original_index]
        stu_name.set(name)
        stu_id.set(student_id)
        button_add.config(text="Update")
        status_label.config(text="Editing student information")

    app.mainloop()

if __name__ == "__main__":
    run()



import tkinter as tk
import os
from tkinter import messagebox

DATA_FILE = "student_data.txt"

def load_data():
    students = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                lines = file.readlines()
                for line in lines:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            name = parts[0]
                            student_id = parts[1]
                            students.append((name, student_id))
        except Exception as e:
            print(f"Error loading data: {e}")
    return students

def save_data(data):
    with open(DATA_FILE, "w") as file:
        for name, student_id in data:
            file.write(f"{name},{student_id}\n")

def run(students_data=None, selected_index=None):
    if students_data is None:
        students_data = load_data()

    original_index = selected_index

    app = tk.Tk()
    app.geometry("400x400+400+100")
    app.config(bg='lightblue')
    app.title("StuInfo")

    # Define StringVars early so they can be pre-filled
    stu_name = tk.StringVar()
    stu_id = tk.StringVar()

    def add_student():
        name = stu_name.get()
        student_id = stu_id.get()

        if name and student_id:
            if original_index is not None:
                students_data[original_index] = (name, student_id)
                status_label.config(text="Student updated successfully!")
            else:
                students_data.append((name, student_id))
                status_label.config(text="Student added successfully!")

            save_data(students_data)
            stu_name.set("")
            stu_id.set("")
        else:
            status_label.config(text="Please fill in all fields!")

    def open_view_window():
        app.withdraw()
        import student_view
        student_view.run(students_data, app)

    def clear_list():
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all student data?"):
            students_data.clear()
            save_data(students_data)
            status_label.config(text="All student data cleared!")

    def save_update():
        name = stu_name.get()
        student_id = stu_id.get()

        if name and student_id:
            if original_index is not None and 0 <= original_index < len(students_data):
                students_data[original_index] = (name, student_id)
                save_data(students_data)
                status_label.config(text="Student updated successfully!")
                app.withdraw()
                import student_view
                student_view.run(students_data, app)
            else:
                status_label.config(text="Select a valid student to update!")
        else:
            status_label.config(text="Please fill in all fields!")

    label1 = tk.Label(app, text="Student Name: ", font=('arial', 20, 'bold'), bg='lightblue')
    label1.place(relx=0.1, rely=0.1)

    entry1 = tk.Entry(app, textvariable=stu_name, font=('arial', 20, 'bold'), bg='white', fg='black')
    entry1.place(relx=0.5, rely=0.1, relwidth=0.4)

    label2 = tk.Label(app, text="Student ID: ", font=('arial', 20, 'bold'), bg='lightblue')
    label2.place(relx=0.1, rely=0.2)

    entry2 = tk.Entry(app, textvariable=stu_id, font=('arial', 20, 'bold'), bg='white', fg='black')
    entry2.place(relx=0.5, rely=0.2, relwidth=0.4)

    button_add = tk.Button(app, text="Add", font=('arial', 20, 'bold'), command=add_student)
    button_add.place(relx=0.1, rely=0.3, relwidth=0.2)

    button_view = tk.Button(app, text="View Information", font=('arial', 20, 'bold'), command=open_view_window)
    button_view.place(relx=0.4, rely=0.3, relwidth=0.2)

    button_clear = tk.Button(app, text="Clear", font=('arial', 20, 'bold'), command=clear_list)
    button_clear.place(relx=0.7, rely=0.3, relwidth=0.2)

    status_label = tk.Label(app, text="", font=('arial', 14), bg='lightblue')
    status_label.place(relx=0.1, rely=0.4, relwidth=0.8)

    button_update = tk.Button(app, text="Update Save", font=('arial', 20, 'bold'), command=save_update)
    button_update.place(relx=0.4, rely=0.5, relwidth=0.2)

    # Pre-fill only after defining stu_name and stu_id
    if original_index is not None and 0 <= original_index < len(students_data):
        name, student_id = students_data[original_index]
        stu_name.set(name)
        stu_id.set(student_id)
        button_add.config(text="Update")
        status_label.config(text="Editing student information")

    app.mainloop()

if __name__ == "__main__":
    run()




