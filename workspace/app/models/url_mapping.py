import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class URLMapping(AsyncAttrs, Base):
    __tablename__ = "url_mappings"

    id = sa.Column(sa.Integer, primary_key=True, index=True)
    short_key = sa.Column(sa.String(10), unique=True, index=True, nullable=False)
    long_url = sa.Column(sa.Text, nullable=False)
    created_at = sa.Column(sa.DateTime(timezone=True), server_default=func.now(), nullable=False)
    expiration_date = sa.Column(sa.DateTime(timezone=True), nullable=True)
    click_count = sa.Column(sa.Integer, default=0, nullable=False)
    custom_alias = sa.Column(sa.String(50), unique=True, nullable=True)

    def __repr__(self):
        return f"<URLMapping(short_key={self.short_key}, long_url={self.long_url})>"
