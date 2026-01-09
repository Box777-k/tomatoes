# Common Components

Общие компоненты, используемые во всех модулях.

## base_controller.py

Базовый контроллер с CRUD операциями для web интерфейса.

### Использование

```python
from app.common.base_controller import BaseCRUDController
from app.modules.production.services import ProductionOrderService

class ProductionOrderController(BaseCRUDController):
    def __init__(self):
        super().__init__(
            service_class=ProductionOrderService,
            template_prefix="production",
            entity_name="order",
            entity_name_plural="orders"
        )

controller = ProductionOrderController()
```

### Методы

- `list_view()` - список всех записей
- `detail_view(item_id)` - детали записи
- `create_view()` - форма создания
- `edit_view(item_id)` - форма редактирования
- `delete_action(item_id)` - удаление записи

### Требуемая структура шаблонов

Для каждого модуля нужно создать:
- `{prefix}/{plural}_list.html` - список
- `{prefix}/{singular}_detail.html` - детали
- `{prefix}/{singular}_form.html` - форма создания/редактирования

Все шаблоны должны наследоваться от `base.html`.

