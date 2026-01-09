"""Custom application exceptions."""


from sqlalchemy.orm.attributes import interfaces


class TomatoesException(Exception):
    """Base exception for Tomatoes application."""
    pass


class EntityNotFoundException(TomatoesException):
    """Entity not found exception."""
    
    def __init__(self, entity_name: str, entity_id: interfaces):
        self.entity_name = entity_name
        self.entity_id = entity_id
        super().__init__(f"{entity_name} with id {entity_id} not found")


class ValidationException(TomatoesException):
    """Validation exception."""
    pass


class BusinessRuleException(TomatoesException):
    """Business rule violation exception."""
    pass


class PermissionDeniedException(TomatoesException):
    """Permission denied exception."""
    pass

