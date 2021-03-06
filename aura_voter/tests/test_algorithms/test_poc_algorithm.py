from decimal import Decimal

import pytest

from aura_voter.constants import AURABAL_GRAVIAURA_WETH_POOL_NAME
from aura_voter.constants import BADGER_WBTC_POOL_NAME
from aura_voter.constants import GRAVIAURA
from aura_voter.constants import POOL_ID_TO_NAME_MAP
from aura_voter.constants import POOL_NAME_TO_ID_MAP
from aura_voter.constants import WBTC_DIGG_GRAVIAURA
from aura_voter.data_collectors import PoolBalance
from aura_voter.tests import PPFS
from aura_voter.voting_algorithms.poc_algorithm import POCVoter


def test_poc_algorithm_happy_simple_data():
    locked_aura = Decimal(1000)
    balances = [
        PoolBalance(
            pool_id=POOL_NAME_TO_ID_MAP[AURABAL_GRAVIAURA_WETH_POOL_NAME],
            balance=Decimal(560),
            balance_aura=Decimal(560) * Decimal(PPFS / 10 ** 18),
            target_token=GRAVIAURA,
        ),
        PoolBalance(
            pool_id=POOL_NAME_TO_ID_MAP[WBTC_DIGG_GRAVIAURA],
            balance=Decimal(300),
            balance_aura=Decimal(300) * Decimal(PPFS / 10 ** 18),
            target_token=GRAVIAURA
        ),

    ]
    voter = POCVoter(locked_aura, balances)
    votes = voter.propose_voting_choices()
    assert votes == {'33/33/33 graviAURA/auraBAL/WETH': Decimal('34.82476162062310654454978017'),
                     '40/40/20 WBTC/DIGG/graviAURA': Decimal('27.84495865188414766986031316'),
                     '80/20 BADGER/WBTC': Decimal('18.27195247242537317520887355'),
                     'MetaStable wstETH/WETH': Decimal('9.529163627533686305190516560'),
                     'bb-a-USDT/bb-a-DAI/bb-a-USDC': Decimal('9.529163627533686305190516560')}
    # Make sure all votes make 100% when summed up
    assert sum(votes.values()) == Decimal(100)


def test_poc_algorithm_stable_vote():
    voter = POCVoter(Decimal(1000), [])
    stable_choices = voter.propose_voting_choices_stable()
    assert stable_choices == {
        '33/33/33 graviAURA/auraBAL/WETH': Decimal(
            '17.21000000000000085265128291212022304534912109375'),
        '80/20 BADGER/WBTC': Decimal(
            '40.25999999999999801048033987171947956085205078125'),
        'MetaStable wstETH/WETH': Decimal(
            '34.02000000000000312638803734444081783294677734375'),
        'p-MetaStable WMATIC/stMATIC': Decimal(
            '8.5099999999999997868371792719699442386627197265625')
    }
    assert sum(stable_choices.values()) == pytest.approx(Decimal(100))


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
            pool_id=POOL_NAME_TO_ID_MAP[WBTC_DIGG_GRAVIAURA],
            balance=balance,
            balance_aura=balance * Decimal(PPFS / 10 ** 18),
            target_token="0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
        )]
    )
    votes = voter.propose_voting_choices()
    pool_expected_vote = ((balance * Decimal(PPFS / 10 ** 18) *
                           POCVoter.ALGORITHM_SETTINGS.badger_pools_fixed_vote_weight)
                          / locked_aura) * Decimal(100)
    assert pool_expected_vote == votes[POOL_ID_TO_NAME_MAP[
        '0x8eb6c82c3081bbbd45dcac5afa631aac53478b7c000100000000000000000270'
    ]]

    badger_wbtc_expected_vote = Decimal(100) - pool_expected_vote
    assert badger_wbtc_expected_vote == votes[BADGER_WBTC_POOL_NAME]
