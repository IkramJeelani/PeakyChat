import time
import threading

from tkinter import *
from tkinter import ttk, messagebox
from userDatabaseAPI import Db


def send(listBox, inputArea, user, receiver):
    Db.sendMessage(user.email, receiver, inputArea.get())
    listBox.insert(listBox.size(), "{}: {}".format(Db.getUserData(user.email)["username"], inputArea.get()))
    inputArea.delete(0, 'end')


def receive(listBox, receiver):
    while True:
        try:
            Db.receiveMessage(receiver, listBox)
            time.sleep(0.2)
        except:
            pass


def threads(listBox, receiver):
    t1 = threading.Thread(target=receive, args=[listBox, receiver], daemon=True)
    time.sleep(5)
    t1.start()


def chattingScreen(user, receiver):
    if receiver == Db.getUserData(user.email)["username"]:
        messagebox.showerror(title="Error", message="Cannot talk to yourself.")
    elif Db.usernameValidChecker(receiver):

        chatWindow = Toplevel()
        chatWindow.resizable(False, False)

        Label(chatWindow, text="Talking to: {}".format(receiver), font=("Helvetica", 20)).grid(row=0, column=0)

        listBox = Listbox(chatWindow, height=20, width=45)
        listBox.grid(row=1, column=0, columnspan=2)

        textEntry = Entry(chatWindow)
        textEntry.grid(row=2, column=0)

        sendButton = Button(chatWindow, text="send", font=("Helvetica", 15),
                            command=(lambda: send(listBox, textEntry, user, receiver)))
        sendButton.grid(row=2, column=1)

        t1 = threading.Thread(target=threads, args=[listBox, receiver], daemon=True)
        t1.start()

        chatWindow.mainloop()

    else:
        messagebox.showerror(title="Error", message="This username does not exist.")


def changePasswordButtonClick(user):
    user.changePassword()
    messagebox.showinfo(title="Change password", message="Check your email.")


def deleteAccountButtonClick(user, root):
    if messagebox.askyesno(title="Delete account", message="Are you sure u want to delete your account?"):
        user.deleteUser()
        Db.deleteUser(user.email)
        messagebox.showinfo(title="Account deleted", message="Please restart the application.")
        root.destroy()


def main(user):
    root = Tk()
    root.title("PeakyChat")
    root_width = 360
    root_height = 160
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (root_width / 2))
    y_coordinate = int((screen_height / 2) - (root_height / 2))
    root.geometry("{}x{}+{}+{}".format(root_width, root_height, x_coordinate, y_coordinate))
    root.resizable(False, False)
    # root.update_idletasks()  update window measurements

    notebook = ttk.Notebook(root)
    friendsTab = Frame(notebook)
    accountDetailsTab = Frame(notebook)
    notebook.add(friendsTab, text="Search")
    notebook.add(accountDetailsTab, text="Account Details")
    notebook.grid(row=0, column=0)

    nameLabel = Label(friendsTab, text="Enter the receivers username:", font=("Helvetica", 20))
    nameLabel.grid(row=0, column=0, padx=(25, 0))
    nameEntry = Entry(friendsTab, font=("Helvetica", 20))
    nameEntry.grid(row=1, column=0, padx=(25, 0))
    nameButton = Button(friendsTab, text="Start Chatting", font=("Helvetica", 20),
                        command=(lambda: chattingScreen(user, nameEntry.get())))
    nameButton.grid(row=2, column=0, padx=(25, 0))

    changePasswordButton = Button(accountDetailsTab, text="Change password",
                                  command=(lambda: changePasswordButtonClick(user)), font=("Helvetica", 20))
    changePasswordButton.pack()

    changePasswordButton = Button(accountDetailsTab, text="Delete account",
                                  command=(lambda: deleteAccountButtonClick(user, root)), font=("Helvetica", 20))
    changePasswordButton.pack()

    root.mainloop()
