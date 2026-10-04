import unittest
import logging
import sys
import os
from main import process_triangle


# аналогична лабе1
log_format = "%(asctime)s | [%(levelname)-7s] | %(message)s"
date_format = "%Y-%m-%d %H:%M:%S"
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.DEBUG,
    format=log_format,
    datefmt=date_format,
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("logs/file_txt.log", encoding="utf-8")
    ]
)
logger = logging.getLogger(__name__)


class TestTriangleProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logger.info("=" * 30)
        logger.info("Автотесты 'main.py'")
        logger.info("=" * 30)

    @classmethod
    def tearDownClass(cls):
        logger.info("=" * 40)
        logger.info("Завершение автотестов 'main.py'")
        logger.info("=" * 40)

    def test_01_scalene(self):
        logger.info("[ТЕСТ 1/10] Разносторонний треугольник (3, 4, 5)")
        self.assertEqual(process_triangle("3", "4", "5")[0], "разносторонний")

    def test_02_isosceles(self):
        logger.info("[ТЕСТ 2/10] Равнобедренный треугольник (5, 5, 8)")
        self.assertEqual(process_triangle("5", "5", "8")[0], "равнобедренный")

    def test_03_equilateral(self):
        logger.info("[ТЕСТ 3/10] Равносторонний треугольник (6, 6, 6)")
        self.assertEqual(process_triangle("6", "6", "6")[0], "равносторонний")

    def test_04_floats(self):
        logger.info("[ТЕСТ 4/10] Дробные числа (3.5, 4.2, 5.1)")
        res_type, coords = process_triangle("3.5", "4.2", "5.1")
        self.assertEqual(res_type, "разносторонний")
        self.assertIsInstance(coords, list)

    def test_05_non_numeric(self):
        logger.info("[ТЕСТ 5/10] Нечисловые данные ('abc', '4', '5')")
        res_type, coords = process_triangle("abc", "4", "5")
        self.assertEqual(res_type, "")
        self.assertEqual(coords, [(-2, -2), (-2, -2), (-2, -2)])

    def test_06_zero_side(self):
        logger.info("[ТЕСТ 6/10] Нулевая сторона ('0', '4', '5')")
        res_type, coords = process_triangle("0", "4", "5")
        self.assertEqual(res_type, "не треугольник")
        self.assertEqual(coords, [(-1, -1), (-1, -1), (-1, -1)])

    def test_07_negative_side(self):
        logger.info("[ТЕСТ 7/10] Отрицательная сторона ('-3', '4', '5')")
        res_type, _ = process_triangle("-3", "4", "5")
        self.assertEqual(res_type, "не треугольник")

    def test_08_inequality(self):
        logger.info("[ТЕСТ 8/10] Нарушение неравенства ('1', '2', '10')")
        res_type, _ = process_triangle("1", "2", "10")
        self.assertEqual(res_type, "не треугольник")

    def test_09_empty_string(self):
        logger.info("[ТЕСТ 9/10] Пустая строка ('', '4', '5')")
        res_type, _ = process_triangle("", "4", "5")
        self.assertEqual(res_type, "")

    def test_10_boundary_inequality(self):
        logger.info("[ТЕСТ 10/10] Пограничный случай ('2', '2', '4')")
        res_type, _ = process_triangle("2", "2", "4")
        self.assertEqual(res_type, "не треугольник")


if __name__ == "__main__":
    unittest.main()