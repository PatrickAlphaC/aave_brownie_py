from scripts.aave_borrow import get_asset_price


def test_get_asset_price():
    # Arrange / Act
    asset_price = get_asset_price()
    # Assert
    assert asset_price > 0
