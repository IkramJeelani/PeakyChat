import loggedIn
import re

from tkinter import *
from tkinter import ttk, messagebox
from userDatabaseAPI import *
from userAuthenticationAPI import *
from localDatabase import LocalDB

configure = {
    "apiKey": "AIzaSyBc8WNHdqe3OSifK243QRe9hcW6kt6nvtc",
    "authDomain": "chatsystem-b2907.firebaseapp.com",
    "databaseURL": "https://chatsystem-b2907-default-rtdb.firebaseio.com",
    "projectId": "chatsystem-b2907",
    "storageBucket": "chatsystem-b2907.appspot.com",
    "messagingSenderId": "513414491105",
    "appId": "1:513414491105:web:f21c4eec3f8d03505b80a0",
    "measurementId": "G-50S7ZK71V8"
}


def emailChecker(email):
    try:
        expression = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        return True if re.match(expression, email).group() == email else False
    except AttributeError:
        pass


def passwordChecker(password):
    try:
        expression = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"
        return True if re.match(expression, password).group() == password else False
    except AttributeError:
        pass


def usernameChecker(username):
    try:
        expression = r"^(?=.{6,20}$)(?![_.])(?!.*[_.]{2})[a-zA-Z0-9._]+(?<![_.])$"
        return True if re.match(expression, username).group() == username else False
    except AttributeError:
        pass


def passwordShow(button):
    if button.get() != "":
        if button.config()["show"][-1] == "*":
            button.config(show="")
        elif button.config()["show"][-1] == "":
            button.config(show="*")
    else:
        button.config(show="*")


def loginButtonLoginClick(emailEntry, passwordEntry, root, check):
    try:
        user = Login(configure, emailEntry.get(), passwordEntry.get())
        if int(check.get()) == 1:
            rememberMeChecked(emailEntry.get(), passwordEntry.get())
        root.destroy()
        loggedIn.main(user)
    except:
        messagebox.showwarning(title="Error", message="Email doesnt exist or password is wrong.")


def signUpButtonSignUpClick(username, email, password, confirmPassword):
    if ((password.get() == confirmPassword.get()) and emailChecker(email.get()) and passwordChecker(
            password.get()) and usernameChecker(username.get()) and not Db.usernameValidChecker(
        username.get()) and not Db.emailValidChecker(email.get())):
        SignUp(configure, email.get(), password.get())
        Db.addNewUser(username.get(), email.get(), password.get())
        messagebox.showinfo(title="Account created", message="Account has been successfully created. Please Login.")
        username.delete(0, 'end')
        email.delete(0, 'end')
        password.delete(0, 'end')
        confirmPassword.delete(0, 'end')
    elif not emailChecker(email.get()):
        messagebox.showwarning(title="Error", message="Enter email in correct format.")
    elif not passwordChecker(password.get()):
        messagebox.showwarning(title="Error",
                               message="Password must be atleast 6 characters long and must contain an uppercase "
                                       "characters,a lowercase characters,a number and a special character ")
    elif not usernameChecker(username.get()):
        messagebox.showwarning(title="Error", message="""1.Only contains alphanumeric characters, underscore and dot.
2.Underscore and dot can't be at the end or start of a username (e.g _username / username_ / .username / username.).
3.Underscore and dot can't be next to each other (e.g user_.name).
4.Underscore or dot can't be used multiple times in a row (e.g user__name / user..name).
5.Number of characters must be between 6 to 20.""")
    elif not (password.get() == confirmPassword.get()) and emailChecker(email.get()):
        messagebox.showwarning(title="Error", message="Passwords don't match.")
    elif Db.emailValidChecker(email.get()):
        messagebox.showwarning(title="Error", message="Email already exists.")
    elif Db.usernameValidChecker(username.get()):
        messagebox.showwarning(title="Error", message="Username already exists.")


def rememberMeChecked(email, password):
    if not LocalDB.showAll():
        LocalDB.insert(email, password)
    else:
        LocalDB.update(1, email, password)


def authenticationGUI():
    root = Tk()
    root.title("PeakyChat")
    root_width = 530
    root_height = 450
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_coordinate = int((screen_width / 2) - (root_width / 2))
    y_coordinate = int((screen_height / 2) - (root_height / 2))
    root.geometry("{}x{}+{}+{}".format(root_width, root_height, x_coordinate, y_coordinate))
    root.resizable(False, False)
    # root.update_idletasks()  update window measurements

    notebook = ttk.Notebook(root)
    loginTab = Frame(notebook)
    signupTab = Frame(notebook)
    notebook.add(loginTab, text="Login")
    notebook.add(signupTab, text="Sign up")
    notebook.grid(row=0, column=0)

    # LOGIN
    affirmativeLabelLogin = Label(loginTab, text="PeakyChat", font=("Helvetica", 50), fg="black", padx=10, pady=10)
    affirmativeLabelLogin.grid(row=0, column=1, pady=(5, 30))

    emailLabelLogin = Label(loginTab, text="Email:", font=("Helvetica", 20), fg="black")
    emailLabelLogin.grid(row=1, column=0)
    emailEntryLogin = Entry(loginTab, font=("Helvetica", 20), width=30)
    emailEntryLogin.grid(row=1, column=1, pady=10, columnspan=2)

    passwordLabelLogin = Label(loginTab, text="Password:", font=("Helvetica", 20), fg="black")
    passwordLabelLogin.grid(row=2, column=0)
    passwordEntryLogin = Entry(loginTab, show="*", font=("Helvetica", 20))  # , width=30
    passwordEntryLogin.grid(row=2, column=1, pady=10, sticky="w")
    passwordShowButtonLogin = ttk.Button(loginTab, text="Show", command=(lambda: passwordShow(passwordEntryLogin)))
    passwordShowButtonLogin.grid(row=2, column=2, sticky="w")

    check = IntVar()
    rememberMeLogin = ttk.Checkbutton(loginTab, text="remember me", variable=check,
                                  onvalue=1, offvalue=0)
    rememberMeLogin.grid(row=3, column=0, columnspan=3, pady=(15, 0), ipady=5, ipadx=5)

    loginButtonLogin = ttk.Button(loginTab, text="Login", command=(
        lambda: loginButtonLoginClick(emailEntryLogin, passwordEntryLogin, root, check)))
    loginButtonLogin.grid(row=4, column=0, columnspan=3, pady=(15, 0), ipady=5, ipadx=5)

    # SIGN UP
    affirmativeLabelLogin = Label(signupTab, text="PeakyChat", font=("Helvetica", 50), fg="black", padx=10, pady=10)
    affirmativeLabelLogin.grid(row=0, column=1, pady=(5, 30))

    userNameLabel = Label(signupTab, text="User\nname:", font=("Helvetica", 20), fg="black")
    userNameLabel.grid(row=1, column=0)
    userNameEntry = Entry(signupTab, font=("Helvetica", 20), width=30)
    userNameEntry.grid(row=1, column=1, pady=10, columnspan=2)

    emailLabelSignUp = Label(signupTab, text="Email:", font=("Helvetica", 20), fg="black")
    emailLabelSignUp.grid(row=2, column=0)
    emailEntrySignUp = Entry(signupTab, font=("Helvetica", 20), width=30)
    emailEntrySignUp.grid(row=2, column=1, pady=10, columnspan=2)

    passwordLabelSignUp = Label(signupTab, text="Password:", font=("Helvetica", 20), fg="black")
    passwordLabelSignUp.grid(row=3, column=0)
    passwordEntrySignUp = Entry(signupTab, show="*", font=("Helvetica", 20))
    passwordEntrySignUp.grid(row=3, column=1, pady=10, sticky="w")
    passwordShowButtonSignUp = ttk.Button(signupTab, text="Show", command=(lambda: passwordShow(passwordEntrySignUp)))
    passwordShowButtonSignUp.grid(row=3, column=2, sticky="w")

    confirmPasswordLabelSignUp = Label(signupTab, text="Confirm\npassword:", font=("Helvetica", 20), fg="black")
    confirmPasswordLabelSignUp.grid(row=4, column=0)
    confirmPasswordEntrySignUp = Entry(signupTab, show="*", font=("Helvetica", 20), width=30)
    confirmPasswordEntrySignUp.grid(row=4, column=1, pady=10, sticky="w", columnspan=2)

    signUpButtonSignUp = ttk.Button(signupTab, text="Sign up",
                                    command=lambda: signUpButtonSignUpClick(userNameEntry, emailEntrySignUp,
                                                                            passwordEntrySignUp,
                                                                            confirmPasswordEntrySignUp))
    signUpButtonSignUp.grid(row=5, column=0, columnspan=3, pady=(15, 5), ipady=5, ipadx=5)

    root.update_idletasks()

    try:
        emailEntryLogin.insert(0, str(LocalDB.showAll()[0][1]))
        passwordEntryLogin.insert(0, str(LocalDB.showAll()[0][2]))
        rememberMeLogin.state(['selected'])
    except IndexError:
        pass

    root.mainloop()


if __name__ == '__main__':
    authenticationGUI()
