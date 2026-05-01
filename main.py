import tkinter as tk
from tkinter import ttk, messagebox
import requests
import json
import os

HISTORY_FILE = "currency_history.json"
API_URL = "https://open.er-api.com/v6/latest/" # Бесплатный пример API

# Доступные валюты
CURRENCIES = ["USD", "EUR", "RUB", "GBP", "JPY"]

history = []

# Загрузка истории
if os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, 'r') as f:
        history = json.load(f)

def save_history():
    with open(HISTORY_FILE, 'w') as f:
        json.dump(history, f)

def update_history():
    history_box.delete(0, tk.END)
    for item in reversed(history[-20:]):  # последние 20
        history_box.insert(tk.END, item)

# --- GUI ---
root = tk.Tk()
root.title("Currency Converter")

# Выбор валют
from_currency = tk.StringVar(value="USD")
to_currency = tk.StringVar(value="EUR")

tk.Label(root, text="Из:").grid(row=0, column=0)
ttk.Combobox(root, textvariable=from_currency, values=CURRENCIES).grid(row=0, column=1)

tk.Label(root, text="В:").grid(row=1, column=0)
ttk.Combobox(root, textvariable=to_currency, values=CURRENCIES).grid(row=1, column=1)

# Ввод суммы
tk.Label(root, text="Сумма:").grid(row=2, column=0)
amount_var = tk.StringVar()
tk.Entry(root, textvariable=amount_var).grid(row=2, column=1)

# Конвертация
result_var = tk.StringVar()

def convert():
    try:
        amount = float(amount_var.get())
        if amount <= 0:
            raise ValueError
    except:
        messagebox.showerror("Ошибка", "Введите положительное число!")
        return

    from_cur = from_currency.get()
    to_cur = to_currency.get()
    # Получение курсов
    try:
        r = requests.get(f"{API_URL}{from_cur}", timeout=5)
        data = r.json()
        rate = data['rates'][to_cur]
        converted = amount * rate
        result_var.set(f"{amount} {from_cur} = {converted:.2f} {to_cur}")

        # Добавить в историю
        entry = f"{amount} {from_cur} → {converted:.2f} {to_cur}"
        history.append(entry)
        update_history()
        save_history()
    except Exception as ex:
        messagebox.showerror("Ошибка", f"Не удалось получить курс:\n{ex}")

tk.Button(root, text="Конвертировать", command=convert).grid(row=3, column=0, columnspan=2)

tk.Entry(root, textvariable=result_var, width=35).grid(row=4, column=0, columnspan=2)

# История
tk.Label(root, text="История:").grid(row=5, column=0, sticky='w')
history_box = tk.Listbox(root, height=10, width=35)
history_box.grid(row=6, column=0, columnspan=2)
update_history()

root.mainloop()
