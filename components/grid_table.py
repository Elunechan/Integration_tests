import time


class GridTable:
    def __init__(self, page, root_selector="div.ag-center-cols-container"):
        self.page = page
        self.root = page.locator(root_selector)
        self.rows = self.root.locator("div[role='row']")

    def wait_loader_disappear(self, timeout=15000):
        # Ожидаем исчезновения всех лоадеров на странице
        time.sleep(2) # Переделать в будущем на ожидание загрузки страницы через поиск всех лоадеров
        self.page.wait_for_function(
            """
            () => {
                // Находим все видимые лоадеры
                const loaders = Array.from(document.querySelectorAll('div.loader__spiner.spinner-border'));
                return loaders.every(l => l.offsetParent === null);
            }
            """,
            timeout=timeout
        )
        # Дожидаемся хотя бы одной строки (если таблица не пуста)
        try:
            self.rows.first.wait_for(state="visible", timeout=3000)
        except Exception:
            # Если строк нет — значит таблица пуста, для некоторых кейсов возможно
            pass

    def row_count(self):
        return self.rows.count()

    def get_row(self, row_idx):
        return self.rows.nth(row_idx)

    def get_cell(self, row_idx, col_id):
        row = self.get_row(row_idx)
        return row.locator(f"div.ag-cell[col-id='{col_id}'] div.cellDiv")

    def get_column_values(self, col_id):
        values = []
        for i in range(self.row_count()):
            cell = self.get_cell(i, col_id)
            val = cell.get_attribute("title")
            if val:
                values.append(val.strip())
            else:
                values.append((cell.text_content() or "").strip())
        return values

    def assert_column_values(self, col_id, expected_value, match_mode="exact"):
        """
        Проверить, что ВСЕ значения столбца равны expected_value.
        match_mode: "exact" — строгое совпадение (по умолчанию)
                    "startswith" — значение должно начинаться с expected_value
                    "contains" — expected_value должен входить в значение
        """
        # Вроде норм
        values = self.get_column_values(col_id)
        assert values, f"Нет значений в столбце '{col_id}'"
        for idx, val in enumerate(values):
            if match_mode == "exact":
                assert val == expected_value, f"Ожидал '{expected_value}', но получил '{val}' (строка {idx+1})"
            elif match_mode == "startswith":
                assert val.startswith(expected_value), f"Ожидал, что '{val}' начинается с '{expected_value}' (строка {idx+1})"
            elif match_mode == "contains":
                assert expected_value in val, f"Ожидал, что '{val}' содержит '{expected_value}' (строка {idx+1})"
            else:
                raise ValueError(f"Неизвестный режим сравнения: {match_mode}")

    def assert_row_contains(self, expected_row: list):
        all_data = self.get_all_data()
        assert expected_row in all_data, f"Нет такой строки: {expected_row}\nТекущие строки: {all_data}"

    def get_all_data(self):
        all_rows = []
        row_count = self.row_count()
        for i in range(row_count):
            row = self.get_row(i)
            cells = row.locator("div.ag-cell div.cellDiv")
            row_data = []
            for j in range(cells.count()):
                val = cells.nth(j).get_attribute("title")
                if val:
                    row_data.append(val.strip())
                else:
                    row_data.append((cells.nth(j).text_content() or "").strip())
            all_rows.append(row_data)
        return all_rows