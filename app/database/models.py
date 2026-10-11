from datetime import datetime
from sqlalchemy import (
    Boolean,
    CheckConstraint,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.db import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, index=True, nullable=False)
    display_name: Mapped[str] = mapped_column(String(100), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    signatures: Mapped[list["AgreementSignature"]] = relationship(back_populates="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    agreement_support: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        server_default="false",
        nullable=False,
    )
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)


class Agreement(Base):
    __tablename__ = "agreements"
    __table_args__ = (UniqueConstraint("title", "version", name="uq_agreement_title_version"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    title: Mapped[str] = mapped_column(String(120), nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    body: Mapped[str] = mapped_column(Text, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    signatures: Mapped[list["AgreementSignature"]] = relationship(back_populates="agreement")


class AgreementSignature(Base):
    __tablename__ = "agreement_signatures"
    __table_args__ = (
        UniqueConstraint("agreement_id", "user_id", name="uq_agreement_signature_user"),
        CheckConstraint(
            "signature_method IN ('typed', 'drawn')",
            name="ck_signature_method",
        ),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    agreement_id: Mapped[int] = mapped_column(ForeignKey("agreements.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    signer_name: Mapped[str] = mapped_column(String(100), nullable=False)
    signature_method: Mapped[str] = mapped_column(String(10), nullable=False)
    signature_data: Mapped[str] = mapped_column(Text, nullable=False)
    signed_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    user: Mapped["User"] = relationship(back_populates="signatures")
    agreement: Mapped["Agreement"] = relationship(back_populates="signatures")
