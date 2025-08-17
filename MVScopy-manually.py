import os
from lxml import etree


def transfer_settings(source_dir, target_dir):
    print(f"\nНачинаем обработку. Исходная папка: {source_dir}, Целевая папка: {target_dir}")

    # Получаем списки файлов
    source_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.tmp', '.xml'))]
    target_files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.tmp', '.xml'))]

    print(f"Найдено {len(source_files)} исходных и {len(target_files)} целевых файлов")

    # Сопоставляем файлы по базовому имени (без расширения)
    file_pairs = []
    for t_file in target_files:
        t_base = os.path.splitext(t_file)[0]
        for s_file in source_files:
            s_base = os.path.splitext(s_file)[0]
            if s_base == t_base:
                file_pairs.append((s_file, t_file))
                break

    if not file_pairs:
        print("ОШИБКА: Нет парных файлов для обработки")
        return

    print(f"Найдено {len(file_pairs)} пар файлов для обработки")

    for s_file, t_file in file_pairs:
        print(f"\nОбработка: {s_file} -> {t_file}")

        try:
            # Читаем исходный файл с учетом BOM
            s_path = os.path.join(source_dir, s_file)
            with open(s_path, 'rb') as f:
                s_content = f.read()
                # Определяем наличие BOM
                has_bom = s_content.startswith(b'\xef\xbb\xbf')
                # Читаем содержимое как UTF-8
                s_content = s_content.decode('utf-8-sig')  # -sig убирает BOM при декодировании

            # Парсим XML
            s_tree = etree.fromstring(s_content.encode('utf-8'))

            # Читаем целевой файл
            t_path = os.path.join(target_dir, t_file)
            with open(t_path, 'rb') as f:
                t_content = f.read()
                t_has_bom = t_content.startswith(b'\xef\xbb\xbf')
                t_content = t_content.decode('utf-8-sig')

            # Парсим целевой XML с сохранением форматирования
            parser = etree.XMLParser(remove_blank_text=False, strip_cdata=False)
            t_tree = etree.fromstring(t_content.encode('utf-8'), parser)

            # Собираем значения из исходного файла
            source_values = {}
            for section in s_tree:
                for elem in section:
                    if 'Value' in elem.attrib:
                        key = f"{section.tag}/{elem.tag}"
                        source_values[key] = elem.attrib['Value']

            # Применяем изменения
            modified = False
            for section in t_tree:
                for elem in section:
                    if 'Value' in elem.attrib:
                        key = f"{section.tag}/{elem.tag}"

                        # Специальная обработка ClusterStyleColor
                        if elem.tag == "ClusterStyleColor":
                            old_val = elem.attrib['Value']
                            if old_val != "Color_AmountDelta":
                                elem.attrib['Value'] = "Color_AmountDelta"
                                modified = True
                            continue

                        # Обычные элементы
                        if key in source_values:
                            old_val = elem.attrib['Value']
                            new_val = source_values[key]
                            if old_val != new_val:
                                elem.attrib['Value'] = new_val
                                modified = True

            # Записываем изменения с сохранением BOM и CRLF
            if modified:
                # Генерируем XML содержимое
                xml_content = etree.tostring(t_tree,
                                             encoding='utf-8',
                                             xml_declaration=True,
                                             pretty_print=True)

                # Добавляем BOM если был в исходном файле
                if t_has_bom:
                    xml_content = b'\xef\xbb\xbf' + xml_content

                # Конвертируем LF в CRLF
                xml_content = xml_content.replace(b'\n', b'\r\n')

                with open(t_path, 'wb') as f:
                    f.write(xml_content)

                print(f"УСПЕХ: Файл {t_file} обновлён (UTF-8 {'с BOM' if t_has_bom else 'без BOM'}, CRLF)")
            else:
                print("ИЗМЕНЕНИЙ НЕТ: Файл уже содержит актуальные значения")

        except Exception as e:
            print(f"ОШИБКА при обработке {t_file}: {str(e)}")


if __name__ == "__main__":
    source_dir = os.path.abspath('MVS')
    target_dir = os.path.abspath('MVScopy')

    if not os.path.exists(source_dir):
        print(f"ОШИБКА: Исходная папка не существует: {source_dir}")
    elif not os.path.exists(target_dir):
        print(f"ОШИБКА: Целевая папка не существует: {target_dir}")
    else:
        print("=" * 50)
        print("XML/TMP Settings Transfer Tool")
        print("(Сохранение UTF-8 с BOM и CRLF)")
        print("=" * 50)

        transfer_settings(source_dir, target_dir)

        print("\nОбработка завершена.")