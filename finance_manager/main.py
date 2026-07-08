import json

class Transaction:
    def __init__(self, amount, category, type, date, description=''):
        self.amount = amount
        self.category = category
        if type.lower()=='доход' or type.lower()=='расход':
            self.type = type[0].upper() + type.lower()[1:]
        else:
            raise ValueError
        self.description = description
        self.date = date
    def __str__(self):
        return (f'{self.type} на сумму {self.amount}$\n'
                f'Категория: {self.category}\n'
                f'Дата: {self.date}\n'
                f'Описание: {(self.description if self.description!='' else 'Нет')}')
    def to_dict(self):
        return {
            'amount': self.amount,
            'category': self.category,
            'type': self.type,
            'date': self.date,
            'description': self.description
        }

class FinanceManager:
    def __init__(self):
        self.transactions = []
    def add_transaction(self, amount, category, type, date, description=''):
        self.transactions.append(Transaction(amount, category, type, date, description))
        print('Транзакция сохранена')
    def delete_transaction(self, index):
        if 0 < index <= len(self.transactions):
            self.transactions.pop(index-1)
            print('Транзакция удалена')
        else:
            print('Некорректный номер')
    def list_transactions(self):
        for index, transaction in enumerate(self.transactions):
            print(f'\n{index+1})\n{transaction}')
    def get_balance(self):
        income = 0
        expenses = 0
        for transaction in self.transactions:
            if transaction.type == 'Доход':
                income += transaction.amount
            elif transaction.type == 'Расход':
                expenses += transaction.amount
        return f'{income - expenses}$'
    def filter_by_category(self, category):
        filtered = []
        for transaction in self.transactions:
            if transaction.category.lower() == category.lower():
                filtered.append(transaction)
        if len(filtered)==0:
            print('Ничего не найдено')
        else:
            for index, transaction in enumerate(filtered):
                print(f'\n{index + 1})\n{transaction}')

    def save_to_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([t.to_dict() for t in self.transactions], f, ensure_ascii=False, indent=2)
        print('Файл успешно сохранён')
    def load_from_file(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            self.transactions = []
            for item in data:
                t = Transaction(
                    amount=item['amount'],
                    category=item['category'],
                    type=item['type'],
                    description=item['description'],
                    date=item['date']
                )
                self.transactions.append(t)
            print('Файл успешно загружен')
        except FileNotFoundError:
            print('Файл не найден')
        except json.decoder.JSONDecodeError:
            print('Ошибка формата файла')
finance_manager = FinanceManager()
while True:
    print()
    print(f'Ваш баланс: {finance_manager.get_balance()}')
    print("""
1. Добавить транзакцию
2. Удалить транзакцию
3. Показать все транзакции
4. Фильтр по категории
5. Сохранить в файл
6. Загрузить из файла
0. Выход
    """)
    command = input('>> ').strip()
    if command == '0':
        break
    elif command == '1':
        while True:
            type = input('Расход/Доход: ')
            if type.lower()=='расход' or type.lower()=='доход':
                break
            else:
                print('Некорректный ввод')
        while True:
            try:
                amount = float(input('Сумма: '))
                break
            except ValueError:
                print('Некорректный ввод')
        category = input('Категория: ')
        description = input('Описание: ')
        date = input('Дата: ')
        finance_manager.add_transaction(amount, category, type, date, description)
    elif command == '2':
        try:
            finance_manager.delete_transaction(int(input('Введите номер транзакции: ')))
        except ValueError:
            print('Некорректный ввод')
    elif command == '3':
        finance_manager.list_transactions()
    elif command == '4':
        finance_manager.filter_by_category(input('Введите категорию: '))
    elif command == '5':
        finance_manager.save_to_file(input('Введите файл: '))
    elif command == '6':
        finance_manager.load_from_file(input('Введите файл: '))


