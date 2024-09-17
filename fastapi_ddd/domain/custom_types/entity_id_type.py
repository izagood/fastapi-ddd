from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.types import TypeDecorator

from fastapi_ddd.common.exception.custom_exceptions import DatabaseException
from fastapi_ddd.domain.entity import EntityId


class EntityIdType(TypeDecorator):
    impl = UUID

    def process_bind_param(self, value: UUID, dialect):
        """Convert the value: UUID to a string."""
        return str(value)

    def process_result_value(self, value: UUID, dialect):
        """Convert the value: UUID to a EntityId."""
        return EntityId(value)

    def load_dialect_impl(self, dialect):
        """Return a TypeEngine with a dialect-specific implementation."""
        if dialect.name == "postgresql":
            return dialect.type_descriptor(UUID(as_uuid=True))

        raise DatabaseException("Unsupported dialect: {dialect.name}")
