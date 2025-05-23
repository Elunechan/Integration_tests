class LabeledDropdown:
    def __init__(self, page, label_text: str):
        self.page = page
        self.label_text = label_text
        self.wrapper = page.locator(
            f"div.trv-wrapper:has(label span:has-text('{label_text}'))"
        )
        self.dropdown = self.wrapper.locator("a.selector-parameters-item__value") # Находим нужный нам фильтр по его label

    def open(self):
        self.dropdown.click()
        popup = self.page.locator("div.selector-parameters.-form-tree-combo[style*='height']").first
        popup.wait_for(state="visible")
        popup.locator("div.text").first.wait_for(state="visible") # Дожидаемся загрузки хотя бы одного элемента выпадающего списка

    def select_value(self, value: str):
        # Данная функция принимает в себя значение value из теста и находит его в выпадающем списке, если не находит, выкидываетс сообщение
        popup = self.page.locator("div.selector-parameters.-form-tree-combo[style*='height']").first
        options = popup.locator(
            f"div.selector-parameters-item__item:has(div.text:has-text('{value.strip()}'))"
        )
        if options.count() == 0:
            raise Exception(f"Значение '{value}' не найдено в фильтре")
        options.first.scroll_into_view_if_needed()
        options.first.click()
        self.page.locator("body").click()