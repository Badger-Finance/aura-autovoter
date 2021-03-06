from copy import deepcopy
from unittest.mock import MagicMock

import pytest

from aura_voter.data_collectors.snapshot_collectors import get_current_hh_proposal_round
from aura_voter.data_collectors.snapshot_collectors import get_gauge_weight_snapshot
from aura_voter.data_collectors.snapshot_collectors import get_snapshot_by_id
from aura_voter.tests.test_data.test_data import ALL_PROPOSAL_TEST_DATA
from aura_voter.tests.test_data.test_data import ACTIVE_PROPOSAL_DATA


def test_get_gauge_weight_snapshot_happy(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=ACTIVE_PROPOSAL_DATA,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                return_value={'timestamp': 1657159210}
            )
        ))
    )
    result = get_gauge_weight_snapshot()
    assert result['title'] == "Gauge Weight for Week of 7th July 2022"
    assert result['state'] == "active"
    assert result['space'] == {'id': 'aurafinance.eth', 'name': 'Aura Finance'}
    assert result['scores'] is not None


def test_get_gauge_weight_snapshot_empty_res(mocker):
    mocker.patch("aura_voter.data_collectors.snapshot_collectors.get_web3", )
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_gauge_weight_snapshot()


@pytest.mark.parametrize('timestamp', [1648684815, 2948684815])
def test_get_gauge_weight_snapshot_no_match(mocker, timestamp):
    """
    timestamp is way off from proposal start and end times
    """
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=ACTIVE_PROPOSAL_DATA,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                return_value={'timestamp': timestamp}
            )
        ))
    )
    assert not get_gauge_weight_snapshot()


def test_get_gauge_weight_snapshot_no_active(mocker):
    data = deepcopy(ALL_PROPOSAL_TEST_DATA)
    data['proposals'][3]['state'] = "closed"
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=data,
            )
        )
    )
    mocker.patch(
        "aura_voter.data_collectors.snapshot_collectors.get_web3",
        return_value=MagicMock(eth=MagicMock(
            getBlock=MagicMock(
                return_value={'timestamp': 1657159210}
            )
        ))
    )
    assert not get_gauge_weight_snapshot()


def test_get_snapshot_by_id(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value=ALL_PROPOSAL_TEST_DATA,
            )
        )
    )
    snapshot = get_snapshot_by_id(
        "0xabaf9275ae0533ce991059e8b5664225bf54bae81b9305ae60b48198db180ad9"
    )
    assert snapshot['title'] == 'Gauge Weight for Week of 23rd June 2022'
    assert snapshot['state'] == "closed"


def test_get_snapshot_by_id_empty_res(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                return_value={},
            )
        )
    )
    assert not get_snapshot_by_id(
        "0xabaf9275ae0533ce991059e8b5664225bf54bae81b9305ae60b48198db180ad9"
    )


def test_get_current_hh_proposal_round_happy(mocker):
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                side_effect=[ALL_PROPOSAL_TEST_DATA, {}],
            )
        )
    )
    # Active snapshot comes as 4 in test dataset, minus test OG dataset made by AURA team
    assert get_current_hh_proposal_round() == 3


def test_get_current_hh_proposal_round_none(mocker):
    test_data = deepcopy(ALL_PROPOSAL_TEST_DATA)
    test_data['proposals'].pop(3)
    mocker.patch(
        'aura_voter.data_collectors.snapshot_collectors.make_gql_client',
        return_value=MagicMock(
            execute=MagicMock(
                side_effect=[test_data, {}],
            )
        )
    )
    # If there is no active proposal, just return None
    assert get_current_hh_proposal_round() is None
