from rasa_core_sdk import Action
from rasa_core_sdk.events import ConversationResumed


class ActionPrintTest(Action):
    def name(self):
        # type: () -> Text
        return "action_print_test"

    def run(self, dispatcher, tracker, domain):
        # type: (Dispatcher, DialogueStateTracker, Domain) -> List[Event]

        dispatcher.utter_message("I have printed a test!")

        print(tracker.latest_message)

        return [ConversationResumed()]