from dataclasses import dataclass
from typing import final
from uuid import UUID

from travelexhibition.core.exceptions import DomainValidationError


# Constants for validation
MIN_TITLE_LENGTH = 2
MAX_TITLE_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000

# Error messages
TITLE_LENGTH_ERROR = "Name must be between 2 and 100 characters"
DESCRIPTION_LENGTH_ERROR = "Description must be at most 1000 characters"


@final
@dataclass(frozen=True, kw_only=True, slots=True)
class Artifact:
    id: UUID
    title: str
    model3d_url: str
    description: str | None = None

    def __post_init__(self) -> None:
        if len(self.title) < MIN_TITLE_LENGTH or len(self.title) > MAX_TITLE_LENGTH:
            error_msg = TITLE_LENGTH_ERROR
            raise DomainValidationError(error_msg)

        if self.description is not None and len(self.description) > MAX_DESCRIPTION_LENGTH:
            error_msg = DESCRIPTION_LENGTH_ERROR
            raise DomainValidationError(error_msg)
