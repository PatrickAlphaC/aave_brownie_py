from brownie import interface, config, network, accounts

amount = 100000000000000000  # 0.1


def main():
    acct = accounts.add(config["wallets"]["from_key"])
    erc20_address = config['networks'][network.show_active()]['weth_token']
    lending_pool = get_lending_pool()
    approve_erc20(amount, lending_pool.address, erc20_address, acct)
    print("Depositing...")
    lending_pool.deposit(erc20_address, amount,
                         acct.address, 0, {'from': acct})
    print("Deposited!")


def get_lending_pool():
    lending_pool_addresses_provider = interface.ILendingPoolAddressesProvider(
        config['networks'][network.show_active()]['lending_poll_addresses_provider'])
    lending_pool_address = lending_pool_addresses_provider.getLendingPool()
    lending_pool = interface.ILendingPool(lending_pool_address)
    return lending_pool


def approve_erc20(amount, lending_pool_address, erc20_address, acct):
    print("Approving ERC20...")
    erc20 = interface.IERC20(erc20_address)
    tx_hash = erc20.approve(lending_pool_address, amount, {'from': acct})
    tx_hash.wait(1)
    print("Approved!")


if __name__ == '__main__':
    main()
