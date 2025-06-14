import tkinter as tk
import os
from tkinter import messagebox

DATA_FILE = "student_data.txt"

def load_data():
    students = []
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                for line in file:
                    if line.strip():
                        parts = line.strip().split(',')
                        if len(parts) >= 2:
                            students.append((parts[0], parts[1]))
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
    app = tk.Toplevel() if tk._default_root else tk.Tk()
    app.geometry("400x400+400+100")
    app.config(bg='lightblue')
    app.title("StuInfo")

    stu_name = tk.StringVar()
    stu_id = tk.StringVar()

    def add_student():
        name = stu_name.get().strip()
        sid = stu_id.get().strip()
        if name and sid:
            if original_index is not None:
                students_data[original_index] = (name, sid)
                status_label.config(text="Student updated successfully!")
            else:
                students_data.append((name, sid))
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
        name = stu_name.get().strip()
        sid = stu_id.get().strip()
        if name and sid and original_index is not None and 0 <= original_index < len(students_data):
            students_data[original_index] = (name, sid)
            save_data(students_data)
            status_label.config(text="Student updated successfully!")
            app.withdraw()
            import student_view
            student_view.run(students_data, app)
            app.destroy()
        else:
            status_label.config(text="Please fill in all fields or select a student!")

    label1 = tk.Label(app, text="Student Name:", font=('arial', 20, 'bold'), bg='lightblue')
    label1.place(relx=0.1, rely=0.1)
    entry1 = tk.Entry(app, textvariable=stu_name, font=('arial', 20, 'bold'))
    entry1.place(relx=0.5, rely=0.1, relwidth=0.4)

    label2 = tk.Label(app, text="Student ID:", font=('arial', 20, 'bold'), bg='lightblue')
    label2.place(relx=0.1, rely=0.2)
    entry2 = tk.Entry(app, textvariable=stu_id, font=('arial', 20, 'bold'))
    entry2.place(relx=0.5, rely=0.2, relwidth=0.4)

    button_add = tk.Button(app, text="Add", font=('arial', 20, 'bold'), command=add_student)
    button_add.place(relx=0.1, rely=0.3, relwidth=0.2)

    button_view = tk.Button(app, text="View Information", font=('arial', 20, 'bold'), command=open_view_window)
    button_view.place(relx=0.4, rely=0.3, relwidth=0.2)

    button_clear = tk.Button(app, text="Clear", font=('arial', 20, 'bold'), command=clear_list)
    button_clear.place(relx=0.7, rely=0.3, relwidth=0.2)

    button_update = tk.Button(app, text="Update Save", font=('arial', 20, 'bold'), command=save_update)
    button_update.place(relx=0.4, rely=0.5, relwidth=0.2)

    status_label = tk.Label(app, text="", font=('arial', 14), bg='lightblue')
    status_label.place(relx=0.1, rely=0.4, relwidth=0.8)

    if original_index is not None and 0 <= original_index < len(students_data):
        name, sid = students_data[original_index]
        stu_name.set(name)
        stu_id.set(sid)
        button_add.place_forget()
        status_label.config(text="Editing student information")

    app.mainloop()

if __name__ == "__main__":
    run()