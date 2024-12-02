from dotenv import load_dotenv
import os

load_dotenv()

trade_config = {
    "public_key": os.getenv("PUBLIC_KEY"),
    "private_key": os.getenv("PRIVATE_KEY"),
    "priority_fee": 0.0005,
    "sell_multiplier": 1.4,
    "sell_multiplier_with_social_activity": 1.7,
    "amount": 100
}

token_config = {
    "time_window": 40,  # Время окна в секундах
    "min_buyers": 5,  # Минимальное количество уникальных покупателей
    "min_transactions": 12  # Минимальное количество сделок для анализа
}

handle_messages_config = {
    "max_tokens": 10,
    "timeout_duration": 100
}

config = {
    "token_config": token_config,
    "trade_config": trade_config,
    "handle_messages_config": handle_messages_config
}