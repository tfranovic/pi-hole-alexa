import time
from ask_sdk_model.ui import Card
from ask_sdk_model.directive import Directive

from intents.base_intent import BaseIntent
from intents.status_intent import StatusIntent


class DisableIntent(BaseIntent):

    def __init__(self, pihole_client, pihole_images, disable_duration_minutes=15):
        super().__init__(pihole_client, pihole_images)
        self.disable_duration_minutes = disable_duration_minutes
        self.__disable()
        self.status_intent = StatusIntent(pihole_client, pihole_images)

    def __disable(self):
        self.get_client().disable(self.disable_duration_minutes * 60)
        time.sleep(0.5)
        self.get_client().refresh()

    def get_speech_message(self) -> str:
        disable_message = "I have successfully disabled Pi Hole for {} minutes. Here's the current status! {}".format(
            self.disable_duration_minutes, self.status_intent.get_speech_message()
        )

        return disable_message

    def get_card(self) -> Card:

        return self.status_intent.get_card()

    def get_apl_directive(self) -> Directive:

        return self.status_intent.get_apl_directive()
