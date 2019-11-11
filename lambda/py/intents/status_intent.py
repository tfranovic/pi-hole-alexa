import json
from decimal import Decimal
from ask_sdk_model.ui import Card, StandardCard, Image
from ask_sdk_model.interfaces.alexa.presentation.apl.render_document_directive import RenderDocumentDirective

from intents.base_intent import BaseIntent


class StatusIntent(BaseIntent):

    SPEECH_TEMPLATE = "Pi Hole is currently {}. In the past 24 hours it had {} queries from {} clients, and blocked {} of them ({}%)."

    CARD_TEXT_TEMPLATE = "Status: {}\n" \
                         "Total Queries: {} ({} clients)\n" \
                         "Blocked Queries: {}\n" \
                         "Blocked Percent: {}%\n"

    def get_speech_message(self) -> str:
        status_message = StatusIntent.SPEECH_TEMPLATE.format(self.get_client().status, self.get_client().total_queries,
                                                             self.get_client().unique_clients, self.get_client().blocked,
                                                             Decimal(self.get_client().ads_percentage).normalize())

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
                                                        Decimal(self.get_client().ads_percentage).normalize())
        )

        return card

    def get_apl_directive(self) -> RenderDocumentDirective:

        with open('apl_templates/status.json') as status_json_file:
            status_json_doc = status_json_file.read() \
                .replace("${logo_url}", self.get_images_url() + "/logo_" + self.get_client().status + ".png") \
                .replace("${total_queries}", self.get_client().total_queries) \
                .replace("${total_clients}", self.get_client().total_clients) \
                .replace("${total_queries_image}", self.get_images_url() + "/globe.jpg") \
                .replace("${total_queries_image_large}", self.get_images_url() + "/globe.jpg") \
                .replace("${blocked_queries}", self.get_client().blocked) \
                .replace("${blocked_queries_image}", self.get_images_url() + "/hand.jpg") \
                .replace("${blocked_queries_image_large}", self.get_images_url() + "/hand.jpg") \
                .replace("${blocked_percent}", str(Decimal(self.get_client().ads_percentage).normalize())) \
                .replace("${blocked_percent_image}", self.get_images_url() + "/pie.jpg") \
                .replace("${blocked_percent_image_large}", self.get_images_url() + "/pie.jpg") \
                .replace("${blocked_domains}", self.get_client().domain_count) \
                .replace("${blocked_domains_image}", self.get_images_url() + "/file.jpg") \
                .replace("${blocked_domains_image_large}", self.get_images_url() + "/file.jpg")

            status_document = json.loads(status_json_doc)

            return RenderDocumentDirective(
                document=status_document['document'],
                datasources=status_document['datasources'],
                token='status_document'
            )
