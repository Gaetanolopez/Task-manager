import os
from datetime import datetime, date


DATETIME_STRING_FORMAT = "%Y-%m-%d"
today = datetime.now()
#today = today.strftime(DATETIME_STRING_FORMAT)
print(today)

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

# ====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")


def reg_user():
    # Ask to enter a name to assign a new username, if exists, ask for another name
    while True:
        new_username = input("New Username: ")
        if new_username in username_password:
            print("Username already exists, try nother one.")
        else:
            break
    # ask for a password, check if matches and assign to the username
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        # - If they are the same, add them to the user.txt file,
        print("New user added")
        username_password[new_username] = new_password
        # write user.txt file and upload new username and password
        with open("user.txt", "w") as out_file:
            user_data = []
            for k in username_password:
                user_data.append(f"{k};{username_password[k]}")
            out_file.write("\n".join(user_data))

    # - Otherwise you present a relevant message.
    else:
        print("Passwords do no match")


def add_task():
    '''Allow a user to add a new task to task.txt file
                Prompt a user for the following:
                 - A username of the person whom the task is assigned to,
                 - A title of a task,
                 - A description of the task and
                 - the due date of the task.'''
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password.keys():
        return print("User does not exist. Please enter a valid username")

    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break

        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    # Then get the current date.
    curr_date = date.today()
    ''' Add the data to the file task.txt and
        Include 'No' to indicate if the task is complete.'''
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    task_list.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = []
        for t in task_list:
            str_attrs = [
                t['username'],
                t['title'],
                t['description'],
                t['due_date'].strftime(DATETIME_STRING_FORMAT),
                t['assigned_date'].strftime(DATETIME_STRING_FORMAT),
                "Yes" if t['completed'] else "No"
            ]
            task_list_to_write.append(";".join(str_attrs))
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")


def view_all():
    '''Reads the task from task.txt file and prints to the console in the
              format of Output 2 presented in the task pdf (i.e. includes spacing
              and labelling)
           '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        disp_str += f"Task Completed: \n {t['completed']}\n"
        print(disp_str)


def view_mine():
    # display the numbers and tasks of username
    for index, t in enumerate(task_list):
        if t['username'] == curr_user:
            disp_str = f"Task number {index}: \t\t {t['title']} \n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            disp_str += f"Task Completed: \n {t['completed']}\n"
            print(disp_str)

    # ask the user to edit the file or return to the menu
    select = int(input("Do you want to edit one of the tasks?type number of task or -1 to return to menu \n"))
    if select != -1:
        choose = input("mark / edit").lower()
        # if user choose to mark, change the value of the task completed as yes
        if choose == "mark":
            task_list[select]["completed"] = True
            print(task_list[select]["title"], "Marked as Completed")
            # Read file tasks.txt
            file = open("tasks.txt", "r")
            read = file.readlines()
            l = list()
            # create a list that stores the content of the file and changes the value of the marked task as completed
            for x in read:
                x.split()
                l.append(x)
            x = (l[select].split(";"))
            x[-1] = "Yes" + "\n"
            s = ""
            for h in x:
                s = s + ";" + h
            s = (s[1:])
            l[select] = s
            file.close()

            # write task.txt file with the new list updated to the completed tasks marked as Yes
            with open("tasks.txt", "w") as f:
                for line in l:
                    f.write(line)
        # if user choose edit and the task is not completed, he can decide to change username or duedate
        elif choose == "edit":
            if not task_list[select]["completed"]:
                edit = input("Choose to edit: username/duedate")
                if edit == "username":
                    username = input("Choose username to change for the task")
                    if username in username_password:
                        task_list[select]["username"] = username
                        # open the file,create a list that stores the content with a different username
                        file = open("tasks.txt", "r")
                        read = file.readlines()
                        l = list()
                        for x in read:
                            x.split()
                            l.append(x)
                        x = (l[select].split(";"))
                        x[0] = username
                        s = ""
                        for h in x:
                            s = s + ";" + h
                        s = (s[1:])
                        l[select] = s
                        file.close()

                        # Write the file with the new list and updated username
                        with open("tasks.txt", "w") as f:
                            for line in l:
                                f.write(line)
                        print("Username changed")
                    # if the username is not in the dictionary, print an error message
                    else:
                        print("Username doesn't exist")
                # if the user chooses duedate,store a value,make a new list and insert the value in the duedate key
                elif edit == "duedate":
                    due_date = input("Choose date to change duedate: example:2022-11-25")
                    task_list[select]["due_date"] = due_date
                    file = open("tasks.txt", "r")
                    read = file.readlines()
                    l = list()
                    for x in read:
                        x.split()
                        l.append(x)
                    x = (l[select].split(";"))
                    x[-2] = due_date
                    s = ""
                    for h in x:
                        s = s + ";" + h
                    s = (s[1:])
                    l[select] = s
                    file.close()
                    # write the file with the updated contents
                    with open("tasks.txt", "w") as f:
                        for line in l:
                            f.write(line)
                    print("Due date changed")
            # if the task is marked as completed, print an error message
            else:
                print("Task already completed")

def generate_reports():
    # make variable n for completed task number
    n = 0
    for t in task_list:
        if t["completed"]:
            n = n + 1
    # make a variable m uncompleted task number
    m = 0
    # make a variable overdue for overdue tasks number
    over= 0
    for t in task_list:
        if not t["completed"]:
            m = m + 1
            # tasks not completed and overdue
            if today > t["due_date"]:
                over = over + 1
                print("over",over)
    # write a new file with all the information
    with open("task_overview.txt", "w") as f:
        f.write(f"Total tasks generated = {len(task_list)} \n")
        f.write(f"Total task completed = {n} \n")
        f.write(f"Total task not completed = {m} \n")
        f.write(f"Total task not completed and overdue = {over} \n")
        f.write(f"Percentage of tasks incomplete = {(m * 100) / len(task_list)} % \n")
        over = 0
        for t in task_list:
            if today > t["due_date"]:
                over = over + 1
        f.write(f"Percentage of tasks overdue = {(over * 100) / len(task_list)} % \n")

    num_tasks = 0
    completed_tasks = 0
    non_comp_tasks = 0
    over = 0
    # check the tasks of the relative user and count them
    for t in task_list:
        if t['username'] == curr_user:
            num_tasks = num_tasks + 1
            # count completed tasks
            if t["completed"]:
                completed_tasks = completed_tasks + 1
            else:
                # count non completed tasks
                non_comp_tasks = non_comp_tasks + 1
                if today > t["due_date"]:
                    over = over + 1

    # write a new file with all the information needed
    with open("user_overview.txt", "w") as f:
        f.write(f"Total user registered = {len(username_password)} \n")
        f.write(f"Total tasks generated = {len(task_list)} \n")
        f.write(f"Total number of tasks assigned to {curr_user}: {num_tasks} \n")
        f.write(f"Percentage of tasks assigned to {curr_user} = {(num_tasks * 100) / len(task_list)} % \n")
        # if the user has more than 1 task, write as well percentage of the work done
        if num_tasks != 0:
            f.write(f"Percentage of tasks assigned to {curr_user} that have been completed = {(completed_tasks * 100) / num_tasks} % \n")
            f.write(f"Percentage of tasks assigned to {curr_user} that must be completed = {(non_comp_tasks * 100) / num_tasks} % \n")
            f.write(f"Percentage of tasks assigned to {curr_user} not completed and overdue = {(over * 100) / non_comp_tasks} % \n")

            # percentage task not completed and overdue


# MAIN PROGRAM---------------------------------------------------------------------------------------------------------------------
# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True

while True:
    # presenting the menu to the user and
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - view my task
gr - generate reports
ds - display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user()

    elif menu == 'a':
        add_task()


    elif menu == 'va':
        view_all()

    elif menu == 'vm':
        view_mine()

    elif menu == "gr":
        generate_reports()

    elif menu == 'ds' and curr_user == 'admin':
        # if the file exits, display the contents in the console
        try:
            file1 = open("task_overview.txt", "r")
            read = file1.read()
            print("Tasks overview")
            print(read)
            file1.close()

            file2 = open("user_overview.txt", "r")
            read = file2.read()
            print("User overview")
            print(read)
            file2.close()
        # if the file does not exist, call the function gr for creating new files and then display them in the console
        except:
            generate_reports()
            menu = "ds"

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")
