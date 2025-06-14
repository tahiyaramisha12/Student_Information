# import tkinter as tk
# import os
# from tkinter import messagebox

# DATA_FILE = "student_data.txt"

# def load_data():
#     students = []
#     if os.path.exists(DATA_FILE):
#         try:
#             with open(DATA_FILE, "r") as file:
#                 for line in file:
#                     if line.strip():
#                         parts = line.strip().split(',')
#                         if len(parts) >= 2:
#                             students.append((parts[0], parts[1]))
#         except Exception as e:
#             print(f"Error loading data: {e}")
#     return students

# def save_data(data):
#     with open(DATA_FILE, "w") as file:
#         for name, student_id in data:
#             file.write(f"{name},{student_id}\n")

# def run(students_data=None, selected_index=None):
#     if students_data is None:
#         students_data = load_data()

#     original_index = selected_index
#     app = tk.Toplevel() if tk._default_root else tk.Tk()
#     app.geometry("400x400+400+100")
#     app.config(bg='lightblue')
#     app.title("StuInfo")

#     stu_name = tk.StringVar()
#     stu_id = tk.StringVar()

#     def add_student():
#         name = stu_name.get().strip()
#         sid = stu_id.get().strip()
#         if name and sid:
#             if original_index is not None:
#                 students_data[original_index] = (name, sid)
#                 status_label.config(text="Student updated successfully!")
#             else:
#                 students_data.append((name, sid))
#                 status_label.config(text="Student added successfully!")
#             save_data(students_data)
#             stu_name.set("")
#             stu_id.set("")
#         else:
#             status_label.config(text="Please fill in all fields!")

#     def open_view_window():
#         app.withdraw()
#         import student_view
#         student_view.run(students_data, app)

#     def clear_list():
#         if messagebox.askyesno("Confirm", "Are you sure you want to clear all student data?"):
#             students_data.clear()
#             save_data(students_data)
#             status_label.config(text="All student data cleared!")

#     def save_update():
#         name = stu_name.get().strip()
#         sid = stu_id.get().strip()
#         if name and sid and original_index is not None and 0 <= original_index < len(students_data):
#             students_data[original_index] = (name, sid)
#             save_data(students_data)
#             status_label.config(text="Student updated successfully!")
#             app.withdraw()
#             import student_view
#             student_view.run(students_data, app)
#             app.destroy()
#         else:
#             status_label.config(text="Please fill in all fields or select a student!")

#     # GUI Layout
#     label1 = tk.Label(app, text="Student Name:", font=('arial', 20, 'bold'), bg='lightblue')
#     label1.place(relx=0.1, rely=0.1)
#     entry1 = tk.Entry(app, textvariable=stu_name, font=('arial', 20, 'bold'))
#     entry1.place(relx=0.5, rely=0.1, relwidth=0.4)

#     label2 = tk.Label(app, text="Student ID:", font=('arial', 20, 'bold'), bg='lightblue')
#     label2.place(relx=0.1, rely=0.2)
#     entry2 = tk.Entry(app, textvariable=stu_id, font=('arial', 20, 'bold'))
#     entry2.place(relx=0.5, rely=0.2, relwidth=0.4)

#     # Dropdown menu for all actions
#     dropdown_label = tk.Label(app, text="Select Action:", font=('arial', 16), bg='lightblue')
#     dropdown_label.place(relx=0.1, rely=0.3)

#     options = ["➕ Add", "👁️ View", "❌ Clear", "💾 Update Save"]
#     selected_option = tk.StringVar(value=options[0])
#     action_menu = tk.OptionMenu(app, selected_option, *options)
#     action_menu.config(font=('arial', 16))
#     action_menu.place(relx=0.5, rely=0.3, relwidth=0.4)

#     def perform_action():
#         action = selected_option.get()
#         if action == "➕ Add":
#             add_student()
#         elif action == "👁️ View":
#             open_view_window()
#         elif action == "❌ Clear":
#             clear_list()
#         elif action == "💾 Update Save":
#             save_update()

#     go_button = tk.Button(app, text="Go", font=('arial', 16, 'bold'), command=perform_action)
#     go_button.place(relx=0.4, rely=0.4, relwidth=0.2)

#     status_label = tk.Label(app, text="", font=('arial', 14), bg='lightblue')
#     status_label.place(relx=0.1, rely=0.5, relwidth=0.8)

#     # Preload values if editing
#     if original_index is not None and 0 <= original_index < len(students_data):
#         name, sid = students_data[original_index]
#         stu_name.set(name)
#         stu_id.set(sid)
#         status_label.config(text="Editing student information")

#     app.mainloop()

# if __name__ == "__main__":
#     run()



import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk  # For dynamic background resizing
import os

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
    app.geometry("600x500+400+100")  # Start with larger size
    app.title("StuInfo")

    stu_name = tk.StringVar()
    stu_id = tk.StringVar()

    # === Load and prepare background image ===
    original_image = Image.open("background.png")  # Use PNG or JPG
    bg_label = tk.Label(app)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    def resize_bg(event):
        resized = original_image.resize((event.width, event.height), Image.ANTIALIAS)
        app.bg_image = ImageTk.PhotoImage(resized)
        bg_label.config(image=app.bg_image)

    app.bind("<Configure>", resize_bg)

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

    # ===== GUI Widgets (overlayed on background) =====
    label1 = tk.Label(app, text="Student Name:", font=('arial', 20, 'bold'), bg='lightblue')
    label1.place(relx=0.1, rely=0.1)
    entry1 = tk.Entry(app, textvariable=stu_name, font=('arial', 20, 'bold'))
    entry1.place(relx=0.5, rely=0.1, relwidth=0.4)

    label2 = tk.Label(app, text="Student ID:", font=('arial', 20, 'bold'), bg='lightblue')
    label2.place(relx=0.1, rely=0.2)
    entry2 = tk.Entry(app, textvariable=stu_id, font=('arial', 20, 'bold'))
    entry2.place(relx=0.5, rely=0.2, relwidth=0.4)

    dropdown_label = tk.Label(app, text="Select Action:", font=('arial', 16), bg='lightblue')
    dropdown_label.place(relx=0.1, rely=0.3)

    options = ["➕ Add", "👁️ View", "❌ Clear", "💾 Update Save"]
    selected_option = tk.StringVar(value=options[0])
    action_menu = tk.OptionMenu(app, selected_option, *options)
    action_menu.config(font=('arial', 16))
    action_menu.place(relx=0.5, rely=0.3, relwidth=0.4)

    def perform_action():
        action = selected_option.get()
        if action == "➕ Add":
            add_student()
        elif action == "👁️ View":
            open_view_window()
        elif action == "❌ Clear":
            clear_list()
        elif action == "💾 Update Save":
            save_update()

    go_button = tk.Button(app, text="Go", font=('arial', 16, 'bold'), command=perform_action)
    go_button.place(relx=0.4, rely=0.4, relwidth=0.2)

    status_label = tk.Label(app, text="", font=('arial', 14))
    status_label.place(relx=0.1, rely=0.5, relwidth=0.8)

    if original_index is not None and 0 <= original_index < len(students_data):
        name, sid = students_data[original_index]
        stu_name.set(name)
        stu_id.set(sid)
        status_label.config(text="Editing student information")

    app.mainloop()

if __name__ == "__main__":
    run()
