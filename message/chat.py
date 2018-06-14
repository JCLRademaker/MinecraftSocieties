import re

class ChatClient:
    def __init__(self, agent):
        self.name = agent
        self.re_direc = re.compile("@"+ self.name)
        self.re_sendr = re.compile("<.*?>")
        self.re_alert = re.compile("Alert:")

    def ReadChat(self, chat):
        """
            Interprets all messages of a chat history
            returns:  returns a list of ChatObjects
        """

        messages = []
        for m in chat:
            inter = self.interpret(m)
            if inter:
                messages.append(inter)

        return messages

    def interpret(self, message):
        """
            Interprets a single message, returns nothing if the message is directed to another agent
            returns: returns a ChatObject
        """
        # Set the message and the sender
        sender = ""
        mess = message
        if self.re_sendr.match(message):
            msg = message.split(' ', 1)
            sender = msg[0][1:-1]

            mess = msg[1]

        # Determine the target of the message
        target = ""
        if mess[0] == "@":
            if self.re_direc.match(mess):
                target = self.name
            else:
                target = "other"

            mess = mess.split(' ', 1)[1]

        priority = 2
        # if the message starts with "Alert:" it is a message with heightened importance
        if self.re_alert.match(message):
            priority = 1
        # If the message is target to this agent, it is of highest importance
        if self.re_direc.match(message):
            priority = 0

        if target == self.name or target == "":
            return ChatObject(mess, sender, priority)

    def StageMessage(self, message, alert = False, target = ""):
        """
            Assembles a message with a target and if it is an alert or not
            Return a string with the total message
        """
        msg = ""

        if not target == "":
            msg = "@"+target + " "
        elif alert:
            msg += "Alert: "

        msg += message

        return msg

class ChatObject:
    def __init__(self, message, sender = "", priority = 2):
        self.sender = sender
        self.message = message
        self.priority = priority

    def __str__(self):
        return self.message


class Deny:
    def __init__(self, reason = ""):
        # Determine what to say in terms of the reason
        if not reason == "":
            self.message = "negative"
        else:
            self.message = "negative, because " + reason

negative = Deny()
confirm = ChatObject("affirmative")
