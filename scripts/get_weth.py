from brownie import accounts, config, network, interface


def main():
    """
    Runs the get_weth function to get WETH
    """
    get_weth()


def get_weth(account=None):
    """
    Mints WETH by depositing ETH.
    """
    account = (
        account if account else accounts.add(config["wallets"]["from_key"])
    )  # add your keystore ID as an argument to this call
    weth = interface.WethInterface(
        config["networks"][network.show_active()]["weth_token"]
    )
    tx = weth.deposit({"from": account, "value": 1000000000000000000})
    print("Received 1 WETH")
    return tx
