# test_transactions.py
import time
from blockchain import Transaction, Blockchain


def test_transaction_creation():
    print("=== ТЕСТ 1: Создание транзакции ===")
    tx = Transaction("Alice", "Bob", 50.0)
    tx.sign_transaction()

    print(f"Отправитель: {tx.sender}")
    print(f"Получатель: {tx.receiver}")
    print(f"Сумма: {tx.amount}")
    print(f"ID: {tx.transaction_id}")
    print(f"Подпись: {tx.signature}")
    print(f"Валидна: {tx.is_valid()}")
    print()


def test_transaction_validation():
    print("=== ТЕСТ 2: Валидация транзакций ===")

    # Валидная транзакция
    valid_tx = Transaction("Alice", "Bob", 25.0)
    valid_tx.sign_transaction()
    print(f"Валидная транзакция: {valid_tx.is_valid()}")

    # Транзакция без подписи
    unsigned_tx = Transaction("Alice", "Bob", 25.0)
    print(f"Транзакция без подписи: {unsigned_tx.is_valid()}")

    # Транзакция с отрицательной суммой
    negative_tx = Transaction("Alice", "Bob", -10.0)
    negative_tx.sign_transaction()
    print(f"Транзакция с отрицательной суммой: {negative_tx.is_valid()}")

    # Mining reward транзакция
    reward_tx = Transaction("0", "Miner", 10.0)
    reward_tx.sign_transaction()
    print(f"Mining reward транзакция: {reward_tx.is_valid()}")
    print()


def test_blockchain_with_transactions():
    print("=== ТЕСТ 3: Блокчейн с транзакциями ===")

    blockchain = Blockchain(difficulty=2)

    # Создаем кошельки
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Bob", 50.0)
    blockchain.create_wallet("Miner1", 0.0)

    print(f"\nНачальные балансы:")
    print(f"Alice: {blockchain.get_balance('Alice')} BTC")
    print(f"Bob: {blockchain.get_balance('Bob')} BTC")
    print(f"Miner1: {blockchain.get_balance('Miner1')} BTC")

    # Создаем транзакции
    tx1 = Transaction("Alice", "Bob", 30.0)
    tx1.sign_transaction()

    tx2 = Transaction("Bob", "Alice", 10.0)
    tx2.sign_transaction()

    # Добавляем транзакции
    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)

    # Майним блок
    blockchain.mine_pending_transactions("Miner1")

    print(f"\nБалансы после майнинга:")
    print(f"Alice: {blockchain.get_balance('Alice')} BTC")
    print(f"Bob: {blockchain.get_balance('Bob')} BTC")
    print(f"Miner1: {blockchain.get_balance('Miner1')} BTC")

    # Проверяем валидность цепи
    print(f"\nЦепь валидна: {blockchain.is_chain_valid()}")
    print()


def test_insufficient_funds():
    print("=== ТЕСТ 4: Проверка недостатка средств ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Alice", 10.0)
    blockchain.create_wallet("Bob", 0.0)

    # Пытаемся отправить больше чем есть
    tx = Transaction("Alice", "Bob", 100.0)
    tx.sign_transaction()

    result = blockchain.add_transaction(tx)
    print(f"Транзакция с недостатком средств добавлена: {result}")
    print()


def test_transaction_in_block():
    print("=== ТЕСТ 5: Транзакции в блоке ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Bob", 0.0)

    tx = Transaction("Alice", "Bob", 25.0)
    tx.sign_transaction()
    blockchain.add_transaction(tx)
    blockchain.mine_pending_transactions("Miner1")

    # Проверяем что транзакция попала в блок
    latest_block = blockchain.get_latest_block()
    print(f"Блок #{latest_block.index} содержит {len(latest_block.transactions)} транзакций")

    for block_tx in latest_block.transactions:
        print(f"  - {block_tx}")
        print(f"    Валидна: {block_tx.is_valid()}")

    print(f"Все транзакции в блоке валидны: {latest_block.has_valid_transactions()}")


def run_all_transaction_tests():
    """Запуск всех тестов транзакций"""
    print("🧪 ТЕСТИРОВАНИЕ СИСТЕМЫ ТРАНЗАКЦИЙ 🧪\n")

    test_transaction_creation()
    test_transaction_validation()
    test_blockchain_with_transactions()
    test_insufficient_funds()
    test_transaction_in_block()

    print("🎉 ТЕСТЫ ТРАНЗАКЦИЙ ЗАВЕРШЕНЫ! 🎉")


if __name__ == "__main__":
    run_all_transaction_tests()