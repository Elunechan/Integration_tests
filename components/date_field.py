class DateField:
    def __init__(self, page, label_text: str):
        # Найти div-обёртку с нужным label
        self.wrapper = page.locator(
            f'//div[contains(@class,"trv-wrapper")][.//label[contains(normalize-space(.), "{label_text}")]]'
        )
        # Найти input внутри этой обёртки
        self.input = self.wrapper.locator('input.trv-datetime__input:not(.trv-datetime__input-hidden)')

    def fill(self, value: str):
        self.input.fill(value)

    def clear(self):
        self.input.fill('')

    def get_value(self):
        return self.input.input_value()