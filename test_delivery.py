import unittest
import logging
import sys
import os
from Delivery import calculate_delivery_cost

# Логер будто всё же нужен
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger("delivery_tests")
logger.setLevel(logging.DEBUG)

if not logger.handlers:
    # метод для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(console_handler)

    # метод для файла
    file_handler = logging.FileHandler("logs/delivery_tests.log", encoding="utf-8", mode="w")  # mode="w" — перезаписывает файл при каждом запуске
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(logging.Formatter(log_format, datefmt=date_format))
    logger.addHandler(file_handler)


class TestDeliveryCost(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=" * 40)
        logger.info("Автотесты 'Delivery.py'")
        logger.info("=" * 40)

    @classmethod
    def tearDownClass(cls):
        logger.info("=" * 40)
        logger.info("Завершение автотестов'Delivery.py'")
        logger.info("=" * 40)

    def test_01_basic(self):
        logger.info("[ТЕСТ 1/10] Базовый расчёт (вес 2кг, 100км, обычный)")
        cost, date = calculate_delivery_cost(2.0, 100, "обычный")
        logger.info(f"  Результат: стоимость={cost} руб, дата={date}")
        self.assertEqual(cost, 700)

    def test_02_medium_weight(self):
        logger.info("[ТЕСТ 2/10] Средний вес (10кг, коэф. 1.2)")
        cost, _ = calculate_delivery_cost(10.0, 100, "обычный")
        logger.info(f"  Результат: стоимость={cost} руб")
        self.assertEqual(cost, 840)

    def test_03_heavy_weight(self):
        logger.info("[ТЕСТ 3/10] Тяжёлый вес (25кг, коэф. 1.5)")
        cost, _ = calculate_delivery_cost(25.0, 100, "обычный")
        logger.info(f"  Результат: стоимость={cost} руб")
        self.assertEqual(cost, 1050)

    def test_04_fragile(self):
        logger.info("[ТЕСТ 4/10] Хрупкий груз (+300 руб)")
        cost, _ = calculate_delivery_cost(2.0, 100, "хрупкий")
        logger.info(f"  Результат: стоимость={cost} руб")
        self.assertEqual(cost, 1000)

    def test_05_dangerous(self):
        logger.info("[ТЕСТ 5/10] Опасный груз (+1000 руб)")
        cost, _ = calculate_delivery_cost(2.0, 100, "опасный")
        logger.info(f"  Результат: стоимость={cost} руб")
        self.assertEqual(cost, 1700)

    def test_06_express_cost(self):
        logger.info("[ТЕСТ 6/10] Экспресс-доставка (должна быть дороже)")
        cost, _ = calculate_delivery_cost(2.0, 100, "обычный", is_express=True)
        logger.info(f"  Результат: стоимость={cost} руб")
        self.assertGreater(cost, 700)

    def test_07_invalid_weight_low(self):
        logger.info("[ТЕСТ 7/10] Невалидный вес (слишком лёгкий, 0.05кг)")
        cost, date = calculate_delivery_cost(0.05, 100, "обычный")
        logger.info(f"  Результат: стоимость={cost}, дата={date}")
        self.assertEqual(cost, -1)
        self.assertEqual(date, "0000-00-00")

    def test_08_invalid_weight_high(self):
        logger.info("[ТЕСТ 8/10] Невалидный вес (слишком тяжёлый, 55кг)")
        cost, _ = calculate_delivery_cost(55.0, 100, "обычный")
        logger.info(f"  Результат: стоимость={cost}")
        self.assertEqual(cost, -1)

    def test_09_invalid_distance(self):
        logger.info("[ТЕСТ 9/10] Невалидное расстояние (6000 км)")
        cost, _ = calculate_delivery_cost(5.0, 6000, "обычный")
        logger.info(f"  Результат: стоимость={cost}")
        self.assertEqual(cost, -1)

    def test_10_invalid_type(self):
        logger.info("[ТЕСТ 10/10] Невалидный тип посылки ('космический')")
        cost, _ = calculate_delivery_cost(5.0, 100, "космический")
        logger.info(f"  Результат: стоимость={cost}")
        self.assertEqual(cost, -1)


if __name__ == "__main__":
    unittest.main()