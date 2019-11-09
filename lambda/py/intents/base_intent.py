from pihole import PiHole
from ask_sdk_model.ui import Card


class BaseIntent:

    def __init__(self, pihole_client: PiHole, pihole_images_url: str):
        self.pihole_client = pihole_client
        self.pihole_images_url = pihole_images_url

    def get_client(self) -> PiHole:
        return self.pihole_client

    def get_images_url(self) -> str:
        return self.pihole_images_url

    def get_speech_message(self) -> str:
        raise NotImplementedError("Abstract class!")

    def get_card(self) -> Card:
        raise NotImplementedError("Abstract class!")
