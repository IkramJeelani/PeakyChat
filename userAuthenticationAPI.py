import pyrebase
from abc import abstractmethod, ABC

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


class LoginError(Exception):
    """Error while logging in"""


class SignUpError(Exception):
    """Error while Signing Up"""


class Authentication(ABC):

    @abstractmethod
    def __init__(self, config, email, password):
        self.config = config
        self.firebase = pyrebase.initialize_app(config)
        self.auth = self.firebase.auth()
        self.email = email
        self.password = password
        self.user = None

    def userInfo(self):
        return self.auth.get_account_info(self.user["idToken"])

    def verifyEmail(self):
        self.auth.send_email_verification(self.user["idToken"])

    def changePassword(self):
        self.auth.send_password_reset_email(self.email)

    def checkVerified(self):
        # print(self.auth.get_account_info(self.user["idToken"]))
        return self.auth.get_account_info(self.user["idToken"])["users"][0]["emailVerified"]

    def deleteUser(self):
        self.auth.delete_user_account(self.user["idToken"])


class Login(Authentication):
    def __init__(self, config, email, password):
        super().__init__(config, email, password)
        try:
            self.user = self.auth.sign_in_with_email_and_password(self.email, self.password)
        except:
            raise LoginError("Error while logging in")


class SignUp(Authentication):
    def __init__(self, config, email, password):
        super().__init__(config, email, password)
        try:
            self.user = self.auth.create_user_with_email_and_password(self.email, self.password)
        except:
            raise SignUpError("Error while Signing Up")
