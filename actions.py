from rasa_core_sdk import Action
from rasa_core_sdk.events import ConversationResumed, UserUtteranceReverted, SlotSet
import smtplib
import email.message
import io
from rasa_core_sdk.events import SlotSet
from rasa_core_sdk.forms import FormAction
from rasa_core_sdk.forms import EntityFormField
from rasa_core_sdk.forms import BooleanFormField


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
        form_of_address = tracker.get_slot("form_of_address")
        first_name = tracker.get_slot("PER")
        surname = tracker.get_slot("surname")
        street_address = tracker.get_slot("street_address")
        street_number = tracker.get_slot("street_number")
        address_zip_code = tracker.get_slot("address_zip_code")
        address_city = tracker.get_slot("address_city")
        phone_number = tracker.get_slot("phone-number")
        email = tracker.get_slot("email")
        business_affair = tracker.get_slot("business_affair")

        if tracker.get_slot("car_is_damaged") == True:
            car_is_damaged = "Ja"
        else:
            car_is_damaged = "Nein"

        counterpart_is_insured = tracker.get_slot("counterpart_is_insured")
        damage_from_own_car = tracker.get_slot("damage_from_own_car")
        first_name_insured_party = tracker.get_slot("first_name_insured_party")
        surname_insured_party = tracker.get_slot("surname_insured_party")
        insurance_number = tracker.get_slot("insurance_number")
        first_name_victim = tracker.get_slot("first_name_victim")
        surname_victim = tracker.get_slot("surname_victim")
        phone_number_victim = tracker.get_slot("phone_number_victim")
        insurance_number_victim = tracker.get_slot("insurance_number_victim")
        insured_party_is_driver = tracker.get_slot("insured_party_is_driver")
        license_plate = tracker.get_slot("license_plate")
        date_of_damage = tracker.get_slot("date_of_damage")
        time_of_damage = tracker.get_slot("time_of_damage")
        cause_of_damage = tracker.get_slot("cause_of_damage")
        damage_location = tracker.get_slot("damage_location")
        description_of_accident = tracker.get_slot("description_of_accident")
        current_location_of_car = tracker.get_slot("current_location_of_car")
        if tracker.get_slot("is_callback_wanted") == True:
            callback_phone_number = tracker.get_slot("callback_phone_number")
        else:
            callback_phone_number = "-"
        form_of_address_of_driver = tracker.get_slot("form_of_address_of_driver")
        first_name_of_driver = tracker.get_slot("first_name_of_driver")
        surname_of_driver = tracker.get_slot("surname_of_driver")
        birth_date_of_driver = tracker.get_slot("birth_date_of_driver")
        visible_damage_before = tracker.get_slot("visible_damage_before")
        visible_damage_after = tracker.get_slot("visible_damage_after")
        collateral_damage_claimed = tracker.get_slot("collateral_damage_claimed")
        vorsteuerabzugsberechtigt = tracker.get_slot("vorsteuerabzugsberechtigt")
        name_address_if_workshop = tracker.get_slot("name_address_if_workshop")
        phone_number_if_workshop = tracker.get_slot("phone_number_if_workshop")
        damage_report_by_if_not_insured = tracker.get_slot("damage_report_by_if_not_insured")
        accident_caused_by = tracker.get_slot("accident_caused_by")
        form_of_address_victim = tracker.get_slot("form_of_address_victim")
        street_address_victim = tracker.get_slot("street_address_victim")
        address_zip_code_victim = tracker.get_slot("address_zip_code_victim")
        address_city_victim = tracker.get_slot("address_city_victim")
        current_location_of_car_victim = tracker.get_slot("current_location_of_car_victim")
        name_address_if_workshop_victim = tracker.get_slot("name_address_if_workshop_victim")
        phone_number_if_workshop_victim = tracker.get_slot("phone_number_if_workshop_victim")
        someone_injured = tracker.get_slot("someone_injured")
        damage_report_by = tracker.get_slot("damage_report_by")

        # Überprüfung, wer der Fahrer war:
        if(insured_party_is_driver == True):
            surname_of_driver = surname
            first_name_of_driver = first_name

        # endregion data
        print("Daten geladen")
        # create message object instance
        msg = email.message.Message()

        # Open HTML File
        file = io.open("robotics_fixed.html", "r", encoding='utf-8').read()

        # region fill email_content
        email_content = file.format(form_of_address=form_of_address, surname=surname, first_name=first_name,
                                    street_address=street_address,
                                    street_number= street_number,
                                    address_zip_code=address_zip_code, address_city=address_city,
                                    phone_number=phone_number, email=email, insurance_number=insurance_number,
                                    license_plate=license_plate, car_is_damaged=car_is_damaged,
                                    current_location_of_car=current_location_of_car, date_of_damage=date_of_damage,
                                    damage_location=damage_location, cause_of_damage=cause_of_damage,
                                    description_of_accident=description_of_accident,
                                    first_name_of_driver=first_name_of_driver, surname_of_driver=surname_of_driver,
                                    first_name_victim=first_name_victim,
                                    surname_victim=surname_victim,
                                    phone_number_victim=phone_number_victim,
                                    time_of_damage=time_of_damage, birth_date_of_driver=birth_date_of_driver,
                                    form_of_address_of_driver=form_of_address_of_driver,
                                    visible_damage_before=visible_damage_before,
                                    visible_damage_after=visible_damage_after,
                                    callback_phone_number=callback_phone_number,
                                    collateral_damage_claimed=collateral_damage_claimed,
                                    vorsteuerabzugsberechtigt=vorsteuerabzugsberechtigt,
                                    name_address_if_workshop=name_address_if_workshop,
                                    phone_number_if_workshop=phone_number_if_workshop,
                                    damage_report_by_if_not_insured=damage_report_by_if_not_insured,
                                    accident_caused_by=accident_caused_by,
                                    form_of_address_victim=form_of_address_victim,
                                    street_address_victim=street_address_victim,
                                    address_zip_code_victim=address_zip_code_victim,
                                    address_city_victim=address_city_victim,
                                    current_location_of_car_victim=current_location_of_car_victim,
                                    name_address_if_workshop_victim=name_address_if_workshop_victim,
                                    phone_number_if_workshop_victim=phone_number_if_workshop_victim,
                                    someone_injured=someone_injured,
                                    damage_report_by=damage_report_by
                                    )
        # endregion fill email_content

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


class ActionAskContactDetails(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("form_of_address", "form_of_address"),
            EntityFormField("entity_PER", "PER"),
            EntityFormField("surname", "surname"),
            EntityFormField("street_address", "street_address"),
            EntityFormField("number", "number"),
            EntityFormField("address_city", "address_city"),
            EntityFormField("phone-number", "phone-number"),
            EntityFormField("email", "email"),
            BooleanFormField("business_affair", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_contact_details'

    def submit(self, dispatcher, tracker, domain):
        SlotSet("address_zip_code", tracker.get_slot("number"))
        SlotSet("phone_number_user", tracker.get_slot("phone-number"))
        return []

class ActionSaveStreetNumber(Action):
    def name(self):
        return "action_save_street_number"

    def run(self, dispatcher, tracker, domain):
        SlotSet("street_number", tracker.get_slot("number"))
        return []

class ActionAskBranch(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("branch", "branch")
        ]

    def name(self):
        return 'action_ask_branch'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskCarIsDamaged(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            BooleanFormField("car_is_damaged", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_car_is_damaged'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskCounterpartInsuredAtZurich(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            BooleanFormField("counterpart_is_insured", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_counterpart_insured_at_zurich'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskLiabilityContactData(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("first_name_insured_party", "first_name_insured_party"),
            EntityFormField("surname_insured_party", "surname_insured_party"),
            EntityFormField("number", "number")
        ]

    def name(self):
        return 'action_ask_liability_contact_data'

    def submit(self, dispatcher, tracker, domain):
        SlotSet("insurance_number", tracker.get_slot("number"))
        return []


class ActionAskKFZ(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("license_plate", "license_plate"),
            EntityFormField("time", "time"),
            EntityFormField("cause_of_damage", "cause_of_damage"),
            EntityFormField("damage_location", "damage_location"),
            EntityFormField("description_of_accident", "description_of_accident"),
            EntityFormField("current_location_of_car", "current_location_of_car")
        ]

    def name(self):
        return 'action_ask_kfz'

    def submit(self, dispatcher, tracker, domain):
        SlotSet("date_of_damage", tracker.get_slot("time"))
        return []


class ActionAskIsCallbackWanted(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            BooleanFormField("is_callback_wanted", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_is_callback_wanted'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskCallbackPhoneNumber(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("phone-number", "phone-number"),
            EntityFormField("reachability_date", "reachability_date")
        ]

    def name(self):
        return 'action_ask_callback_information'

    def submit(self, dispatcher, tracker, domain):
        SlotSet("callback_phone_number", "phone-number")
        return []


class ActionAskIsDamageCausedByOwnCar(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            BooleanFormField("damage_from_own_car", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_is_damage_caused_by_own_car'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskKFZOtherParty(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("first_name_insured_party", "first_name_insured_party"),
            EntityFormField("surname_insured_party", "surname_insured_party"),
            EntityFormField("insurance_number", "insurance_number")
        ]

    def name(self):
        return 'action_ask_kfz_other_party'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskInsuredPartyDriver(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            BooleanFormField("insured_party_is_driver", "confirm", "deny")
        ]

    def name(self):
        return 'action_ask_insured_party_driver'

    def submit(self, dispatcher, tracker, domain):
        return []


class ActionAskInsuredPartyDriverInformations(FormAction):

    RANDOMIZE = False

    @staticmethod
    def required_fields():
        return [
            EntityFormField("form_of_address_of_driver", "form_of_address_of_driver"),
            EntityFormField("first_name_of_driver", "first_name_of_driver"),
            EntityFormField("surname_of_driver", "surname_of_driver"),
            EntityFormField("birth_date_of_driver", "birth_date_of_driver")
        ]

    def name(self):
        return 'action_ask_insured_party_driver_informations'

    def submit(self, dispatcher, tracker, domain):
        return []

# DONT DELETE THIS ONE
class ActionSafeStreetAddress(Action):
    def name(self):
        return "action_safe_street_address"

    def run(self, dispatcher, tracker, domain):
        street = tracker.get_slot("street")
        house_number = tracker.get_slot("house_number")

        return [SlotSet("street_address", str(street + " " + house_number))]