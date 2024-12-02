# чисто рабочий файл, не читать

import asyncio
from src.queue_manager import add_trade_to_queue

async def add_tasks():
    # Добавляем задачи в очередь
    await add_trade_to_queue("5GdPTBf1gkRVHtPWCLG5Q76oUjyvViUDbfqJcwF7pump", 100, "buy")
    await add_trade_to_queue("5GdPTBf1gkRVHtPWCLG5Q76oUjyvViUDbfqJcwF7pump", 100, "sell")

