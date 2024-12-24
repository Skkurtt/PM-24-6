import csv
import pickle
import datetime

def load_table_csv(file_path):
    """Загружает таблицу из CSV-файла"""
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            table = [row for row in reader]
        return table
    except FileNotFoundError:
        raise FileNotFoundError(f'Ошибка: файл {file_path} не найден.')
    except PermissionError:
        raise PermissionError(f'Ошибка: нет доступа к файлу {file_path}.')
    except csv.Error as e:
        raise csv.Error(f'Ошибка при чтении CSV файла: {e}')

def save_table_csv(file_path, table):
    """Сохраняет таблицу в CSV-файл"""
    try:
        with open(file_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(table)
    except PermissionError:
        raise PermissionError(f'Ошибка: нет доступа для записи в файл {file_path}.')
    except Exception as e:
        raise Exception(f'Неизвестная ошибка при сохранении CSV файла: {e}')

def load_table_pickle(file_path):
    """Загружает таблицу из Pickle-файла"""
    try:
        with open(file_path, mode='rb') as file:
            table = pickle.load(file)
        return table
    except FileNotFoundError:
        raise FileNotFoundError(f'Ошибка: файл {file_path} не найден.')
    except PermissionError:
        raise PermissionError(f'Ошибка: нет доступа к файлу {file_path}.')
    except pickle.UnpicklingError:
        raise pickle.UnpicklingError(f'Ошибка при десериализации Pickle файла.')

def save_table_pickle(file_path, table):
    """Сохраняет таблицу в Pickle-файл"""
    try:
        with open(file_path, mode='wb') as file:
            pickle.dump(table, file)
    except PermissionError:
        raise PermissionError(f'Ошибка: нет доступа для записи в файл {file_path}.')
    except Exception as e:
        raise Exception(f'Неизвестная ошибка при сохранении Pickle файла: {e}')

def save_table_txt(file_path, table):
    """Сохраняет таблицу в текстовый файл"""
    try:
        with open(file_path, mode='w', encoding='utf-8') as file:
            for row in table:
                file.write(' | '.join(map(str, row)) + '\n')
    except PermissionError:
        raise PermissionError(f'Ошибка: нет доступа к файлу {file_path}.')
    except Exception as e:
        raise Exception(f'Неизвестная ошибка при сохранении текстового файла: {e}')

def get_rows_by_number(table, start, stop=None, copy_table=False):
    """Возвращает строки таблицы по номеру"""
    if stop is None:
        rows = [table[start]]
    else:
        rows = table[start:stop]
    if copy_table:
        rows = [row.copy() for row in rows]
    return rows

def get_rows_by_index(table, *vals, copy_table=False):
    """Возвращает строки таблицы по значениям первого столбца"""
    rows = [row for row in table if row[0] in vals]
    if copy_table:
        rows = [row.copy() for row in rows]
    return rows

def get_column_types(table, by_number=True):
    """Определяет типы столбцов таблицы"""
    types = {}
    for col_index in range(len(table[0])):
        col_values = [row[col_index] for row in table[1:]]
        if all(isinstance(val, int) for val in col_values if val is not None):
            col_type = int
        elif all(isinstance(val, float) for val in col_values if val is not None):
            col_type = float
        elif all(isinstance(val, bool) for val in col_values if val is not None):
            col_type = bool
        elif all(is_valid_date(val) for val in col_values if val is not None):
            col_type = datetime.datetime
        else:
            col_type = str
        key = col_index if by_number else table[0][col_index]
        types[key] = col_type
    return types

def is_valid_date(value):
    """Определяет тип datetime"""
    try:
        datetime.datetime.strptime(value, '%Y-%m-%d')
        return True
    except ValueError:
        return False
    
def set_column_types(table, types_dict, by_number=True):
    """Устанавливает типы столбцов таблицы"""
    for col_key, col_type in types_dict.items():
        if by_number:
            col_index = col_key
        else:
            col_index = table[0].index(col_key)
        for i in range(1, len(table)):
            try:
                table[i][col_index] = col_type(table[i][col_index])
            except ValueError:
                raise ValueError(f'Ошибка преобразования значения в строке {i} и столбце {col_key}.')

def get_values(table, column=0):
    """Возвращает значения указанного столбца таблицы"""
    if isinstance(column, str):
        column_index = table[0].index(column)
    else:
        column_index = column
    return [row[column_index] for row in table[1:]]

def get_value(table, column=0):
    """Возвращает значение ячейки таблицы из первой строки данных"""
    if len(table) <= 1:
        raise ValueError('Таблица не содержит данных.')
    if isinstance(column, str):
        column_index = table[0].index(column)
    else:
        column_index = column
    return table[1][column_index]

def set_values(table, values, column=0):
    """Устанавливает значения для указанного столбца таблицы"""
    if isinstance(column, str):
        column_index = table[0].index(column)
    else:
        column_index = column
    if len(values) != len(table) - 1:
        raise ValueError('Количество значений не соответствует количеству строк в таблице.')
    for i in range(1, len(table)):
        table[i][column_index] = values[i - 1]

def set_value(table, value, column=0):
    """Устанавливает значение в ячейку таблицы из первой строки данных"""
    if isinstance(column, str):
        column_index = table[0].index(column)
    else:
        column_index = column
    if len(table) <= 1:
        raise ValueError('Таблица не содержит данных.')
    table[1][column_index] = value

def print_table(table):
    """Печатает таблицу"""
    if not table:
        print('Таблица пуста')
        return
    col_widths = [max(len(str(item)) for item in col) for col in zip(*table)]
    for row in table:
        print(' | '.join(str(val).ljust(width) for val, width in zip(row, col_widths)))

def load_table(*file_paths, infer_types=False):
    tables = []

    for file_path in file_paths:
        try:
            if file_path.endswith('.csv'):
                with open(file_path, mode='r', newline='', encoding='utf-8') as file:
                    reader = csv.reader(file)
                    table = [row for row in reader]
            elif file_path.endswith('.pkl'):
                with open(file_path, mode='rb') as file:
                    table = pickle.load(file)
            else:
                raise ValueError(f"Неподдерживаемый формат файла: {file_path}")

            tables.append(table)
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")
        except Exception as e:
            raise ValueError(f"Ошибка при загрузке файла {file_path}: {e}")

    if not tables:
        raise ValueError("Не удалось загрузить ни одной таблицы.")

    headers = tables[0][0]
    for table in tables:
        if table[0] != headers:
            raise ValueError("Структура заголовков файлов не совпадает.")

    combined_table = tables[0]
    for table in tables[1:]:
        combined_table.extend(table[1:])

    if infer_types:
        types_dict = get_column_types(combined_table, by_number=False)
        set_column_types(combined_table, types_dict, by_number=False)
        print("Определенные типы столбцов:", types_dict)

    return combined_table

def save_table(table, base_file_path, max_rows):
    if not base_file_path.endswith(('.csv', '.pkl')):
        raise ValueError("Формат файла должен быть .csv или .pkl")

    file_format = 'csv' if base_file_path.endswith('.csv') else 'pkl'
    base_name = base_file_path.rsplit('.', 1)[0]

    for i in range(0, len(table), max_rows):
        chunk = table[i:i + max_rows]
        file_name = f"{base_name}_part{i // max_rows + 1}.{file_format}"

        if file_format == 'csv':
            with open(file_name, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerows(chunk)
        elif file_format == 'pkl':
            with open(file_name, mode='wb') as file:
                pickle.dump(chunk, file)

        print(f"Сохранено: {file_name}")

def concat(table1, table2):
    if table1[0] != table2[0]:
        raise ValueError("Заголовки таблиц не совпадают")
    return table1 + table2[1:]

def split(table, row_number):
    if row_number < 1 or row_number >= len(table):
        raise ValueError("Неверный номер строки для разделения")
    return table[:row_number], table[row_number:]

def add_columns(table, column1, column2, result_column):
    if result_column in table[0]:
        raise ValueError(f"Столбец '{result_column}' уже существует в таблице.")

    if column1 not in table[0] or column2 not in table[0]:
        raise ValueError("Один или оба указанных столбца отсутствуют в таблице.")

    col1_index = table[0].index(column1)
    col2_index = table[0].index(column2)

    table[0].append(result_column)

    for row in table[1:]:
        val1 = row[col1_index]
        val2 = row[col2_index]

        if not isinstance(val1, (int, float, bool)) or not isinstance(val2, (int, float, bool)):
            raise ValueError("Оба столбца должны содержать числовые или логические значения.")

        row.append(val1 + val2)

def subtract_columns(table, column1, column2, result_column):
    if result_column in table[0]:
        raise ValueError(f"Столбец '{result_column}' уже существует в таблице.")

    if column1 not in table[0] or column2 not in table[0]:
        raise ValueError("Один или оба указанных столбца отсутствуют в таблице.")

    col1_index = table[0].index(column1)
    col2_index = table[0].index(column2)

    table[0].append(result_column)

    for row in table[1:]:
        val1 = row[col1_index]
        val2 = row[col2_index]

        if not isinstance(val1, (int, float, bool)) or not isinstance(val2, (int, float, bool)):
            raise ValueError("Оба столбца должны содержать числовые или логические значения.")

        row.append(val1 - val2)

def multiply_columns(table, column1, column2, result_column):
    if result_column in table[0]:
        raise ValueError(f"Столбец '{result_column}' уже существует в таблице.")

    if column1 not in table[0] or column2 not in table[0]:
        raise ValueError("Один или оба указанных столбца отсутствуют в таблице.")

    col1_index = table[0].index(column1)
    col2_index = table[0].index(column2)

    table[0].append(result_column)

    for row in table[1:]:
        val1 = row[col1_index]
        val2 = row[col2_index]

        if not isinstance(val1, (int, float, bool)) or not isinstance(val2, (int, float, bool)):
            raise ValueError("Оба столбца должны содержать числовые или логические значения.")

        row.append(val1 * val2)

def divide_columns(table, column1, column2, result_column):
    if result_column in table[0]:
        raise ValueError(f"Столбец '{result_column}' уже существует в таблице.")

    if column1 not in table[0] or column2 not in table[0]:
        raise ValueError("Один или оба указанных столбца отсутствуют в таблице.")

    col1_index = table[0].index(column1)
    col2_index = table[0].index(column2)

    table[0].append(result_column)

    for row in table[1:]:
        val1 = row[col1_index]
        val2 = row[col2_index]

        if not isinstance(val1, (int, float, bool)) or not isinstance(val2, (int, float, bool)):
            raise ValueError("Оба столбца должны содержать числовые или логические значения.")

        if val2 == 0:
            raise ZeroDivisionError("Деление на ноль невозможно.")

        row.append(val1 / val2)

def main():
    print('Задание 1.1: Сохранение и загрузка таблицы в CSV')
    table = [
        ['ID', 'Name', 'Age'],
        [1, 'Alice', 30],
        [2, 'Bob', 25],
        [3, 'Charlie', 35]
    ]
    save_table_csv('table.csv', table)
    loaded_csv = load_table_csv('table.csv')
    print('Loaded CSV:')
    print_table(loaded_csv)

    print('\nЗадание 1.2: Сохранение и загрузка таблицы через Pickle')
    save_table_pickle('table.pkl', table)
    loaded_pickle = load_table_pickle('table.pkl')
    print('Loaded Pickle:')
    print_table(loaded_pickle)

    print('\nЗадание 1.3: Сохранение таблицы в текстовый файл')
    save_table_txt('table.txt', table)
    print('Saved to TXT')

    print('\nЗадание 2.1: Получение строк по номеру')
    rows_by_number = get_rows_by_number(table, 1, 3)
    print_table(rows_by_number)

    print('\nЗадание 2.2: Получение строк по индексу значений')
    new_rows = get_rows_by_index(table, 1, 2)
    print('Rows by Index:')
    print_table(new_rows)

    print('\nЗадание 2.3: Определение типов столбцов')
    print('Column Types:')
    print(get_column_types(table))

    print('\nЗадание 2.4: Установка типов столбцов')
    set_column_types(table, {2: str}, by_number=True)
    print('Updated Column Types:')
    print(get_column_types(table))

    print('\nЗадание 2.5: Получение значений из столбца')
    column_values = get_values(table, 'Age')
    print(column_values)

    print('\nЗадание 2.6: Получение значения из первой строки')
    single_value = get_value(table, 'Name')
    print(single_value)

    print('\nЗадание 2.7: Установка значений для столбца')
    set_values(table, [40, 45, 50], 'Age')
    print_table(table)

    print('\nЗадание 2.8: Установка значения для ячейки')
    set_value(table, 'Eve', 'Name')
    print_table(table)

    print('\nЗадание 3.1: Загрузка таблицы из нескольких файлов')
    table2 = [
        ['ID', 'Name', 'Age'],
        [4, 'David', 40],
        [5, 'Eve', 45]
    ]
    save_table_csv('table1.csv', table)
    save_table_pickle('table2.pkl', table2)
    loaded_table = load_table('table1.csv', 'table2.pkl')
    print_table(loaded_table)

    print('\nЗадание 3.2: Загрузка таблицы из нескольких файлов')
    table = [
        ['ID', 'Name', 'Age'],
        [1, 'Alice', 30],
        [2, 'Bob', 25]
    ]
    table2 = [
        ['ID', 'Name', 'Age'],
        [3, 'Charlie', 35],
        [4, 'David', 40]
    ]
    save_table(table, 'table1.csv', max_rows=1)
    save_table(table2, 'table2.pkl', max_rows=3)

    loaded_table = load_table('table1.csv', 'table2.pkl')
    print_table(loaded_table)

    print('\nЗадание 3.3: Конкатенация и разделение таблиц')
    concatenated_table = concat(table, table2)
    print("Конкатенация таблиц:")
    print_table(concatenated_table)

    part1, part2 = split(concatenated_table, 3)
    print("Часть 1 после разделения:")
    print_table(part1)
    print("Часть 2 после разделения:")
    print_table(part2)

    print('\nЗадание 3.4: Автоматическое определение типов столбцов')
    loaded_table_with_types = load_table('table1.csv', 'table2.pkl', infer_types=True)
    print_table(loaded_table_with_types)

    print('\nЗадание 3.5: Определение типов столбцов с поддержкой datetime')
    table = [
        ['ID', 'Name', 'Date'],
        [1, 'Alice', '2023-12-01'],
        [2, 'Bob', '2023-11-30']
    ]
    column_types = get_column_types(table, by_number=False)
    print("Определенные типы столбцов:", column_types)

    print('\nЗадание 3.6: Арифметические операции над столбцами')
    table = [
        ['ID', 'Value1', 'Value2'],
        [1, 10, 2],
        [2, 20, 4],
        [3, 30, 6]
    ]

    add_columns(table, 'Value1', 'Value2', 'Сумма')
    print("3.6.1: Таблица после сложения столбцов:")
    print_table(table)

    subtract_columns(table, 'Value1', 'Value2', 'Разность')
    print("\n3.6.2: Таблица после вычитания столбцов:")
    print_table(table)

    multiply_columns(table, 'Value1', 'Value2', 'Произведение')
    print("\n3.6.3: Таблица после умножения столбцов:")
    print_table(table)

    divide_columns(table, 'Value1', 'Value2', 'Частное')
    print("\n3.6.4: Таблица после деления столбцов:")
    print_table(table)

if __name__ == '__main__':
    main()
