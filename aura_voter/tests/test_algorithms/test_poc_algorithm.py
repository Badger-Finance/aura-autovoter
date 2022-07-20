from decimal import Decimal

import pytest

from aura_voter.constants import AURABAL_GRAVIAURA_WETH_POOL_NAME
from aura_voter.constants import AURABAL_WETH_GRAVIAURA
from aura_voter.constants import BADGER_WBTC_POOL_NAME
from aura_voter.constants import GRAVIAURA
from aura_voter.constants import POOL_ID_TO_NAME_MAP
from aura_voter.constants import POOL_NAME_TO_ID_MAP
from aura_voter.data_collectors import PoolBalance
from aura_voter.tests import PPFS
from aura_voter.voting_algorithms.poc_algorithm import POCVoter


def test_poc_algorithm_happy_simple_data():
    locked_aura = Decimal(1000)
    balances = [
        PoolBalance(
            pool_id=POOL_NAME_TO_ID_MAP[AURABAL_WETH_GRAVIAURA],
            balance=Decimal(560),
            balance_aura=Decimal(560) * Decimal(PPFS / 10 ** 18),
            target_token=GRAVIAURA,
        ),
        PoolBalance(
            pool_id=POOL_NAME_TO_ID_MAP['DIGG'],
            balance=Decimal(300),
            balance_aura=Decimal(300) * Decimal(PPFS / 10 ** 18),
            target_token=GRAVIAURA
        ),

    ]
    voter = POCVoter(locked_aura, balances)
    votes = voter.propose_voting_choices()
    assert votes == {
        '33/33/33 auraBAL/graviAURA/WETH': Decimal('33.76800000000000004973799150'),
        'DIGG': Decimal('27.00000000000000066613381478'),
        # 2 pools below are voted as a part of the regulation for auraBAL pool
        'bb-a-USDT/bb-a-DAI/bb-a-USDC': Decimal('9.240000000000000435207425655'),
        'MetaStable wstETH/WETH': Decimal('9.240000000000000435207425655'),
        '80/20 BADGER/WBTC': Decimal('20.75199999999999841371334240')
    }
    # Make sure all votes make 100% when summed up
    assert sum(votes.values()) == Decimal(100)


def test_poc_algorithm_stable_vote():
    voter = POCVoter(Decimal(1000), [])
    stable_choices = voter.propose_voting_choices_stable()
    assert stable_choices == {
        BADGER_WBTC_POOL_NAME: Decimal(66.67),
        AURABAL_GRAVIAURA_WETH_POOL_NAME: Decimal(33.33)
    }
    assert sum(stable_choices.values()) == Decimal(100)


@pytest.mark.parametrize(
    "balance",
    [
        Decimal(1), Decimal(900), Decimal(0.00123)
    ]
)
def test_poc_algorithm_calc_comparison(balance):
    locked_aura = Decimal(1000)
    voter = POCVoter(
        locked_aura, [PoolBalance(
            pool_id=POOL_NAME_TO_ID_MAP['DIGG'],
            balance=balance,
            balance_aura=balance * Decimal(PPFS / 10 ** 18),
            target_token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        )]
    )
    votes = voter.propose_voting_choices()
    pool_expected_vote = ((balance * POCVoter.ALGORITHM_SETTINGS.badger_pools_fixed_vote_weight)
                          / locked_aura) * Decimal(100)
    assert pool_expected_vote == votes[POOL_ID_TO_NAME_MAP[
        '0x8eb6c82c3081bbbd45dcac5afa631aac53478b7c000100000000000000000270'
    ]]

    badger_wbtc_expected_vote = Decimal(100) - pool_expected_vote
    assert badger_wbtc_expected_vote == votes[BADGER_WBTC_POOL_NAME]
