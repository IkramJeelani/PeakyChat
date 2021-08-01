import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class Db(object):
    cred = credentials.Certificate("chatsystem-b2907-firebase-adminsdk-whzif-d08472bc80.json")
    firebase_admin.initialize_app(cred)
    db = firestore.client()

    @classmethod
    def usernameValidChecker(cls, username):
        return False if not [user.to_dict() for user in
                             cls.db.collection("Users").where("username", "==", username).get()] else True

    @classmethod
    def emailValidChecker(cls, email):
        return False if not [user.to_dict() for user in
                             cls.db.collection("Users").where("email", "==", email).get()] else True

    @classmethod
    def getAllUsers(cls):
        return [user.to_dict() for user in cls.db.collection("Users").get()]

    @classmethod
    def getUserData(cls, email):
        return cls.db.collection("Users").document(email).get().to_dict()

    @classmethod
    def addNewUser(cls, username, email, password):
        cls.db.collection("Users").document(email).set({"username": username, "email": email, "password": password})

    @classmethod
    def sendMessage(cls, user, receiver, message):
        cls.db.collection("Users").document(user).collection("messages").add(
            {"order": len(cls.db.collection("Users").document(user).collection("messages").get()),
             "message": message,
             "sender_email": user,
             "receiver_username": receiver,
             "status": "sent"})

    @classmethod
    def receiveMessage(cls, receiver, listBox):
        mail = None
        for email in list(cls.db.collection("Users").get()):
            if cls.db.collection("Users").document(email.to_dict()["email"]).get().to_dict()["username"] == receiver:
                mail = cls.db.collection("Users").document(email.to_dict()["email"]).get().to_dict()["email"]
                break

        newlist = (sorted([i.to_dict() for i in
                           cls.db.collection("Users").document(mail).collection("messages").where("status", "==",
                                                                                                  "sent").get()],
                          key=lambda k: k['order']))
        for msg in newlist:
            cls.db.collection("Users").document(mail).collection("messages").document(
                cls.db.collection("Users").document(mail).collection("messages").where("order", "==",
                                                                                       msg["order"]).get()[
                    0].id).update({"status": "received"})
            listBox.insert(listBox.size(), f"{receiver}: {msg['message']}")

        """for user in cls.db.collection("Users").document(mail).collection("messages").where("order", "==",
                                                                                           msg["order"]).get():
            cls.db.collection("Users").document(mail).collection("messages").document(user.id).update(
                {"status": "received"})"""

    @classmethod
    def deleteUser(cls, email):
        cls.db.collection("Users").document(email).delete()
