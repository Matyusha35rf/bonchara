def check_and_remove_key(file_path, key):
    """
    Проверяет, есть ли ключ в файле, и удаляет его, если он найден.
    :param file_path: Путь к файлу с ключами.
    :param key: Ключ, который нужно проверить и удалить.
    :return: True, если ключ найден и удален, иначе False.
    """
    try:
        # Открываем файл для чтения
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()  # Читаем все строки

        # Проверяем, есть ли ключ в файле
        key_found = False
        updated_lines = []
        for line in lines:
            if line.strip() == key:  # Убираем лишние пробелы и символы новой строки
                key_found = True  # Ключ найден
            else:
                updated_lines.append(line)  # Сохраняем строки, кроме удаляемого ключа

        # Если ключ найден, перезаписываем файл без него
        if key_found:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.writelines(updated_lines)  # Записываем обновленные строки
            return True  # Ключ удален

        return False  # Ключ не найден

    except Exception as e:
        print(f"Ошибка при работе с файлом: {e}")
        return False