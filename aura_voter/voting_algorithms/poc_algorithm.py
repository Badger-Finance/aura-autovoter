from dataclasses import dataclass
from decimal import Decimal
from typing import Dict
from typing import List

from aura_voter.constants import AURABAL_GRAVIAURA_WETH_POOL_NAME
from aura_voter.constants import BADGER_WBTC_POOL_NAME
from aura_voter.constants import BOOBA_TRI_STABLE
from aura_voter.constants import META_WSTETH_WETH
from aura_voter.constants import POOL_ID_TO_NAME_MAP
from aura_voter.constants import POOL_NAME_TO_ID_MAP
from aura_voter.data_collectors import PoolBalance


@dataclass
class AlgorithmSettings:
    badger_pools_fixed_vote_weight: Decimal
    regulations: Dict[str, Decimal]
    regulations_votes_to_comply: Dict[str, Decimal]


class POCVoter:
    """
    Algorithmic voting for bveAURA on Snapshot
    """
    ALGORITHM_SETTINGS = AlgorithmSettings(
        badger_pools_fixed_vote_weight=Decimal(0.9),  # In %
        # Subject to change each voting round
        regulations={
            POOL_NAME_TO_ID_MAP[AURABAL_GRAVIAURA_WETH_POOL_NAME]: Decimal(0.33)
        },
        # Subject to change each voting round
        regulations_votes_to_comply={
            BOOBA_TRI_STABLE: Decimal(0.5),  # in %
            META_WSTETH_WETH: Decimal(0.5),  # in %
        },
    )

    def __init__(
            self, total_badger_locked_aura: Decimal,
            badger_pools_with_balances: List[PoolBalance],
    ):
        # TODO: Convert balances to AURA from graviAURA
        self.badger_pools_with_balances = badger_pools_with_balances
        self.badger_locked_aura = total_badger_locked_aura

    def propose_voting_choices(self) -> Dict[str, Decimal]:
        """
        Distributing votes across badger pools for bveAURA
        """
        finalized_votes = {}
        regulation_taken_voting_power = Decimal(0.0)
        for pool in self.badger_pools_with_balances:
            pool_id = pool.pool_id
            if self.ALGORITHM_SETTINGS.regulations.get(pool_id):
                # Decision made by council to subtract Y% as regulation on auraBAL pool
                regulation_taken_voting_power += (
                    pool.balance_aura * self.ALGORITHM_SETTINGS.regulations[pool_id]
                )
                voting_power = pool.balance_aura - regulation_taken_voting_power
            else:
                voting_power = pool.balance_aura
            # Each pool votes Y% of it's graviAURA balance for itself
            finalized_votes[POOL_ID_TO_NAME_MAP[pool_id]] = ((
                self.ALGORITHM_SETTINGS.badger_pools_fixed_vote_weight * voting_power
            ) / self.badger_locked_aura) * Decimal(100)
        # Votes subtracted for regulation needs are voting below
        if regulation_taken_voting_power:
            # Regulation voting power votes for some ecosystem pools
            for pool_name, v_weight in self.ALGORITHM_SETTINGS.regulations_votes_to_comply.items():
                finalized_votes[pool_name] = (
                    (regulation_taken_voting_power * v_weight / self.badger_locked_aura)
                    * Decimal(100)
                )
        # TODO: Implement fees capture instead of voting will all naked vlAURA
        finalized_votes[BADGER_WBTC_POOL_NAME] = Decimal(100) - sum(finalized_votes.values())
        return finalized_votes

    def propose_voting_choices_stable(self) -> Dict[str, Decimal]:
        """
        Stub method to vote 100% for ecosystem pool
        """
        return {
            BADGER_WBTC_POOL_NAME: Decimal(66.67),
            AURABAL_GRAVIAURA_WETH_POOL_NAME: Decimal(33.33)
        }
