#!/usr/bin/python3
from brownie import VRFConsumer, accounts, config

STATIC_SEED = 123


def main():
    dev = accounts.add(config["wallets"]["from_key"])
    # Get the most recent PriceFeed Object
    vrf_contract = VRFConsumer[len(VRFConsumer) - 1]
    vrf_contract.getRandomNumber(STATIC_SEED, {"from": dev})
