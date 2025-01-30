import requests
from hyperliquid.info import Info
from hyperliquid.utils import constants

def get_token_info(token: str) -> dict:
    """
    Get token information from the Hyperliquid API using tokenDetails endpoint.

    Args:
        token (str): The token symbol to look up

    Returns:
        dict: Token information including total supply and circulating supply
    """
    try:
        # Use the SDK's Info client to get spot metadata
        info = Info(constants.MAINNET_API_URL, skip_ws=True)
        meta_data = info.spot_meta()

        # Find the token ID
        token_id = None
        for token_info in meta_data['tokens']:
            if token_info['name'] == token:
                token_id = token_info['tokenId']
                break

        if not token_id:
            print(f"Could not find token ID for {token}")
            return None

        # Get token details using the token ID
        response = requests.post(
            f"{constants.MAINNET_API_URL}/info",
            json={
                "type": "tokenDetails",
                "tokenId": token_id
            }
        )
        response.raise_for_status()
        return response.json()

    except Exception as e:
        print(f"Error fetching token info: {str(e)}")
        return None

def is_whale_wallet(wallet_address: str, token: str, threshold_percentage: float) -> bool:
    """
    Check if a wallet qualifies as a 'whale wallet' based on their token holdings and threshold percentage.

    Args:
        wallet_address (str): The wallet address to check
        token (str): The token symbol to check holdings for (e.g., 'BTC', 'ETH')
        threshold_percentage (float): The minimum percentage of total supply required to be considered a whale (0-100)

    Returns:
        bool: True if the wallet holds more than the threshold percentage of total supply, False otherwise
    """
    # Initialize the Info API client
    info = Info(constants.MAINNET_API_URL, skip_ws=True)

    try:
        # Get token information including total supply
        token_info = get_token_info(token)
        if not token_info:
            print(f"Could not find token information for {token}")
            return False

        # Get the clearinghouse state which contains user positions
        clearinghouse_state = info.spot_user_state(wallet_address)
        # Find the position for the specified token
        for holding in clearinghouse_state['balances']:
            if holding['coin'] == token:
                # Get the size of the holding
                holding_size = abs(float(holding['total']))

                # Calculate the percentage of circulating supply
                total_supply = float(token_info['totalSupply'])
                holding_percentage = (holding_size / total_supply) * 100

                return holding_percentage >= threshold_percentage

        print(f"Wallet {wallet_address} does not hold any {token} tokens")
        return False

    except Exception as e:
        print(f"Error checking whale status: {str(e)}")
        return False

# Example usage:
if __name__ == "__main__":
    # Example: Check if a wallet has more than 1% of total HFUN supply
    wallet = "0xa2ce501d9c0c5e23d34272f84402cfb7835b3126"
    result = is_whale_wallet(wallet, "HFUN", 1.0)
    print(f"Is whale wallet: {result}")