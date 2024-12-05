import asyncio
import logging
from asyncio import Queue

from config import setup_logger
logger = setup_logger(name=__name__, log_file=__name__, level=logging.INFO)


# Создаем очередь
trade_queue = Queue()

# Функция для добавления задачи в очередь
async def add_trade_to_queue(mint, amount, action):
    await trade_queue.put((mint, amount, action))
    logger.info(f"Добавлена задача: {action} {amount} для {mint}")
