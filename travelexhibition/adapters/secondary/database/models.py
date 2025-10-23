from litestar.plugins.sqlalchemy import base
from sqlalchemy import Index, String, Text
from sqlalchemy.orm import Mapped, MappedAsDataclass, mapped_column


class Artifact(MappedAsDataclass, base.UUIDAuditBase, kw_only=True):
    __tablename__ = "artifacts"
    __table_args__ = (
        Index(
            "ix_artifacts_title",
            "title",
            postgresql_ops={"title": "text_pattern_ops"},
        ),
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    model3d_url: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str | None] = mapped_column(Text(1000), nullable=True)
