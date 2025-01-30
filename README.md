# hyperliquid-whale-check

## Installation
```bash
pip install hyperliquid-python-sdk
```

## Run the File
```bash
python whale_checker.py
```

## Usage Examples
```python
if __name__ == "__main__":
    # Example: Check if a wallet has more than 1% of total HFUN supply
    wallet = "0xa2ce501d9c0c5e23d34272f84402cfb7835b3126"
    result = is_whale_wallet(wallet, "HFUN", 1.0)
    print(f"Is whale wallet: {result}")
```
