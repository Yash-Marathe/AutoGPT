import re
from decimal import Decimal
from sample_code import get_ethereum_price

def test_get_ethereum_price() -> None:
    # Read the Ethereum price from the file
    with open("eth_price.txt", "r") as file:
        eth_price = file.read().strip()

    # Validate that the eth price is a number
    pattern = r"^\d+(\.\d{1,2})?$"
    matches = re.match(pattern, eth_price) is not None
    if not matches:
        raise AssertionError(f"AssertionError: Ethereum price should be a number with at most two decimal places, but got {eth_price}")

    # Get the current price of Ethereum
    real_eth_price = get_ethereum_price()

    # Convert the eth price to a numerical value for comparison
    eth_price_value = Decimal(eth_price)
    real_eth_price_value = Decimal(real_eth_price)

    # Check if the eth price is within 5% of the actual Ethereum price
    assert (
        abs((real_eth_price_value - eth_price_value) / real_eth_price_value) <= 0.05
    ), f"AssertionError: Ethereum price is not within 5% of the actual Ethereum price (Provided price: ${eth_price}, Real price: ${real_eth_price})"

    print("Matches")


if __name__ == "__main__":
    test_get_ethereum_price()
