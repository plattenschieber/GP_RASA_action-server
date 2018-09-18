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
            dispatcher.utter_message("Ich habe Sie nicht verstanden. Formulieren Sie bitte ihre letzte Nachricht um")
            return [UserUtteranceReverted()]
        elif business_affair == "ja" or business_affair == "richtig" or business_affair == "korrekt" or business_affair == "genau":
            return [SlotSet('business_affair', True)]
        else:
            return [SlotSet('business_affair', False)]

class ActionIsCarDamaged(Action):
    def name(self):
        return "action_is_car_damaged"

    def run(self, dispatcher, tracker, domain):
        car_is_damaged = next(tracker.get_latest_entity_values('car_is_damaged'), None)

        if not car_is_damaged:
            dispatcher.utter_message("Please rephrase it again")
            return [UserUtteranceReverted()]
        elif car_is_damaged == "wahr" or car_is_damaged == "beschädigt" or car_is_damaged == "ja":
            return [SlotSet("car_is_damaged", True)]
        elif car_is_damaged == "falsch" or car_is_damaged == "unbeschädigt" or car_is_damaged == "nein":
            return [SlotSet("car_is_damaged", False)]
        else:
            return [SlotSet("car_is_damaged", False)]

class ActionSendEmail(Action):
    def name(self):
        # type: () -> Text
        return "action_send_email"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]
        # Dispatcher: send messages back to the user
        # DialogueStateTracker:  the state tracker for the current user. You can access slot values using
        # tracker.get_slot(slot_name) and the most recent user message is tracker.latest_message.text

        print("In Methode")
        # region data
        form_of_address = tracker.get_slot("form_of_address")
        first_name = tracker.get_slot("first_name")
        surname = tracker.get_slot("surname")
        address_street = tracker.get_slot("address_street")
        address_street_number = tracker.get_slot("address_street_number")
        address_zip_code = tracker.get_slot("address_zip_code")
        address_city = tracker.get_slot("address_city")
        phone_number = tracker.get_slot("phone_number")
        e_mail = tracker.get_slot("e_mail")
        business_affair = tracker.get_slot("business_affair")
        car_is_damaged = tracker.get_slot("car_is_damaged")
        counterpart_is_insured = tracker.get_slot("counterpart_is_insured")
        damage_from_own_car = tracker.get_slot("damage_from_own_car")
        first_name_insured_party = tracker.get_slot("first_name_insured_party")
        surname_insured_party = tracker.get_slot("surname_insured_party")
        insurance_number = tracker.get_slot("insurance_number")
        first_name_injured_party = tracker.get_slot("first_name_injured_party")
        surname_injured_party = tracker.get_slot("surname_injured_party")
        phone_number_injured_party = tracker.get_slot("phone_number_injured_party")
        insurance_number_injured_party = tracker.get_slot("insurance_number_injured_party")
        insured_party_is_driver = tracker.get_slot("insured_party_is_driver")
        license_plate = tracker.get_slot("license_plate")
        date_of_damage = tracker.get_slot("date_of_damage")
        cause_of_damage = tracker.get_slot("cause_of_damage")
        damage_location = tracker.get_slot("damage_location")
        description_of_accident = tracker.get_slot("description_of_accident")
        current_location_of_car = tracker.get_slot("current_location_of_car")
        is_callback_wanted = tracker.get_slot("is_callback_wanted")
        # Überprüfung, wer der Fahrer war:
        surname_of_driver = "Keine Angabe"
        first_name_of_driver = "Keine Angabe"
        if(insured_party_is_driver == True):
            surname_of_driver = surname_insured_party
            first_name_of_driver = first_name_insured_party
        else:
            surname_of_driver = "TBD: Name des Geschädigten"
            first_name_of_driver = "TBD: Name des Geschädigten"

        # endregion data
        print("Daten geladen")
        # create message object instance
        msg = email.message.Message()

        # Open HTML File
        file = io.open("robotics_fixed.html", "r", encoding='utf-8').read()

        email_content = file.format(form_of_address=form_of_address, surname=surname, first_name=first_name,
                                    address_street=address_street, address_street_number=address_street_number,
                                    address_zip_code=address_zip_code, address_city=address_city,
                                    phone_number=phone_number, e_mail=e_mail, insurance_number=insurance_number,
                                    license_plate=license_plate, car_is_damaged=car_is_damaged,
                                    current_location_of_car=current_location_of_car, date_of_damage=date_of_damage,
                                    damage_location=damage_location, cause_of_damage=cause_of_damage,
                                    description_of_accident=description_of_accident,
                                    first_name_of_driver=first_name_of_driver, surname_of_driver=surname_of_driver,
                                    first_name_injured_party=first_name_injured_party,
                                    surname_injured_party=surname_injured_party,
                                    phone_number_injured_party=phone_number_injured_party)

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

class ActionSetCallback(Action):
    def name(self):
        return "action_set_callback"

    def run(self, dispatcher, tracker, domain):
        is_callback_wanted = next(tracker.get_latest_entity_values('is_callback_wanted'), None)

        if not is_callback_wanted:
            dispatcher.utter_message("Ich habe Sie nicht verstanden. Formulieren Sie bitte ihre letzte Nachricht um")
            return [UserUtteranceReverted()]
        elif is_callback_wanted == "ja" or is_callback_wanted == "gerne":
            return [SlotSet('is_callback_wanted', True)]
        else:
            return [SlotSet('is_callback_wanted', False)]