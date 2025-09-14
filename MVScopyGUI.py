import os
from lxml import etree
import tkinter as tk
from tkinter import filedialog, messagebox
import ttkbootstrap as ttk
from ttkbootstrap.constants import *

    # https://github.com/IzhMechanics/MVScopyCScalp

def transfer_settings():
    source_dir = source_dir_entry.get()
    target_dir = target_dir_entry.get()

    if not source_dir or not target_dir:
        messagebox.showerror("Ошибка", "Укажите обе папки!")
        return

    confirm = messagebox.askyesno(
        "Подтверждение",
        "Вы уверены, что хотите перенести настройки?\n\nПеред использованием сохраните резервные копии файлов!"
    )
    if not confirm:
        return

    try:
        # Получаем списки файлов
        source_files = [f for f in os.listdir(source_dir) if f.lower().endswith(('.tmp', '.xml'))]
        target_files = [f for f in os.listdir(target_dir) if f.lower().endswith(('.tmp', '.xml'))]

        # Сопоставляем файлы по базовому имени
        file_pairs = []
        for t_file in target_files:
            t_base = os.path.splitext(t_file)[0]
            for s_file in source_files:
                if os.path.splitext(s_file)[0] == t_base:
                    file_pairs.append((s_file, t_file))
                    break

        if not file_pairs:
            messagebox.showwarning("Предупреждение", "Нет парных файлов для обработки!")
            return

        updated_files = 0

        for s_file, t_file in file_pairs:
            try:
                # Читаем исходный файл
                s_path = os.path.join(source_dir, s_file)
                with open(s_path, 'rb') as f:
                    s_content = f.read()
                    has_bom = s_content.startswith(b'\xef\xbb\xbf')
                    s_content = s_content.decode('utf-8-sig')

                s_tree = etree.fromstring(s_content.encode('utf-8'))

                # Читаем целевой файл
                t_path = os.path.join(target_dir, t_file)
                with open(t_path, 'rb') as f:
                    t_content = f.read()
                    t_has_bom = t_content.startswith(b'\xef\xbb\xbf')
                    t_content = t_content.decode('utf-8-sig')

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

                            if elem.tag == "ClusterStyleColor":
                                if elem.attrib['Value'] != "Color_AmountDelta":
                                    elem.attrib['Value'] = "Color_AmountDelta"
                                    modified = True
                                continue

                            if elem.tag == "RulerDataType":
                                if elem.attrib['Value'] != "3":
                                    elem.attrib['Value'] = "3"
                                    modified = True
                                continue

                            if elem.tag == "ShowProfitType":
                                if elem.attrib['Value'] != "4":
                                    elem.attrib['Value'] = "4"
                                    modified = True
                                continue

                            if key in source_values:
                                if elem.attrib['Value'] != source_values[key]:
                                    elem.attrib['Value'] = source_values[key]
                                    modified = True

                # Сохраняем изменения
                if modified:
                    xml_content = etree.tostring(t_tree, encoding='utf-8', xml_declaration=True, pretty_print=True)

                    # Убираем лишний перевод строки в конце
                    if xml_content.endswith(b'\n'):
                        xml_content = xml_content[:-1]

                    if t_has_bom:
                        xml_content = b'\xef\xbb\xbf' + xml_content
                    xml_content = xml_content.replace(b'\n', b'\r\n')

                    with open(t_path, 'wb') as f:
                        f.write(xml_content)

                    updated_files += 1

            except Exception as e:
                messagebox.showerror(
                    "Ошибка обработки файла",
                    f"Ошибка при обработке {t_file}:\n{str(e)}"
                )
                return

        messagebox.showinfo(
            "Готово",
            f"Настройки успешно перенесены!\n\n"
            f"Статистика обработки:\n"
            f"- Всего найденных пар файлов: {len(file_pairs)}\n"
            f"- Успешно обновлено: {updated_files}\n"
            f"\n"  # пустая строка
            f"Общее количество файлов:\n"
            f"- Исходных: {len(source_files)}\n"
            f"- Целевых: {len(target_files)}"
        )

    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{str(e)}")

def browse_source():
    dir_path = filedialog.askdirectory(title="Выберите исходную папку")
    if dir_path:
        source_dir_entry.delete(0, tk.END)
        source_dir_entry.insert(0, dir_path)


def browse_target():
    dir_path = filedialog.askdirectory(title="Выберите целевую папку")
    if dir_path:
        target_dir_entry.delete(0, tk.END)
        target_dir_entry.insert(0, dir_path)

    # Копирует текст в буфер обмена
def copy_to_clipboard(address, label):
    try:
        # Создаем временное скрытое текстовое поле
        temp_text = tk.Text(root, height=1)
        temp_text.insert('1.0', address)
        temp_text.tag_add('sel', '1.0', 'end-1c')
        temp_text.event_generate('<<Copy>>')
        temp_text.destroy()

        # Обновляем статус
        label.config(text="✓ Скопировано!")
        root.after(2000, lambda: label.config(text=address))  # Через 2 секунды вернуть адрес
    except Exception as e:
        label.config(text="X Ошибка копирования")

# Создаем GUI
root = ttk.Window(themename="darkly")
root.title("Перенос настроек MVS")
root.geometry("615x417")

# Фрейм для основного содержимого
main_frame = ttk.Frame(root, padding=20)
main_frame.pack(fill=tk.BOTH, expand=True)

# Заголовок
ttk.Label(
    main_frame,
    text="Перенос настроек между конфигурациями MVS",
    font=('Helvetica', 14, 'bold')
).pack(pady=(0, 15))

# Поле для исходной папки
source_frame = ttk.Frame(main_frame)
source_frame.pack(fill=tk.X, pady=5)

ttk.Label(source_frame, text="Исходная папка:", width=15).pack(side=tk.LEFT)
source_dir_entry = ttk.Entry(source_frame)
source_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Button(
    source_frame,
    text="Обзор",
    command=browse_source,
    bootstyle=INFO
).pack(side=tk.LEFT)

# Поле для целевой папки
target_frame = ttk.Frame(main_frame)
target_frame.pack(fill=tk.X, pady=5)

ttk.Label(target_frame, text="Целевая папка:", width=15).pack(side=tk.LEFT)
target_dir_entry = ttk.Entry(target_frame)
target_dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
ttk.Button(
    target_frame,
    text="Обзор",
    command=browse_target,
    bootstyle=INFO
).pack(side=tk.LEFT)

# Кнопка переноса
transfer_btn = ttk.Button(
    main_frame,
    text="Перенести настройки",
    command=transfer_settings,
    bootstyle=SUCCESS,
    width=20
)
transfer_btn.pack(pady=20)

# Информационное сообщение
ttk.Label(
    main_frame,
    text="Перед переносом рекомендуется создать резервные копии файлов!",
    font=('Helvetica', 9),
    foreground="lightgray"
).pack(pady=(0, 10))

# Разделитель
separator = ttk.Separator(main_frame, orient='horizontal')
separator.pack(fill=tk.X, pady=1)

# Фрейм для крипто-кошельков
crypto_frame = ttk.Frame(main_frame)
crypto_frame.pack(fill=tk.X, pady=5, padx=4)

ttk.Label(
    crypto_frame,
    text="Поддержка разработчика",
    font=('Helvetica', 9),
    foreground="lightgray"
).pack(pady=(5, 5))

# Список крипто-кошельков
wallets = [
    {"name": "BSC (BEP20)", "address": "0xddcbe9f84e455fb920a5ba63b4ff023ffe7f9f72"},
    {"name": "TON", "address": "UQB9ox7Lx85ewqlMkD52qOjsfM-s03frtPBXzrzkgbX_nyn5"},
    {"name": "APTOS", "address": "0xfa91c8dd813a43be92117565fe49d0cde224882304d85d53469a31665b284436"},
    {"name": "TRON (TRC20)", "address": "TBJz8hVW9s4oMdiPqadY7GoB4uDFH4QGSV"}
]

for wallet in wallets:
    wallet_frame = ttk.Frame(crypto_frame)
    wallet_frame.pack(fill=tk.X, pady=3)

    # Название кошелька
    ttk.Label(
        wallet_frame,
        text=f"{wallet['name']}:",
        width=14,
        font=('Helvetica', 8)
    ).pack(side=tk.LEFT)

    # Фрейм для адреса и кнопки
    address_frame = ttk.Frame(wallet_frame)
    address_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=3)

    # Адрес кошелька (полный)
    address_label = ttk.Label(
        address_frame,
        text=wallet['address'],
        font=('Helvetica', 9),
        foreground="lightblue",
        cursor="hand2",
        relief="flat",
        padding=(5, 2)
    )
    address_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
    address_label.bind("<Button-1>", lambda e, addr=wallet['address'], lbl=address_label: copy_to_clipboard(addr, lbl))

    # Подсказка при наведении
    def create_tooltip(widget, text):
        def show_tooltip(event):
            tooltip = tk.Toplevel(widget)
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root + 5}+{event.y_root - 20}")
            label = ttk.Label(tooltip, text=text, background="yellow", foreground="black", padding=2)
            label.pack()
            widget.tooltip = tooltip

        def hide_tooltip(event):
            if hasattr(widget, 'tooltip'):
                widget.tooltip.destroy()

        widget.bind("<Enter>", show_tooltip)
        widget.bind("<Leave>", hide_tooltip)

    create_tooltip(address_label, "Кликните для копирования")

root.mainloop()
