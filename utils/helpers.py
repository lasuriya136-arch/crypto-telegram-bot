# utils/helpers.py

# Словарь соответствия тикеров -> ID для CoinGecko
SYMBOL_TO_ID = {
    "btc": "bitcoin",
    "eth": "ethereum",
    "sol": "solana",
    "doge": "dogecoin",
    "ada": "cardano",
    "dot": "polkadot",
    "xrp": "ripple",
    "ltc": "litecoin",
    "bch": "bitcoin-cash",
    "link": "chainlink",
    "matic": "polygon",
    "uni": "uniswap",
    "avax": "avalanche-2",
    "atom": "cosmos",
    "fil": "filecoin",
    "trx": "tron",
    "etc": "ethereum-classic",
    "xlm": "stellar",
    "dash": "dash",
    "zec": "zcash",
    # добавляйте по необходимости
}

def normalize_symbol(symbol: str) -> str:
    """
    Приводит символ к нижнему регистру и заменяет тикер на ID для CoinGecko.
    Если тикер не найден в словаре, возвращает как есть (в нижнем регистре).
    """
    symbol_lower = symbol.lower()
    return SYMBOL_TO_ID.get(symbol_lower, symbol_lower)