from brownie import FundMe, network, accounts, exceptions
from scripts.helpful_scripts import get_account, LOCAL_BLOCKCHAIN_ENVIRONMENTS
from scripts.deploy import deploy_fund_me
import pytest


def test_can_fund_and_withdraw():
    account = get_account()

    deploy_fund_me()
    fund_me = FundMe[-1]

    entrance_fee = fund_me.getEntranceFee()
    tx = fund_me.fund({"from": account, "value": entrance_fee})
    tx.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == entrance_fee

    tx2 = fund_me.clean({"from": account})
    tx2.wait(1)
    assert fund_me.addressToAmountFunded(account.address) == 0


def test_only_owner_can_withdraw():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        pytest.skip("only for local testing")
    account = get_account()
    print("account:")
    deploy_fund_me()
    fund_me = FundMe[-1]
    # accounts.add()
    bad_actor = accounts[1]
    print(type(bad_actor))
    print(f"bad actor: {bad_actor.address}")

    with pytest.raises(exceptions.VirtualMachineError):
        fund_me.clean({"from": bad_actor.address})
