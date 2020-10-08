from dataclasses import dataclass, field
from datetime import date

from nova_api.entity import Entity


@dataclass
class User(Entity):
    name: str = field(default="Anom")
    email: str = None
    birthday: date = field(default=None, metadata={"date_format": "%d/%m/%Y"})
