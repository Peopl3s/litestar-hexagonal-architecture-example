import logging
from dataclasses import dataclass
from typing import final

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from travelexhibition.adapters.secondary.exceptions import DataMapperError
from travelexhibition.ports.uow_ports import UnitOfWork

log = logging.getLogger(__name__)


@final
@dataclass(slots=True, frozen=True, kw_only=True)
class SqlAlchemyUnitOfWork(UnitOfWork):
    session: AsyncSession

    async def commit(self) -> None:
        """:raises DataMapperError:"""
        try:
            await self.session.commit()
            log.debug("%s Main session.", "DB_COMMIT_DONE")

        except SQLAlchemyError as err:
            raise DataMapperError(f"Error") from err

    async def rollback(self) -> None:
        """:raises DataMapperError:"""
        try:
            await self.session.rollback()
            log.debug("%s Main session.", "DB_COMMIT_DONE")
        except SQLAlchemyError as err:
            raise DataMapperError(f"Error") from err




