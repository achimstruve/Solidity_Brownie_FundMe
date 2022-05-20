from brownie import network, MockV3Aggregator, config, accounts
from web3 import Web3

DECIMALS = 18
STARTING_PRICE = Web3.toWei(2000, "ether")

LOCAL_BLOCKCHAIN_ENVIRONMENTS = ["development", "ganache-local"]


def get_account():
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])


def deploy_mocks():
    # This function deploys mocks. Mocks are used to immitate real things like if they were present.
    # Since a local testnet like ganache has not access to chainlink data feeds this has to be immitated
    # by a mock of the AggregatorV3Interface, called MockV3Aggregator.
    # The source code of MockV3Aggregator has been copied from the GitHub chainlink-mix repository
    # https://github.com/smartcontractkit/chainlink-mix/blob/main/contracts/test/MockV3Aggregator.sol
    # It has been pasted into the MockV3Aggregator.sol file in the test folder of contracts
    print(f"The active network is {network.show_active()}")
    print("Deploying Mocks...")
    if len(MockV3Aggregator) <= 0:
        MockV3Aggregator.deploy(DECIMALS, STARTING_PRICE, {"from": get_account()})
