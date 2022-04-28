<br/>
<p align="center">
<a href="https://chain.link" target="_blank">
<img src="https://raw.githubusercontent.com/PatrickAlphaC/aave_brownie_py/main/img/aave.png" width="225" alt="Python + Aave">
<img src="https://raw.githubusercontent.com/PatrickAlphaC/aave_brownie_py/main/img/python.png" width="225" alt="Python + Aave">
</a>
</p>
<br/>

# Requirements

-   [brownie](https://eth-brownie.readthedocs.io/en/stable/install.html)
-   [nodejs](https://nodejs.org/en/)
-   [ganache-cli](https://www.npmjs.com/package/ganache-cli)

# aave_brownie_py

Put down collateral, Borrow, and repay a loan from Aave! Use this to short assets and accrue interest.

[You can see a web3 version of this here. ](https://github.com/PatrickAlphaC/aave_web3_py)

In our `aave_borrow.py` script, we do the following:

1. Approve our `ETH` to be swapped for `WETH`
2. Swap an `amount` of `ETH` for `WETH`
3. Using `deposit_to_aave` we deposit the `WETH` as collateral
4. We use that collateral to borrow `DAI` with `borrow_erc20`
5. Then, we pay it back!
6. We can view the txs on etherscan to see what's going on under the hood.

# Setup

You'll need python installed. If working with a virtual environment, you can run:

```
pip install -r requirements.txt
```

Or, ideally you use pipx:

```bash
pip install --user pipx
pipx ensurepath
# restart your terminal
pipx install eth-brownie
```

You'll need the following [environment variables](https://www.twilio.com/blog/2017/01/how-to-set-environment-variables.html). You can set them all in your `.env` file:

```
export WEB3_INFURA_PROJECT_ID=YourProjectID
export PRIVATE_KEY="0xasdfasdfasdfasd..."
```

-   `PRIVATE_KEY`: Your Private Key from your Wallet. \*Note: If using metamask, you'll have to add a 0x to the start of your private key.
-   `WEB3_INFURA_PROJECT_ID`: Your connection to the blockchain. You can get a URL from a service like [Infura](https://infura.io/)]. Right now it is hard coded to work with infura, but you can modify it however you want using `brownie networks modify`.

## Run `source .env`

This doesn't auto-pull in your `.env` file at the start, so you have to set your environment variables at the start.

And last, be sure to check the aave_dai_token if you're using a [testnet DAI token](https://docs.aave.com/developers/deployed-contracts/deployed-contracts0). Aave sometimes changes the token they use on testnet to keep liquidity, [please check here for reference](https://aave.github.io/aave-addresses/kovan.json).
Also, feel free to check the [Aave docs](https://docs.aave.com/developers/the-core-protocol/lendingpool) as well, to learn more about the tools we are using.

# Quickstart - kovan

1. [Get some kovan ETH](https://faucet.kovan.network/)

2. Get some WETH

```
brownie run scripts/get_weth.py --network kovan
```

3. Run the script!

```
brownie run scripts/aave_borrow.py --network kovan
```

# Quickstart - mainnet-fork

Optional for running locally:
If you want to run locally, you can install `ganache-cli` and `yarn`. Here is where you can [install yarn.](https://classic.yarnpkg.com/en/docs/install/#mac-stable)

```
yarn global add ganache-cli
```

Then, you can run `ganache-cli --fork YOUR_INFURA_URL_HERE`, or just `brownie run <YOUR_SCRIPT> --network mainnet-fork`

1. Get some WETH, borrow, and repay!

```
brownie run scripts/aave_borrow.py
```
