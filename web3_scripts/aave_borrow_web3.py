from web3 import Web3
from abis import lending_pool_addresses_provider_abi, lending_pool_abi, erc20_abi, price_feed_abi
import os

kovan_lending_poll_addresses_provider = Web3.toChecksumAddress(
    '0x88757f2f99175387aB4C6a4b3067c77A695b0349')
kovan_weth_address = Web3.toChecksumAddress(
    '0xd0a1e359811322d97991e03f863a0c30c2cf029c')
kovan_aave_link_address = Web3.toChecksumAddress(
    '0xAD5ce863aE3E4E9394Ab43d4ba0D80f419F61789')
my_address = Web3.toChecksumAddress(
    '0x643315C9Be056cDEA171F4e7b2222a4ddaB9F88D')


def main():
    w3 = Web3(Web3.HTTPProvider(os.getenv('KOVAN_RPC_URL')))
    amount = w3.toWei(0.1, 'ether')
    lending_pool = get_lending_pool(w3)
    nonce_one = w3.eth.getTransactionCount(my_address)
    nonce_two = nonce_one + 1
    nonce_three = nonce_two + 1
    approve_erc20(w3, kovan_weth_address, lending_pool.address,
                  amount, nonce=nonce_one)
    tx_hash = deposit_to_aave(w3, amount, lending_pool, nonce=nonce_two)
    print(tx_hash.hex())
    borrowable_eth = get_borrowable_data(lending_pool, my_address)
    print(f"LETS BORROW IT ALL")
    erc20_eth_price = get_asset_price(w3)
    amount_erc20_to_borrow = (1/erc20_eth_price) * (borrowable_eth * 0.95)
    print(f"We are going to borrow {amount_erc20_to_borrow} LINK")
    borrow_erc20(w3, lending_pool, amount_erc20_to_borrow,
                 erc20_address=kovan_aave_link_address, nonce=nonce_three)
    get_borrowable_data(lending_pool, my_address)


def borrow_erc20(w3, lending_pool, amount, erc20_address=None, nonce=None):
    # 1 is stable interest rate
    # 0 is the referral code
    nonce = nonce if nonce else w3.eth.getTransactionCount(my_address)
    function_call = lending_pool.functions.borrow(
        erc20_address, Web3.toWei(amount, 'ether'), 1, 0, my_address)
    transaction = function_call.buildTransaction({'chainId': 42,
                                                  'from': my_address,
                                                 'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Congratulations! We have just borrowed {amount}")


def get_asset_price(w3):
    # # For mainnet we can just do:
    # # return Contract(f"{pair}.data.eth").latestAnswer() / 1e8
    # link_eth_price_feed = interface.AggregatorV3Interface(
    #     config['networks'][network.show_active()]['link_eth_price_feed'])
    link_eth_price_feed = w3.eth.contract(
        address='0x3Af8C569ab77af5230596Acf0E8c2F9351d24C38', abi=price_feed_abi)
    latest_price = Web3.fromWei(
        link_eth_price_feed.functions.latestRoundData().call()[1], 'ether')
    print(f"The LINK/ETH price is {latest_price}")
    return float(latest_price)


def get_borrowable_data(lending_pool, my_address):
    total_collateral_eth, total_debt_eth, available_borrow_eth, current_liquidation_threshold, tlv, health_factor = lending_pool.functions.getUserAccountData(
        my_address).call()
    available_borrow_eth = Web3.fromWei(available_borrow_eth, 'ether')
    total_collateral_eth = Web3.fromWei(total_collateral_eth, 'ether')
    total_debt_eth = Web3.fromWei(total_debt_eth, 'ether')
    print(
        f"You have {total_collateral_eth} worth of ETH deposited.")
    print(f"You have {total_debt_eth} worth of ETH borrowed.")
    print(f"You can borrow {available_borrow_eth} worth of ETH.")
    return float(available_borrow_eth)


def get_lending_pool(w3):
    lending_poll_addresses_provider = w3.eth.contract(
        address=kovan_lending_poll_addresses_provider, abi=lending_pool_addresses_provider_abi)
    lending_pool_address = lending_poll_addresses_provider.functions.getLendingPool().call()
    lending_pool = w3.eth.contract(
        address=lending_pool_address, abi=lending_pool_abi)
    return lending_pool


def deposit_to_aave(w3, amount, lending_pool, nonce=None):
    print("Depositing to Aave...")
    nonce = nonce if nonce else w3.eth.getTransactionCount(my_address)
    function_call = lending_pool.functions.deposit(
        kovan_weth_address, amount, my_address, 0)
    transaction = function_call.buildTransaction({'chainId': 42,
                                                  'from': my_address,
                                                  'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print("Deposited!")
    return tx_hash


def approve_erc20(w3, erc20_address, spender, amount, nonce=None):
    print("Approving ERC20...")
    nonce = nonce if nonce else w3.eth.getTransactionCount(my_address)
    erc20 = w3.eth.contract(address=erc20_address, abi=erc20_abi)
    function_call = erc20.functions.approve(spender, amount)
    nonce = w3.eth.getTransactionCount(my_address)
    transaction = function_call.buildTransaction({'chainId': 42,
                                                  'from': my_address,
                                                 'nonce': nonce})
    signed_txn = w3.eth.account.sign_transaction(
        transaction, private_key=os.getenv('PRIVATE_KEY'))
    tx_hash = w3.eth.send_raw_transaction(signed_txn.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)
    print(f"Approved {amount} tokens for contract {spender}")


if __name__ == '__main__':
    main()
