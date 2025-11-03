# blockchain.py
import hashlib
import json
import time
from typing import List, Dict, Any, Tuple
import uuid
from datetime import datetime


class Transaction:
    def __init__(self, sender: str, receiver: str, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount
        self.signature = None
        self.transaction_id = str(uuid.uuid4())
        self.timestamp = time.time()
        self.fee = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            'transaction_id': self.transaction_id,
            'sender': self.sender,
            'receiver': self.receiver,
            'amount': self.amount,
            'fee': self.fee,
            'timestamp': self.timestamp
        }

    def calculate_hash(self) -> str:
        transaction_string = json.dumps(self.to_dict(), sort_keys=True)
        return hashlib.sha256(transaction_string.encode()).hexdigest()

    def sign_transaction(self, private_key: str = None):
        if private_key is None:
            self.signature = f"signed_{self.calculate_hash()}"
        else:
            self.signature = f"signed_with_{private_key}_{self.calculate_hash()}"

    def is_valid(self) -> bool:
        if self.sender == "0":
            return True

        if not all([self.sender, self.receiver, self.amount]):
            return False

        if self.amount <= 0:
            return False

        if not self.signature:
            return False

        if not self.signature.startswith("signed_"):
            return False

        return True

    def verify_integrity(self) -> Tuple[bool, str]:
        try:
            if not all([self.sender, self.receiver, self.amount is not None]):
                return False, "Отсутствуют обязательные поля"

            if self.amount <= 0:
                return False, "Сумма должна быть положительной"

            if self.sender != "0" and self.sender == self.receiver:
                return False, "Отправитель и получатель не могут быть одинаковыми"

            if self.sender != "0":
                if not self.signature:
                    return False, "Отсутствует подпись"

                if not self.signature.startswith("signed_"):
                    return False, "Невалидный формат подписи"

            return True, "Транзакция валидна"

        except Exception as e:
            return False, f"Ошибка при проверке транзакции: {str(e)}"

    def __repr__(self):
        return f"Transaction({self.sender} -> {self.receiver}: {self.amount} BTC)"


class Block:
    def __init__(self, index: int, transactions: List[Transaction], previous_hash: str, timestamp: float = None):
        self.index = index
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.timestamp = timestamp or time.time()
        self.nonce = 0
        self.difficulty = 0
        self.miner = None
        self.hash = self.calculate_hash()
        self.mining_duration = 0

    def calculate_hash(self) -> str:
        block_string = json.dumps({
            'index': self.index,
            'transactions': [tx.to_dict() for tx in self.transactions],
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'nonce': self.nonce,
            'difficulty': self.difficulty
        }, sort_keys=True)
        return hashlib.sha256(block_string.encode()).hexdigest()

    def mine_block(self, difficulty: int, miner_address: str = None):
        self.difficulty = difficulty
        self.miner = miner_address
        target = "0" * difficulty

        print(f"Майнинг блока #{self.index} (сложность: {difficulty})...")
        start_time = time.time()
        attempts = 0

        while self.hash[:difficulty] != target:
            self.nonce += 1
            attempts += 1
            self.hash = self.calculate_hash()

            if attempts % 10000 == 0:
                print(f"  Попыток: {attempts}, текущий хеш: {self.hash[:20]}...")

        end_time = time.time()
        self.mining_duration = end_time - start_time

        print(f"Блок #{self.index} успешно замайнен!")
        print(f"   Хеш: {self.hash}")
        print(f"   Nonce: {self.nonce}")
        print(f"   Попыток: {attempts}")
        print(f"   Время: {self.mining_duration:.2f} сек")
        print(f"   Майнер: {miner_address}")

    def has_valid_transactions(self) -> bool:
        for transaction in self.transactions:
            if not transaction.is_valid():
                print(f"Невалидная транзакция: {transaction}")
                return False
        return True

    def get_total_fees(self) -> float:
        return sum(tx.fee for tx in self.transactions if tx.sender != "0")

    def verify_integrity(self) -> Tuple[bool, str]:
        try:
            calculated_hash = self.calculate_hash()
            if self.hash != calculated_hash:
                return False, f"Хеш блока не совпадает. Ожидался: {calculated_hash}"

            if self.index < 0:
                return False, "Индекс блока должен быть неотрицательным"

            if not isinstance(self.transactions, list):
                return False, "Транзакции должны быть списком"

            if not self.previous_hash:
                return False, "Отсутствует хеш предыдущего блока"

            if self.difficulty > 0 and not self.hash.startswith("0" * self.difficulty):
                return False, f"Блок не удовлетворяет сложности {self.difficulty}"

            current_time = time.time()
            if self.timestamp > current_time + 7200:
                return False, "Временная метка блока в будущем"

            return True, "Блок валиден"

        except Exception as e:
            return False, f"Ошибка при проверке блока: {str(e)}"


class Blockchain:
    def __init__(self, difficulty: int = 2):
        self.chain: List[Block] = [self.create_genesis_block()]
        self.difficulty = difficulty
        self.pending_transactions: List[Transaction] = []
        self.mining_reward = 50.0
        self.block_reward_halving_interval = 210000
        self.wallets: Dict[str, float] = {}
        self.total_blocks_mined = 0
        self.total_transactions_processed = 0
        self.security_log: List[str] = []

    def create_genesis_block(self) -> Block:
        genesis_transaction = Transaction("0", "founder", 50.0)
        genesis_transaction.sign_transaction()
        return Block(0, [genesis_transaction], "0")

    def get_current_block_reward(self) -> float:
        halvings = self.total_blocks_mined // self.block_reward_halving_interval
        current_reward = self.mining_reward / (2 ** halvings)
        return current_reward

    def create_wallet(self, name: str, initial_balance: float = 100.0):
        if name in self.wallets:
            print(f"Кошелек '{name}' уже существует!")
            return False

        if name == "0":
            print("Нельзя создать кошелек с именем '0'")
            return False

        self.wallets[name] = initial_balance
        print(f"Создан кошелек '{name}' с балансом {initial_balance} BTC")
        return True

    def get_balance(self, wallet_name: str) -> float:
        return self.wallets.get(wallet_name, 0.0)

    def transfer(self, from_wallet: str, to_wallet: str, amount: float, fee: float = 0.1) -> bool:
        if from_wallet not in self.wallets:
            print(f"Кошелек отправителя '{from_wallet}' не найден")
            return False

        if to_wallet not in self.wallets:
            print(f"Кошелек получателя '{to_wallet}' не найден")
            return False

        total_cost = amount + fee
        if self.wallets[from_wallet] < total_cost:
            print(f"Недостаточно средств. Нужно: {total_cost} BTC, доступно: {self.wallets[from_wallet]} BTC")
            return False

        transaction = Transaction(from_wallet, to_wallet, amount)
        transaction.fee = fee
        transaction.sign_transaction()

        if self.add_transaction(transaction):
            print(f"Перевод: {from_wallet} -> {to_wallet}: {amount} BTC (комиссия: {fee} BTC)")
            return True

        return False

    def add_transaction(self, transaction: Transaction) -> bool:
        if not transaction.is_valid():
            print("Невалидная транзакция")
            return False

        self.pending_transactions.append(transaction)
        print(f"Транзакция добавлена в пул: {transaction}")
        return True

    def select_transactions_for_block(self, max_transactions: int = 10) -> List[Transaction]:
        sorted_transactions = sorted(
            self.pending_transactions,
            key=lambda tx: tx.fee,
            reverse=True
        )

        selected = sorted_transactions[:max_transactions]

        print(f"Отобрано {len(selected)} транзакций из {len(self.pending_transactions)}")
        total_fees = sum(tx.fee for tx in selected)
        print(f"Общая комиссия в блоке: {total_fees} BTC")

        return selected

    def mine_pending_transactions(self, mining_reward_address: str, max_transactions: int = 10):
        if not self.pending_transactions:
            print("Нет транзакций для майнинга")
            return

        selected_transactions = self.select_transactions_for_block(max_transactions)

        print(f"Начинаем майнинг блока #{len(self.chain)}...")
        print(f"Транзакций в блоке: {len(selected_transactions)}")
        print(f"Сложность: {self.difficulty}")

        new_block = Block(
            len(self.chain),
            selected_transactions,
            self.get_latest_block().hash
        )

        new_block.mine_block(self.difficulty, mining_reward_address)

        block_reward = self.get_current_block_reward()
        total_fees = new_block.get_total_fees()

        reward_transaction = Transaction("0", mining_reward_address, block_reward)
        reward_transaction.sign_transaction()

        for tx in selected_transactions:
            if tx in self.pending_transactions:
                self.pending_transactions.remove(tx)

        self.pending_transactions.append(reward_transaction)
        self.chain.append(new_block)

        self._update_balances(new_block, block_reward)

        self.total_blocks_mined += 1
        self.total_transactions_processed += len(selected_transactions)

        print(f"Блок #{new_block.index} успешно добавлен в цепь!")
        print(f"Майнер {mining_reward_address} получает: {block_reward + total_fees} BTC")
        print(f"   (Награда за блок: {block_reward} BTC + комиссии: {total_fees} BTC)")

        self.print_network_stats()

    def _update_balances(self, block: Block, block_reward: float):
        total_fees = 0

        for transaction in block.transactions:
            if transaction.sender != "0":
                total_amount = transaction.amount + transaction.fee
                self.wallets[transaction.sender] = self.get_balance(transaction.sender) - total_amount
                total_fees += transaction.fee

            self.wallets[transaction.receiver] = self.get_balance(transaction.receiver) + transaction.amount

        if block.miner:
            self.wallets[block.miner] = self.get_balance(block.miner) + block_reward + total_fees

    def print_network_stats(self):
        print(f"СТАТИСТИКА СЕТИ:")
        print(f"   Всего блоков: {len(self.chain)}")
        print(f"   Всего транзакций: {self.total_transactions_processed}")
        print(f"   Текущая награда за блок: {self.get_current_block_reward()} BTC")
        print(f"   Транзакций в пуле ожидания: {len(self.pending_transactions)}")
        print(f"   Кошельков в системе: {len(self.wallets)}")

    def is_chain_valid(self, verbose: bool = False) -> Tuple[bool, List[str]]:
        errors = []

        genesis_block = self.chain[0]
        genesis_valid, genesis_msg = genesis_block.verify_integrity()
        if not genesis_valid:
            errors.append(f"Генезис-блок: {genesis_msg}")
            if verbose:
                print(f"Генезис-блок: {genesis_msg}")

        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if verbose:
                print(f"Проверка блока #{current_block.index}...")

            block_valid, block_msg = current_block.verify_integrity()
            if not block_valid:
                errors.append(f"Блок #{current_block.index}: {block_msg}")
                if verbose:
                    print(f"Блок #{current_block.index}: {block_msg}")

            if current_block.previous_hash != previous_block.hash:
                error_msg = f"Блок #{current_block.index}: нарушена связь с предыдущим блоком"
                errors.append(error_msg)
                if verbose:
                    print(error_msg)

            if not current_block.has_valid_transactions():
                error_msg = f"Блок #{current_block.index}: содержит невалидные транзакции"
                errors.append(error_msg)
                if verbose:
                    print(error_msg)

            if current_block.index != previous_block.index + 1:
                error_msg = f"Блок #{current_block.index}: нарушена последовательность индексов"
                errors.append(error_msg)
                if verbose:
                    print(error_msg)

        is_valid = len(errors) == 0
        if is_valid and verbose:
            print("Цепь полностью валидна!")

        return is_valid, errors

    def get_latest_block(self) -> Block:
        return self.chain[-1]

    def get_chain_length(self) -> int:
        return len(self.chain)

    def print_chain(self):
        print(f"БЛОКЧЕЙН (всего блоков: {len(self.chain)})")
        for block in self.chain:
            print(f"Блок #{block.index}:")
            print(f"  Хеш: {block.hash}")
            print(f"  Предыдущий: {block.previous_hash}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Сложность: {block.difficulty}")
            print(f"  Майнер: {block.miner}")
            print(f"  Транзакций: {len(block.transactions)}")
            print(f"  Время майнинга: {block.mining_duration:.2f} сек")

            for tx in block.transactions:
                fee_info = f" (комиссия: {tx.fee} BTC)" if tx.fee > 0 else ""
                print(f"    - {tx.sender} -> {tx.receiver}: {tx.amount} BTC{fee_info}")