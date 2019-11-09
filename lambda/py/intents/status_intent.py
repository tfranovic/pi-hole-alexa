from ask_sdk_model.ui import Card, StandardCard, Image
from intents.base_intent import BaseIntent


class StatusIntent(BaseIntent):

    SPEECH_TEMPLATE = "Pi Hole is currently {}. It had {} queries from {} clients, and blocked {} of them ({}%)."

    CARD_TEXT_TEMPLATE = "Status: {}\n" \
                         "Total Queries: {} ({} clients)\n" \
                         "Blocked Queries: {}\n" \
                         "Blocked Percent: {}%\n"

    def get_speech_message(self) -> str:
        status_message = StatusIntent.SPEECH_TEMPLATE.format(self.get_client().status, self.get_client().total_queries,
                                                             self.get_client().unique_clients, self.get_client().blocked,
                                                             self.get_client().ads_percentage)

        return status_message

    def get_card(self) -> Card:

        card = StandardCard(
            title="Pi-hole Alexa",
            image=Image(
                small_image_url=self.get_images_url() + "/logo.png",
                large_image_url=self.get_images_url() + "/logo_large.png"
            ),
            text=StatusIntent.CARD_TEXT_TEMPLATE.format(self.get_client().status, self.get_client().total_queries,
                                                        self.get_client().unique_clients, self.get_client().blocked,
                                                        self.get_client().ads_percentage)
        )

        return card
