import os
from typing import Optional

from badger_voter_sdk.aws import get_secret
from badger_voter_sdk.rich_logger import logger
from discord import InvalidArgument
from discord import RequestsWebhookAdapter
from discord import Webhook

from aura_voter.constants import DISCORD_WEBHOOK_SECRET_ID
from aura_voter.constants import DISCORD_WEBHOOK_SECRET_KEY


def send_code_block_to_discord(
    msg: str, username: str, url: Optional[str] = None
):
    if not url:
        url = os.getenv("DISCORD_WEBHOOK_URL") or get_secret(
            secret_id=DISCORD_WEBHOOK_SECRET_ID,
            secret_key=DISCORD_WEBHOOK_SECRET_KEY,
        )
    try:
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
    except InvalidArgument:
        logger.error("Discord Webhook URL is not configured")
        return
    msg = f"```\n{msg}\n```"
    webhook.send(username=username, content=msg)


def send_message_to_discord(
    msg: str,
    username: str,
    url: Optional[str] = None,
) -> None:
    if not url:
        url = os.getenv("DISCORD_WEBHOOK_URL") or get_secret(
            secret_id=DISCORD_WEBHOOK_SECRET_ID,
            secret_key=DISCORD_WEBHOOK_SECRET_KEY,
        )
    try:
        webhook = Webhook.from_url(
            url,
            adapter=RequestsWebhookAdapter(),
        )
    except InvalidArgument:
        logger.error("Discord Webhook URL is not configured")
        return
    webhook.send(content=msg, username=username)
