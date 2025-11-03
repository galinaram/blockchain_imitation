# demo_advanced.py
from blockchain import Blockchain, Transaction
import time


def advanced_demo():
    print("🚀 РАСШИРЕННАЯ ДЕМОНСТРАЦИЯ БЛОКЧЕЙНА")
    print("=" * 60)

    blockchain = Blockchain(difficulty=3)

    print("Создаем кошельки...")
    wallets = [
        ("Alice", 200.0),
        ("Bob", 150.0),
        ("Charlie", 100.0),
        ("David", 80.0),
        ("Eve", 120.0),
        ("Miner1", 0.0),
        ("Miner2", 0.0)
    ]

    for name, balance in wallets:
        blockchain.create_wallet(name, balance)

    print("\n" + "=" * 60)
    print("ЭТАП 1: Создаем несколько транзакций с разными комиссиями")
    print("=" * 60)

    transactions = [
        ("Alice", "Bob", 25.0, 0.1),
        ("Bob", "Charlie", 15.0, 0.05),
        ("Charlie", "David", 10.0, 0.2),
        ("David", "Eve", 5.0, 0.3),
        ("Eve", "Alice", 8.0, 0.15),
        ("Alice", "Charlie", 12.0, 0.25),
        ("Bob", "David", 7.0, 0.08)
    ]

    for i, (sender, receiver, amount, fee) in enumerate(transactions, 1):
        print(f"\nТранзакция {i}: {sender} -> {receiver}: {amount} BTC (комиссия: {fee} BTC)")
        blockchain.transfer(sender, receiver, amount, fee)
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("ЭТАП 2: Майнинг первого блока (Miner1)")
    print("=" * 60)

    print(f"Транзакций в пуле: {len(blockchain.pending_transactions)}")
    blockchain.mine_pending_transactions("Miner1", max_transactions=4)

    print("\nБалансы после первого блока:")
    for wallet in ["Alice", "Bob", "Charlie", "David", "Eve", "Miner1"]:
        balance = blockchain.get_balance(wallet)
        print(f"  {wallet}: {balance:.2f} BTC")

    print("\n" + "=" * 60)
    print("ЭТАП 3: Создаем еще транзакций")
    print("=" * 60)

    more_transactions = [
        ("Charlie", "Bob", 8.0, 0.4),
        ("Eve", "David", 6.0, 0.12),
        ("Alice", "Eve", 10.0, 0.18),
        ("David", "Charlie", 4.0, 0.22)
    ]

    for i, (sender, receiver, amount, fee) in enumerate(more_transactions, 1):
        print(f"\nТранзакция {i}: {sender} -> {receiver}: {amount} BTC (комиссия: {fee} BTC)")
        blockchain.transfer(sender, receiver, amount, fee)
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("ЭТАП 4: Майнинг второго блока (Miner2)")
    print("=" * 60)

    print(f"Транзакций в пуле: {len(blockchain.pending_transactions)}")
    blockchain.mine_pending_transactions("Miner2", max_transactions=3)

    print("\nБалансы после второго блока:")
    for wallet in ["Alice", "Bob", "Charlie", "David", "Eve", "Miner1", "Miner2"]:
        balance = blockchain.get_balance(wallet)
        print(f"  {wallet}: {balance:.2f} BTC")

    print("\n" + "=" * 60)
    print("ЭТАП 5: Создаем транзакции с высокими комиссиями")
    print("=" * 60)

    high_fee_transactions = [
        ("Bob", "Alice", 20.0, 1.0),
        ("Eve", "Charlie", 15.0, 0.8),
        ("David", "Bob", 12.0, 0.9)
    ]

    for i, (sender, receiver, amount, fee) in enumerate(high_fee_transactions, 1):
        print(f"\nТРАНЗАКЦИЯ С ВЫСОКОЙ КОМИССИЕЙ {i}: {sender} -> {receiver}: {amount} BTC (комиссия: {fee} BTC)")
        blockchain.transfer(sender, receiver, amount, fee)
        time.sleep(0.3)

    print("\n" + "=" * 60)
    print("ЭТАП 6: Майнинг третьего блока (Miner1)")
    print("=" * 60)

    print(f"Транзакций в пуле: {len(blockchain.pending_transactions)}")
    blockchain.mine_pending_transactions("Miner1", max_transactions=2)

    print("\n" + "=" * 60)
    print("ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ")
    print("=" * 60)

    print("\nФинальные балансы:")
    for wallet in ["Alice", "Bob", "Charlie", "David", "Eve", "Miner1", "Miner2"]:
        balance = blockchain.get_balance(wallet)
        print(f"  {wallet}: {balance:.2f} BTC")

    print("\nСтатистика майнеров:")
    miner1_balance = blockchain.get_balance("Miner1")
    miner2_balance = blockchain.get_balance("Miner2")
    print(f"  Miner1 заработал: {miner1_balance:.2f} BTC")
    print(f"  Miner2 заработал: {miner2_balance:.2f} BTC")

    print("\n" + "=" * 60)
    print("ЭТАП 7: Показываем структуру блокчейна")
    print("=" * 60)

    blockchain.print_chain()

    print("\n" + "=" * 60)
    print("ЭТАП 8: Проверка безопасности")
    print("=" * 60)

    is_valid, errors = blockchain.is_chain_valid(verbose=True)
    print(f"Цепь валидна: {is_valid}")

    if errors:
        print("Обнаруженные ошибки:")
        for error in errors:
            print(f"  - {error}")

    print("\n" + "=" * 60)
    print("ЭТАП 9: Демонстрация защиты от изменений")
    print("=" * 60)

    blockchain.simulate_tampering_attack()

    print("\n" + "=" * 60)
    print("🎉 РАСШИРЕННАЯ ДЕМОНСТРАЦИЯ УСПЕШНО ЗАВЕРШЕНА!")
    print("=" * 60)


def transaction_competition_demo():
    print("\n" + "=" * 60)
    print("🏆 ДЕМОНСТРАЦИЯ КОНКУРЕНЦИИ ТРАНЗАКЦИЙ")
    print("=" * 60)

    blockchain = Blockchain(difficulty=2)

    blockchain.create_wallet("User1", 100.0)
    blockchain.create_wallet("User2", 100.0)
    blockchain.create_wallet("User3", 100.0)
    blockchain.create_wallet("Miner", 0.0)

    print("\nСоздаем транзакции с разными комиссиями:")
    print("(Транзакции с высокими комиссиями должны быть выбраны первыми)")

    low_fee_tx = Transaction("User1", "User2", 10.0)
    low_fee_tx.fee = 0.01
    low_fee_tx.sign_transaction()
    blockchain.add_transaction(low_fee_tx)
    print(f"  Низкая комиссия: 0.01 BTC")

    medium_fee_tx = Transaction("User2", "User3", 15.0)
    medium_fee_tx.fee = 0.1
    medium_fee_tx.sign_transaction()
    blockchain.add_transaction(medium_fee_tx)
    print(f"  Средняя комиссия: 0.1 BTC")

    high_fee_tx = Transaction("User3", "User1", 20.0)
    high_fee_tx.fee = 0.5
    high_fee_tx.sign_transaction()
    blockchain.add_transaction(high_fee_tx)
    print(f"  Высокая комиссия: 0.5 BTC")

    print(f"\nВсего транзакций в пуле: {len(blockchain.pending_transactions)}")
    print("Майним блок с ограничением в 2 транзакции...")

    blockchain.mine_pending_transactions("Miner", max_transactions=2)

    print("\nРезультат: должны быть выбраны транзакции с самыми высокими комиссиями!")
    print(f"Оставшиеся транзакции в пуле: {len(blockchain.pending_transactions)}")


if __name__ == "__main__":
    advanced_demo()
    transaction_competition_demo()