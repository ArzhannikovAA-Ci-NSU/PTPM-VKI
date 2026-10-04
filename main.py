import logging
import sys
import math
import os

# логи
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


def process_triangle(side_a: str, side_b: str, side_c: str):
    logging.info(f"Получен запрос: A='{side_a}', B='{side_b}', C='{side_c}'")

    try:
        a = float(side_a)
        b = float(side_b)
        c = float(side_c)
    except ValueError as e:
        logging.error("Ошибка: получены невалидные (нечисловые) данные.")
        logging.exception("Трассировка стека исключения:")
        return "", [(-2, -2), (-2, -2), (-2, -2)]

    # 2. Проверка на положительность и неравенство треугольника
    if a <= 0 or b <= 0 or c <= 0:
        logging.warning("Ошибка: стороны должны быть строго положительными числами.")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    if a + b <= c or a + c <= b or b + c <= a:
        logging.warning("Ошибка: нарушено неравенство треугольника.")
        return "не треугольник", [(-1, -1), (-1, -1), (-1, -1)]

    # 3. Определение типа треугольника
    if a == b == c:
        tri_type = "равносторонний"
    elif a == b or a == c or b == c:
        tri_type = "равнобедренный"
    else:
        tri_type = "разносторонний"

    # координаты вершин
    x1, y1 = 0.0, 0.0
    x2, y2 = c, 0.0

    x3 = (b ** 2 + c ** 2 - a ** 2) / (2 * c)
    y3_squared = b ** 2 - x3 ** 2

    y3 = math.sqrt(max(0, y3_squared))

    # до целых чисел
    coords_int = [(round(x1), round(y1)), (round(x2), round(y2)), (round(x3), round(y3))]

    logging.info(f"Успешный запрос. Тип: '{tri_type}', Координаты: {coords_int}")
    return tri_type, coords_int


if __name__ == "__main__":
    logging.info("Приложение запущено")

    # Ручной ввод с консоли
    side_a = input("Сторона A: ")
    side_b = input("Сторона B: ")
    side_c = input("Сторона C: ")

    print(f"\nОбработка введенных данных: A='{side_a}', B='{side_b}', C='{side_c}'")
    res_type, res_coords = process_triangle(side_a, side_b, side_c)
    print(f"\nРезультат: {res_type}, {res_coords}")

    logging.info("Приложение завершено")
