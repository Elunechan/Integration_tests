from pydantic import BaseModel, ValidationError

def parse_response(response, model: type[BaseModel]):
    """
    Универсальная функция для парсинга ответа через pydantic-модель.
    Выдает assert с красивым сообщением при ошибке валидации.
    """
    try:
        return model.model_validate(response.json())
    except ValidationError as e:
        assert False, f"Ошибка валидации ответа {model.name}: {e}"