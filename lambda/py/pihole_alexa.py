# -*- coding: utf-8 -*-

# This is a simple Hello World Alexa Skill, built using
# the decorators approach in skill builder.
import logging
from functools import wraps

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response

import pihole
import os

from intents.base_intent import BaseIntent
from intents.status_intent import StatusIntent
from intents.enable_intent import EnableIntent
from intents.disable_intent import DisableIntent

sb = SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

pihole_server = os.environ['PIHOLE_SERVER']
pihole_images = os.environ['PIHOLE_IMAGES']
pihole_password = os.environ['PIHOLE_PASSWORD']

pihole_client = pihole.PiHole(pihole_server)
pihole_client.authenticate(pihole_password)


def supports_apl(handler_input):

    return handler_input.request_envelope.context.system.device.supported_interfaces.alexa_presentation_apl is not None


def client_refresh(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        pihole_client.refresh()
        return func(*args, **kwargs)
    return wrapper


def handle_base_intent(handler_input: HandlerInput, intent: BaseIntent, should_end_session: bool = True):

    response_builder = handler_input.response_builder.speak(intent.get_speech_message()).set_card(
        intent.get_card()).set_should_end_session(should_end_session)

    if supports_apl(handler_input):
        response_builder.add_directive(intent.get_apl_directive())

    return response_builder.response


@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
@client_refresh
def launch_request_handler(handler_input: HandlerInput) -> Response:
    """Handler for Skill Launch."""

    status_intent = StatusIntent(pihole_client, pihole_images)

    speech_text = "Welcome to the Alexa Pi Hole skill, here's the current status! " + status_intent.get_speech_message()

    response_builder = handler_input.response_builder.speak(speech_text).set_card(
        status_intent.get_card()).set_should_end_session(False)

    if supports_apl(handler_input):
        response_builder.add_directive(status_intent.get_apl_directive())

    return response_builder.response


@sb.request_handler(can_handle_func=is_intent_name("StatusIntent"))
@client_refresh
def status_intent_handler(handler_input: HandlerInput) -> Response:
    """Handler for Status Intent."""

    status_intent = StatusIntent(pihole_client, pihole_images)

    return handle_base_intent(handler_input, status_intent)


@sb.request_handler(can_handle_func=is_intent_name("EnableIntent"))
@client_refresh
def enable_intent_handler(handler_input: HandlerInput) -> Response:
    """Handler for Enable Intent."""

    enable_intent = EnableIntent(pihole_client, pihole_images)

    return handle_base_intent(handler_input, enable_intent)


@sb.request_handler(can_handle_func=is_intent_name("DisableIntent"))
@client_refresh
def disable_intent_handler(handler_input: HandlerInput) -> Response:
    """Handler for Disable Intent."""

    slots = handler_input.request_envelope.request.intent.slots

    if 'Duration' in slots and slots['Duration'].value is not None:
        disable_intent = DisableIntent(pihole_client, pihole_images, slots['Duration'].value)
    else:
        disable_intent = DisableIntent(pihole_client, pihole_images)

    return handle_base_intent(handler_input, disable_intent)


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input: HandlerInput) -> Response:
    """Handler for Help Intent."""

    speech_text = "You can say 'show status' to me!"

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            "Pi-hole Alexa", speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input: HandlerInput) -> Response:
    """Single handler for Cancel and Stop Intent."""

    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard("Pi-hole Alexa", speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input: HandlerInput) -> Response:
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    speech = (
        "The Pi Hole Alexa skill can't help you with that.  "
        "You can say 'show status'!!")
    reprompt = "You can say 'status' or 'show status'!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input: HandlerInput) -> Response:
    """Handler for Session End."""

    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input: HandlerInput, exception: Exception) -> Response:
    """Catch all exception handler, log exception and
    respond with custom message.
    """

    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


handler = sb.lambda_handler()
