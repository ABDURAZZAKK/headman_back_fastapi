from .models import (
    groups,
    users,
    studstat_accs,
    categories,
    homeworks,
)
from .base import metadata, engine


metadata.create_all(bind=engine)
