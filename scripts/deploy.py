from brownie import FundMe, MockV3Aggregator, network, config
from scripts.helpful_scripts import (
    get_account,
    deploy_mocks,
    LOCAL_BLOCKCHAIN_ENVIRONMENTS,
)
from web3 import Web3


def deploy_fund_me():
    account = get_account()
    # pass the price feed address to our FundMe contract

    # if we are on a persistent network like rinkeby, use the associated address
    # otherwise, deploy mocks
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        price_feed_address = config["networks"][network.show_active()][
            "eth_usd_price_feed"
        ]
    else:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
        # the -1 index of the MockV3Aggregator contract is used to just use the latest deployment of the MockV3Aggregator
        print(f"Mocks deployed at address {price_feed_address}")

    fund_me = FundMe.deploy(
        price_feed_address,
        {"from": account},
        publish_source=config["networks"][network.show_active()].get(
            "verify"
        ),  # the .get("verify") at the end is the same as ["verify"], but it reduces the danger of index errors
    )  # argument publish_source=True publishes the verified source code on etherscan
    print(f"Contract deployed to {fund_me.address}")


def main():
    deploy_fund_me()
