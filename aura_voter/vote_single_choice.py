from aura_voter.cast_vote import cast_single_choice_vote
from aura_voter.constants import BOT_USERNAME
from aura_voter.discord import send_message_to_discord

# Hardcoded params for one-time needs
SNAPSHOT_IDS = [
    ("0x797467e0b451a49773cfea97359a32ab880caee688d16fe7db41f94a4e0570f0", 1),
]


def vote_single_choice():
    for snapshot_id, choice in SNAPSHOT_IDS:
        send_message_to_discord(
            f"🗳️🗳️🗳️🗳️ Voting for single choice on snapshot {snapshot_id} 🗳️🗳️🗳️🗳️",
            username=BOT_USERNAME
        )
        cast_single_choice_vote(choice, snapshot_id)
        send_message_to_discord(
            "👍👍👍👍 Voting succeeded 👍👍👍👍",
            username=BOT_USERNAME
        )
