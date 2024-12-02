import asyncio
import logging
from asyncio import Queue

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаем очередь
trade_queue = Queue()

# Функция для добавления задачи в очередь
async def add_trade_to_queue(mint, amount, action):
    await trade_queue.put((mint, amount, action))
    logger.info(f"Добавлена задача: {action} {amount} для {mint}")
