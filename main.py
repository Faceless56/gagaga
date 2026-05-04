import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import random
import string

HISTORY_FILE = 'history.json'

def load_history():
    if os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'r') as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return []
    return []

def save_history(history):
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f, indent=4)

def generate_password():
    length = password_length.get()
    if not (4 <= length <= 64):
        messagebox.showerror("Ошибка", "Длина должна быть от 4 до 64 символов.")
        return
    
    chars = ''
    if var_numbers.get():
        chars += string.digits
    if var_letters.get():
        chars += string.ascii_letters
    if var_symbols.get():
        chars += string.punctuation
    
    if not chars:
        messagebox.showerror("Ошибка", "Выберите хотя бы один тип символов.")
        return
    
    password = ''.join(random.choice(chars) for _ in range(length))
    password_var.set(password)

    # обновляем историю
    global history
    if len(history) >= 1000:
        history = history[-999:]
    history.append({'password': password})
    save_history(history)
    update_history_table()

def update_history_table():
    for row in tree.get_children():
        tree.delete(row)
    for item in history[-10:]:
        tree.insert('', 'end', values=(item['password'],))

def copy_password():
    pwd = password_var.get()
    if not pwd:
        return
    root.clipboard_clear()
    root.clipboard_append(pwd)
    messagebox.showinfo("Ок", "Пароль скопирован в буфер обмена.")

# Загружаем историю
history = load_history()

root = tk.Tk()
root.title("Генератор паролей")

# Размер пароля
ttk.Label(root, text="Длина пароля:").grid(row=0, column=0, padx=5, pady=5, sticky='w')
password_length = tk.IntVar(value=12)
length_spinbox = ttk.Spinbox(root, from_=4, to=64, textvariable=password_length, width=5)
length_spinbox.grid(row=0, column=1, padx=5, pady=5, sticky='w')

# Чекбоксы для символов
var_numbers = tk.BooleanVar(value=True)
var_letters = tk.BooleanVar(value=True)
var_symbols = tk.BooleanVar(value=False)

ttk.Checkbutton(root, text="Цифры", variable=var_numbers).grid(row=1, column=0, sticky='w', padx=5)
ttk.Checkbutton(root, text="Буквы", variable=var_letters).grid(row=1, column=1, sticky='w', padx=5)
ttk.Checkbutton(root, text="Символы", variable=var_symbols).grid(row=1, column=2, sticky='w', padx=5)

# Кнопка для генерации
ttk.Button(root, text="Генерировать", command=generate_password).grid(row=2, column=0, columnspan=3, pady=10)

# Поле для вывода пароля
ttk.Label(root, text="Пароль:").grid(row=3, column=0, padx=5, pady=5, sticky='w')
password_var = tk.StringVar()
password_entry = ttk.Entry(root, textvariable=password_var, width=40, font=('Arial', 12))
password_entry.grid(row=3, column=1, columnspan=2, padx=5, pady=5)

# Кнопка копировать
ttk.Button(root, text="Копировать", command=copy_password).grid(row=4, column=0, columnspan=3, pady=5)

# История
ttk.Label(root, text="История (последние 10):").grid(row=5, column=0, padx=5, pady=5, sticky='w')
columns = ('Пароль',)
tree = ttk.Treeview(root, columns=columns, show='headings', height=10)
tree.heading('Пароль', text='Пароль')
tree.grid(row=6, column=0, columnspan=3, padx=5, pady=5)

# Обновляем историю при запуске
update_history_table()

root.mainloop()
