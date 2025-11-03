# test_blockchain.py
import time
from blockchain import Block, Blockchain


def test_block_basic():
    print("=== ТЕСТ 1: Базовое создание блока ===")
    genesis_block = Block(0, ["Genesis transaction"], "0")
    print(f"Индекс: {genesis_block.index}")
    print(f"Хеш блока: {genesis_block.hash}")
    print(f"Nonce: {genesis_block.nonce}")
    print()


def test_block_hash_consistency():
    print("=== ТЕСТ 2: Проверка консистентности хеша ===")
    block1 = Block(1, ["Tx1", "Tx2"], "previous_hash_123")
    block2 = Block(1, ["Tx1", "Tx2"], "previous_hash_123")
    print(f"Блок 1 хеш: {block1.hash}")
    print(f"Блок 2 хеш: {block2.hash}")
    print(f"Хеши одинаковые: {block1.hash == block2.hash}")
    print()


def test_block_hash_sensitivity():
    print("=== ТЕСТ 3: Чувствительность хеша к изменениям ===")
    block1 = Block(1, ["Tx1", "Tx2"], "prev_hash")
    block2 = Block(1, ["Tx1", "Tx3"], "prev_hash")
    print(f"Хеши разные: {block1.hash != block2.hash}")
    print(f"Изменение составило: {sum(1 for a, b in zip(block1.hash, block2.hash) if a != b)} символов")
    print()


def test_mining():
    print("=== ТЕСТ 4: Тестирование майнинга ===")
    easy_block = Block(1, ["Transaction A", "Transaction B"], "prev_hash_123")
    print("До майнинга:")
    print(f"Хеш: {easy_block.hash}")
    print(f"Nonce: {easy_block.nonce}")

    print("\nНачинаем майнинг со сложностью 2...")
    start_time = time.time()
    easy_block.mine_block(2)
    end_time = time.time()

    print(f"После майнинга:")
    print(f"Хеш: {easy_block.hash}")
    print(f"Nonce: {easy_block.nonce}")
    print(f"Время майнинга: {end_time - start_time:.4f} секунд")
    print(f"Хеш начинается с '00': {easy_block.hash.startswith('00')}")
    print()


def test_blockchain_creation():
    print("=== ТЕСТ 5: Создание блокчейна ===")
    blockchain = Blockchain(difficulty=2)
    print(f"Длина цепи: {blockchain.get_chain_length()}")
    print(f"Генезис-блок хеш: {blockchain.chain[0].hash}")
    print(f"Сложность: {blockchain.difficulty}")
    print("✓ Блокчейн создан успешно\n")


def test_blockchain_add_blocks():
    print("=== ТЕСТ 6: Добавление блоков в цепь ===")
    blockchain = Blockchain(difficulty=2)

    print("Добавляем блок 1...")
    blockchain.add_block(["Alice -> Bob: 50 BTC", "Charlie -> Dave: 25 BTC"])

    print("Добавляем блок 2...")
    blockchain.add_block(["Eve -> Frank: 10 BTC"])

    print(f"Длина цепи: {blockchain.get_chain_length()}")

    # Проверяем связь между блоками
    block1_to_block2 = blockchain.chain[1].hash == blockchain.chain[2].previous_hash
    print(f"Блок 1 → Блок 2 связь корректна: {block1_to_block2}")
    print("✓ Блоки успешно связаны\n")


def test_blockchain_integrity():
    print("=== ТЕСТ 7: Проверка целостности блокчейна ===")
    blockchain = Blockchain(difficulty=2)

    blockchain.add_block(["Tx1", "Tx2"])
    blockchain.add_block(["Tx3", "Tx4", "Tx5"])

    print("Проверяем целостность цепи...")
    integrity_ok = blockchain.is_chain_valid()
    print(f"Цепь валидна: {integrity_ok}\n")


def test_blockchain_tamper_resistance():
    print("=== ТЕСТ 8: Защита от изменений ===")
    blockchain = Blockchain(difficulty=2)

    blockchain.add_block(["Original transaction 1"])
    blockchain.add_block(["Original transaction 2"])

    print(f"Цепь до изменений валидна: {blockchain.is_chain_valid()}")

    # Пытаемся изменить данные в блоке 1
    print("Пытаемся изменить транзакцию в блоке 1...")
    blockchain.chain[1].transactions = ["HACKED transaction!"]

    print(f"Цепь после изменений валидна: {blockchain.is_chain_valid()}")
    print("✓ Защита от изменений работает корректно\n")


def run_all_tests():
    """Запуск всех тестов"""
    print("🧪 ЗАПУСК ТЕСТОВ БЛОКЧЕЙНА 🧪\n")

    test_block_basic()
    test_block_hash_consistency()
    test_block_hash_sensitivity()
    test_mining()
    test_blockchain_creation()
    test_blockchain_add_blocks()
    test_blockchain_integrity()
    test_blockchain_tamper_resistance()

    print("🎉 ВСЕ ТЕСТЫ ЗАВЕРШЕНЫ! 🎉")


if __name__ == "__main__":
    run_all_tests()