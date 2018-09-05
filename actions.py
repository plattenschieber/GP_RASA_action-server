from rasa_core_sdk import Action
from rasa_core_sdk.events import SlotSet

class ActionCheckRestaurants(Action):
    def name(self):
        # type: () -> Text
        return "action_check_restaurants"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

        cuisine = tracker.get_slot('cuisine')
        q = "select * from restaurants where cuisine='{0}' limit 1".format(cuisine)
        result = db.query(q)

        return [SlotSet("matches", result if result is not None else [])]
