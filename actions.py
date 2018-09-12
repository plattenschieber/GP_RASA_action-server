from rasa_core_sdk import Action
from rasa_core_sdk.events import ConversationResumed, UserUtteranceReverted, SlotSet
import smtplib
import email.message
import io


class ActionSetBusinessAffair(Action):
    def name(self):
        return "action_set_business_affair"

    def run(self, dispatcher, tracker, domain):
        business_affair = next(tracker.get_latest_entity_values('business_affair'), None)

        if not business_affair:
            dispatcher.utter_message("Please rephrase it again")
            return [UserUtteranceReverted()]
        elif business_affair == "ja" or business_affair == "richtig" or business_affair == "korrekt" or business_affair == "genau":
            return [SlotSet("business_affair", True)]
        else:
            return [SlotSet("business_affair", False)]

class SendEmail(Action):
    def name(self):
        # type: () -> Text
        return "action_save_address"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        # Dispatcher: send messages back to the user
        # DialogueStateTracker:  the state tracker for the current user. You can access slot values using
        # tracker.get_slot(slot_name) and the most recent user message is tracker.latest_message.text

        address = tracker.get_slot("address_street")
        address_number = tracker.get_slot("address_street_number")
        print("String Adresse: ", address, address_number)

        #create message object instance
        msg = email.message.Message()

        #Open HTML File
        file = io.open("robotics_fixed.html", "r", encoding='utf-8').read()

        email_content = file.format(code=address_number, address=address)

        # setup the parameters of the message
        password = "GuidedProjectWS18/19"
        msg['From'] = "chat.bot.send@gmail.com"
        msg['To'] = "chat.bot.send@gmail.com"
        msg['Subject'] = "Sparte KFZ"
        msg.add_header('Content-Type', 'text/html')
        msg.set_payload(email_content)

        # create server
        server = smtplib.SMTP('smtp.gmail.com:587')
        server.starttls()

        # Login Credentials for sending the mail
        server.login(msg['From'], password)

        # send the message via the server.
        server.sendmail(msg['From'], msg['To'], msg.as_string().encode('utf-8'))

        server.quit()

        dispatcher.utter_message("Email Send..")

        print(tracker.latest_message)

        return [ConversationResumed()]