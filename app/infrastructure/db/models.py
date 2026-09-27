from sqlalchemy import Float, ForeignKey, Integer, String, Text
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class CatalogModel(Base):
    __tablename__ = "catalogs"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100), unique=True)
    description: Mapped[str | None] = mapped_column(Text)

    products: Mapped[list["ProductModel"]] = relationship(
        back_populates="catalog", cascade="all, delete-orphan"
    )


class ProductModel(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str | None] = mapped_column(Text)
    price: Mapped[float] = mapped_column(Float)
    quantity: Mapped[int] = mapped_column(Integer, default=0)
    catalog_id: Mapped[int] = mapped_column(
        ForeignKey("catalogs.id", ondelete="CASCADE"), index=True
    )

    catalog: Mapped[CatalogModel] = relationship(back_populates="products")
