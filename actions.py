import email.message
import io
import smtplib

from rasa_core_sdk import Action
from rasa_core_sdk.events import ConversationResumed, UserUtteranceReverted
from rasa_core_sdk.events import SlotSet


class ActionSaveDamageTime(Action):
    def name(self):
        # type: () -> Text
        return "action_save_damage_time"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("damage_time", tracker.get_slot("time"))]


class ActionSaveCallbackTime(Action):
    def name(self):
        # type: () -> Text
        return "action_save_callback_time"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("callback_time", tracker.get_slot("time"))]


class ActionSaveUserPhoneNumber(Action):
    def name(self):
        # type: () -> Text
        return "action_save_user_phone_number"

    def run(self, dispatcher, tracker, domain):

        if tracker.get_slot("phone-number") and tracker.get_slot("crf-phone-number") is not None:
            user_phone = tracker.get_slot("crf-phone-number")
            return [SlotSet("user_phone_number", user_phone)]
        if tracker.get_slot("phone-number") is not None:
            user_phone = tracker.get_slot("phone-number")
            return [SlotSet("user_phone_number", user_phone)]
        if tracker.get_slot("crf-phone-number") is not None:
            user_phone = tracker.get_slot("crf-phone-number")
            return [SlotSet("user_phone_number", user_phone)]


class ActionSaveUserEmail(Action):
    def name(self):
        # type: () -> Text
        return "action_save_user_email"

    def run(self, dispatcher, tracker, domain):
        return [SlotSet("user_email", tracker.get_slot("email"))]


class ActionSaveStreetAddress(Action):
    def name(self):
        return "action_save_street_address"

    def run(self, dispatcher, tracker, domain):
        street = next(tracker.get_latest_entity_values('street'), None)
        house_number = next(tracker.get_latest_entity_values('house_number'), None)

        if not street:
            dispatcher.utter_message("Bitte geben Sie den Straßennamen zusätzlich zu Ihrer Hausnummer an")
            return [UserUtteranceReverted()]
        elif not house_number:
            dispatcher.utter_message("Bitte geben Sie die Hausnummer zusätzlich zu Ihrem Straßennamen an")
            return [UserUtteranceReverted()]

        return [SlotSet("street_address", str(street + " " + house_number))]


class ActionSaveZipCity(Action):
    def name(self):
        return "action_save_zip_city"

    def run(self, dispatcher, tracker, domain):
        zip_code = tracker.get_slot("zip")
        city = tracker.get_slot("city")

        if zip_code is None:
            dispatcher.utter_message("Bitte schreiben Sie auch ihre Postleitzahl gemeinsam mit Ihrem Wohnort")
            return [UserUtteranceReverted()]
        elif city is None:
            dispatcher.utter_message("Bitte schreiben Sie auch ihr Wohnort gemeinsam mit Ihrer Postleitzahl")
            return [UserUtteranceReverted()]

        return [SlotSet("zip_city", str(zip_code + " " + city))]


class ActionSendEmail(Action):
    def name(self):
        # type: () -> Text
        return "action_send_email"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        # Dispatcher: send messages back to the user
        # DialogueStateTracker:  the state tracker for the current user. You can access slot values using
        # tracker.get_slot(slot_name) and the most recent user message is tracker.latest_message.text

        # region data
        street = tracker.get_slot("street")
        house_number = tracker.get_slot("house_number")
        user_phone_number = tracker.get_slot("user_phone_number")
        first_name = tracker.get_slot("first_name")
        last_name = tracker.get_slot("last_name")
        user_email = tracker.get_slot("user_email")
        damage_time = tracker.get_slot("damage_time")
        # endregion data
        print("Daten geladen")
        # create message object instance
        msg = email.message.Message()

        # Open HTML File
        file = io.open("robotics_fixed.html", "r", encoding='utf-8').read()

        # fill email_content
        email_content = file.format(street=street, house_number=house_number, user_phone_number=user_phone_number,
                                    first_name=first_name, last_name=last_name, user_email=user_email,
                                    damage_time=damage_time)

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

        print(tracker.latest_message)

        return [ConversationResumed()]
