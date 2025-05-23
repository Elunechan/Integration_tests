from pydantic import BaseModel
from typing import List, Optional

"""
  Базовая реализация парсинга JSON ответа через Pydentic.
  Использовать только модели и в крайнем случае list, так как это гибко, проще масштабировать и отлавливать баги.
  """
class Element(BaseModel):
    values: List[Optional[str]]

class DictionaryValuesResponse(BaseModel):
    attributes: List[str]
    elements: List[Element]