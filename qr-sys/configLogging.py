import logging
import os


def configure_logging(log_dir: str, log_filename: str = "app.log"):
    # Очистка попередніх налаштувань логування
    logging.getLogger().handlers = []

    # Перевірка, чи передано директорію
    if not log_dir:
        raise ValueError("log_dir must be provided")

    # Перевірка, чи існує директорія
    if not os.path.exists(log_dir):
        # print(f"Directory does not exist: {log_dir}")
        os.makedirs(log_dir, exist_ok=True)  # Створюємо директорію, якщо її немає

    # Створення абсолютного шляху до файлу
    log_file_path = os.path.join(log_dir, log_filename)

    # Перевірка директорії для фалу
    # print(f"Configuring logging in directory: {log_dir}")
    # print(f"Log file will be created at: {log_file_path}")

    # Налаштування логування
    logging.basicConfig(
        filename=log_file_path,
        filemode="a",  # Додає нові записи в кінець файлу
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.DEBUG,  # Рівень логів: DEBUG, INFO, WARNING, ERROR, CRITICAL
    )
    logging.info(f"Logging initialized in directory: {log_dir}")
