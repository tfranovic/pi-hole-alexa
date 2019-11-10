import time
from ask_sdk_model.ui import Card
from ask_sdk_model.directive import Directive

from intents.base_intent import BaseIntent
from intents.status_intent import StatusIntent


class EnableIntent(BaseIntent):

    def __init__(self, pihole_client, pihole_images):
        super().__init__(pihole_client, pihole_images)
        self.did_enable = self.__enable_if_not_already_enabled()
        self.status_intent = StatusIntent(pihole_client, pihole_images)

    def __enable_if_not_already_enabled(self) -> bool:
        if self.get_client().status == "enabled":
            return False

        self.get_client().enable()
        time.sleep(1)
        self.get_client().refresh()
        return True

    def get_speech_message(self) -> str:

        if self.did_enable:
            enable_message = "I have successfully enabled Pi Hole."
        else:
            enable_message = "Pi Hole was already enabled."

        enable_message = "{} Here's the current status! {}".format(enable_message, self.status_intent.get_speech_message())

        return enable_message

    def get_card(self) -> Card:

        return self.status_intent.get_card()

    def get_apl_directive(self) -> Directive:

        return self.status_intent.get_apl_directive()
