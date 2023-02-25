from .models import (
                    groups,
                    users,
                    # users_groups,
                    categories,
                    homeworks,
                    )
from .base import metadata, engine


metadata.create_all(bind=engine)