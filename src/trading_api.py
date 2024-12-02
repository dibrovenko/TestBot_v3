import asyncio
import ssl
import aiohttp
import time
import logging
from solders.transaction import VersionedTransaction
from solders.keypair import Keypair
from solders.commitment_config import CommitmentLevel
from solders.rpc.requests import SendVersionedTransaction
from solders.rpc.config import RpcSendTransactionConfig
from asyncio import Queue
from config import trade_config


# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class TokenTradingAPI:
    def __init__(self, trade_queue: Queue):
        self.config = trade_config
        self.trade_queue = trade_queue
        self.ssl_context = ssl.create_default_context()
        self.ssl_context.check_hostname = False
        self.ssl_context.verify_mode = ssl.CERT_NONE
        self.tokens_to_sell = {}

    async def _make_transaction(self, url, payload):
        """Отправляет запрос на выполнение транзакции (покупка или продажа)."""
        logger.info(f"Отправка запроса на {url} с данными {payload}")
        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(url, json=payload, ssl=self.ssl_context) as response:
                    if response.status == 200:
                        logger.info(f"Успешный ответ от {url}")
                        return await response.read()
                    else:
                        logger.error(f"Ошибка при выполнении запроса: {response.status}")
                        return None
            except Exception as e:
                logger.exception(f"Исключение при выполнении запроса: {e}")
                return None

    async def _process_transaction(self, response_content, mint, action, amount=None):
        """Обрабатывает транзакцию и обновляет состояние токенов."""
        logger.info(f"Обработка транзакции для {mint} с действием {action}")
        keypair = Keypair.from_base58_string(self.config.get("private_key"))
        tx = VersionedTransaction(VersionedTransaction.from_bytes(response_content).message, [keypair])
        commitment = CommitmentLevel.Confirmed
        cfg = RpcSendTransactionConfig(preflight_commitment=commitment)

        async with aiohttp.ClientSession() as session:
            try:
                async with session.post(
                    url="https://api.mainnet-beta.solana.com/",
                    headers={"Content-Type": "application/json"},
                    data=SendVersionedTransaction(tx, cfg).to_json(),
                    ssl=self.ssl_context
                ) as rpc_response:
                    if rpc_response.status == 200:
                        rpc_res = await rpc_response.json()
                        tx_signature = rpc_res.get('result')
                        if tx_signature:
                            logger.info(f"Транзакция успешно выполнена: https://solscan.io/tx/{tx_signature}")
                            if action == "buy":
                                self.tokens_to_sell[mint] = {"amount": amount, "timestamp": time.time()}
                                logger.info(f"Добавлен токен {mint} в список на покупку: {amount}")
                            elif action == "sell":
                                self.tokens_to_sell.pop(mint, None)
                                logger.info(f"Добавлен токен {mint} в список на продажу: {amount}")
                        else:
                            logger.error(f"Транзакция {action} не выполнена: {rpc_res}, токен {mint}")
                    else:
                        logger.error(f"Ошибка выполнения RPC-запроса: {rpc_response.status}")
            except Exception as e:
                logger.exception(f"Исключение при обработке транзакции: {e}")

    async def buy_or_sell(self, mint, amount, action):
        """Объединенная функция для покупки и продажи токена."""
        logger.info(f"Начало операции {action} для {mint} на сумму {amount}")
        url = 'https://pumpportal.fun/api/trade-local'
        payload = {
            "publicKey": self.config.get("public_key"),
            "action": action,
            "mint": mint,
            "amount": amount,
            "denominatedInSol": "false",
            "slippage": 4,
            "priorityFee": self.config.get("priority_fee"),
            "pool": "pump"
        }

        response_content = await self._make_transaction(url, payload)
        if response_content:
            await self._process_transaction(response_content, mint, action, amount)
        self.trade_queue.task_done()

    async def trade_worker(self):
        """Фоновый процесс для обработки очереди торгов."""
        while True:
            mint, amount, action = await self.trade_queue.get()
            logger.info(f"Получена задача: {action} {mint} на сумму {amount}")
            await self.buy_or_sell(mint, amount, action)


    async def start(self):
        """Запускает фоновый процесс."""
        logger.info("Запуск фонового процесса торговли")
        asyncio.create_task(self.trade_worker())
