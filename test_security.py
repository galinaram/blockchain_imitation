# test_security.py
from blockchain import Blockchain, Transaction
import time


def test_comprehensive_security():
    print("=== ТЕСТ 1: Комплексная проверка безопасности ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Bob", 50.0)
    blockchain.create_wallet("Miner1", 0.0)

    # Создаем нормальные транзакции
    tx1 = Transaction("Alice", "Bob", 25.0)
    tx1.fee = 0.5
    tx1.sign_transaction()

    tx2 = Transaction("Bob", "Alice", 10.0)
    tx2.fee = 0.2
    tx2.sign_transaction()

    blockchain.add_transaction(tx1)
    blockchain.add_transaction(tx2)
    blockchain.mine_pending_transactions("Miner1")

    # Проверяем безопасность
    print("\n🔒 Проверка безопасности после нормальных операций:")
    report = blockchain.detect_tampering()
    print(f"   Вмешательство обнаружено: {report['tampering_detected']}")
    print(f"   Цепь валидна: {report['chain_valid']}")

    # Проверяем логи безопасности
    print(f"\n📋 Логи безопасности ({len(blockchain.security_log)} записей):")
    for log in blockchain.security_log[-3:]:  # Последние 3 записи
        print(f"   {log}")

    print()


def test_transaction_validation():
    print("=== ТЕСТ 2: Расширенная валидация транзакций ===")

    # Тестируем различные сценарии транзакций
    test_cases = [
        ("Alice", "Bob", 25.0, True, "Нормальная транзакция"),
        ("Alice", "Alice", 10.0, False, "Отправитель = получатель"),
        ("Alice", "Bob", -5.0, False, "Отрицательная сумма"),
        ("", "Bob", 10.0, False, "Пустой отправитель"),
        ("Alice", "", 10.0, False, "Пустой получатель"),
        ("0", "Miner", 50.0, True, "Mining reward"),
    ]

    for sender, receiver, amount, should_be_valid, description in test_cases:
        tx = Transaction(sender, receiver, amount)
        if sender != "0":  # Mining reward не требует подписи
            tx.sign_transaction()

        is_valid, message = tx.verify_integrity()
        status = "✅" if is_valid == should_be_valid else "❌"
        print(f"   {status} {description}: {message}")


def test_chain_manipulation():
    print("\n=== ТЕСТ 3: Обнаружение манипуляций с цепью ===")

    blockchain = Blockchain(difficulty=2)
    blockchain.create_wallet("Alice", 100.0)
    blockchain.create_wallet("Miner1", 0.0)

    # Создаем нормальный блок
    tx = Transaction("Alice", "Miner1", 10.0)
    tx.sign_transaction()
    blockchain.add_transaction(tx)
    blockchain.mine_pending_transactions("Miner1")

    print("Исходное состояние:")
    is_valid, errors = blockchain.is_chain_valid()
    print(f"   Цепь валидна: {is_valid}")

    # Манипулируем цепью
    print("\nМанипулируем цепью...")
    blockchain.chain[1].transactions[0].amount = 1000.0  # Изменяем сумму

    print("После манипуляции:")
    is_valid, errors = blockchain.is_chain_valid(verbose=True)
    print(f"   Цепь валидна: {is_valid}")

    # Проверяем отчет безопасности
    report = blockchain.detect_tampering()
    print(f"   Вмешательство обнаружено: {report['tampering_detected']}")

    print()


def run_all_security_tests():
    """Запуск всех тестов безопасности"""
    print("🔒 ТЕСТИРОВАНИЕ СИСТЕМЫ БЕЗОПАСНОСТИ БЛОКЧЕЙНА 🔒\n")

    test_comprehensive_security()
    test_transaction_validation()
    test_chain_manipulation()

    print("🎉 ТЕСТЫ БЕЗОПАСНОСТИ ЗАВЕРШЕНЫ! 🎉")


if __name__ == "__main__":
    run_all_security_tests()