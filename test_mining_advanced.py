# test_mining_advanced.py
import time
from blockchain import Blockchain, Transaction


def test_mining_reward_system():
    print("=== ТЕСТ 1: Система наград за майнинг ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Miner1", 0.0)
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Bob", 50.0)

    print(f"Текущая награда за блок: {blockchain.get_current_block_reward()} BTC")

    # Создаем транзакции
    tx1 = Transaction("Alice", "Bob", 25.0)
    tx1.fee = 0.5
    tx1.sign_transaction()

    tx2 = Transaction("Bob", "Alice", 10.0)
    tx2.fee = 0.2
    tx2.sign_transaction()

    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)

    # Майним блок
    blockchain.mine_pending_transactions("Miner1")

    print(f"Баланс майнера: {blockchain.get_balance('Miner1')} BTC")
    print()


def test_difficulty_adjustment():
    print("=== ТЕСТ 2: Регулировка сложности ===")

    blockchain = Blockchain(difficulty=1)
    blockchain.create_wallet("Miner1", 0.0)
    blockchain.create_wallet("Test", 100.0)

    print(f"Начальная сложность: {blockchain.difficulty}")

    # Создаем несколько блоков для тестирования регулировки
    for i in range(3):
        tx = Transaction("Test", "Test", 1.0)
        tx.sign_transaction()
        blockchain.add_transaction(tx)
        blockchain.mine_pending_transactions("Miner1")

        # Имитируем разное время создания блоков
        if i == 1:
            print("Имитация быстрого создания блока...")
            blockchain.adjust_difficulty(target_block_time=10)
        elif i == 2:
            print("Имитация медленного создания блока...")
            blockchain.adjust_difficulty(target_block_time=300)

    print(f"Финальная сложность: {blockchain.difficulty}")
    print()


def test_transaction_selection():
    print("=== ТЕСТ 3: Выбор транзакций по комиссии ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Miner1", 0.0)
    blockchain.create_wallet("Alice", 200.0)
    blockchain.create_wallet("Bob", 100.0)
    blockchain.create_wallet("Charlie", 50.0)

    # Создаем транзакции с разными комиссиями
    transactions = [
        ("Alice", "Bob", 10.0, 0.1),
        ("Bob", "Charlie", 5.0, 0.5),  # Высокая комиссия
        ("Charlie", "Alice", 2.0, 0.01),  # Низкая комиссия
        ("Alice", "Charlie", 8.0, 0.3),
    ]

    for sender, receiver, amount, fee in transactions:
        tx = Transaction(sender, receiver, amount)
        tx.fee = fee
        tx.sign_transaction()
        blockchain.add_transaction(tx)

    print(f"Транзакций в пуле: {len(blockchain.pending_transactions)}")

    # Выбираем транзакции для блока (максимум 2)
    selected = blockchain.select_transactions_for_block(max_transactions=2)

    print("Выбранные транзакции (по highest fee):")
    for tx in selected:
        print(f"  {tx.sender} -> {tx.receiver}: {tx.amount} BTC (fee: {tx.fee} BTC)")
    print()


def test_wallet_system():
    print("=== ТЕСТ 4: Система кошельков ===")

    blockchain = Blockchain(difficulty=2)

    # Создаем кошельки
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Bob", 50.0)
    blockchain.create_wallet("Miner1", 0.0)

    # Используем упрощенный перевод
    print("Тестируем переводы между кошельками...")
    blockchain.transfer("Alice", "Bob", 25.0, fee=0.1)
    blockchain.transfer("Bob", "Alice", 5.0, fee=0.05)

    # Пытаемся перевести больше чем есть
    blockchain.transfer("Alice", "Bob", 1000.0, fee=1.0)

    print("\nФинальные балансы:")
    for wallet in ["Alice", "Bob", "Miner1"]:
        balance = blockchain.get_balance(wallet)
        print(f"  {wallet}: {balance} BTC")
    print()


def test_network_statistics():
    print("=== ТЕСТ 5: Статистика сети ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Miner1", 0.0)
    blockchain.create_wallet("User1", 100.0)
    blockchain.create_wallet("User2", 50.0)

    # Создаем несколько блоков
    for i in range(3):
        tx1 = Transaction("User1", "User2", 5.0 * (i + 1))
        tx1.fee = 0.1
        tx1.sign_transaction()

        tx2 = Transaction("User2", "User1", 2.0 * (i + 1))
        tx2.fee = 0.05
        tx2.sign_transaction()

        blockchain.add_transaction(tx1)
        blockchain.add_transaction(tx2)
        blockchain.mine_pending_transactions("Miner1")

    blockchain.print_network_stats()
    print()


def run_all_mining_tests():
    """Запуск всех тестов майнинга"""
    print("🧪 ТЕСТИРОВАНИЕ УЛУЧШЕННОЙ СИСТЕМЫ МАЙНИНГА 🧪\n")

    test_mining_reward_system()
    test_difficulty_adjustment()
    test_transaction_selection()
    test_wallet_system()
    test_network_statistics()

    print("🎉 ТЕСТЫ МАЙНИНГА ЗАВЕРШЕНЫ! 🎉")


if __name__ == "__main__":
    run_all_mining_tests()