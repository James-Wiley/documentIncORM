from sqlalchemy import (
    Column, Integer, String, Date, DateTime,
    ForeignKey, Text, Table, UniqueConstraint
)
from sqlalchemy.orm import declarative_base, relationship
from datetime import datetime

Base = declarative_base()

# --------------------------
# Association Table (M:M)
# --------------------------
user_account = Table(
    "user_account",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("user.user_id", ondelete="CASCADE"), primary_key=True),
    Column("account_id", Integer, ForeignKey("account.account_id", ondelete="CASCADE"), primary_key=True),
)

# --------------------------
# Client
# --------------------------
class Client(Base):
    __tablename__ = "client"

    client_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)

    users = relationship("User", back_populates="client")

    def __repr__(self):
        return f"<Client(id={self.client_id}, name='{self.name}')>"


# --------------------------
# User
# --------------------------
class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True)
    client_id = Column(Integer, ForeignKey("client.client_id"))
    email = Column(String(255), unique=True, nullable=False)
    phone_number = Column(String(20))
    role = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    client = relationship("Client", back_populates="users")
    accounts = relationship("Account", secondary=user_account, back_populates="users")
    preference = relationship("Preference", back_populates="user", uselist=False)

    def __repr__(self):
        return f"<User(id={self.user_id}, email='{self.email}')>"


# --------------------------
# Account
# --------------------------
class Account(Base):
    __tablename__ = "account"

    account_id = Column(Integer, primary_key=True)
    account_number = Column(String(50), unique=True, nullable=False)
    account_type = Column(String(50))
    status = Column(String(50))

    users = relationship("User", secondary=user_account, back_populates="accounts")
    statements = relationship("Statement", back_populates="account")

    def __repr__(self):
        return f"<Account(id={self.account_id}, number='{self.account_number}')>"


# --------------------------
# Preference (1:1 with User)
# --------------------------
class Preference(Base):
    __tablename__ = "preference"

    preference_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.user_id", ondelete="CASCADE"), unique=True)
    delivery_method = Column(String(50))
    effective_date = Column(Date)

    user = relationship("User", back_populates="preference")

    def __repr__(self):
        return f"<Preference(user_id={self.user_id}, method='{self.delivery_method}')>"


# --------------------------
# Statement
# --------------------------
class Statement(Base):
    __tablename__ = "statement"

    statement_id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("account.account_id"))
    issue_date = Column(Date)
    delivery_type = Column(String(50))
    file_path = Column(Text)

    account = relationship("Account", back_populates="statements")
    notifications = relationship("Notification", back_populates="statement")
    audit_logs = relationship("AuditLog", back_populates="statement")

    def __repr__(self):
        return f"<Statement(id={self.statement_id}, account={self.account_id})>"


# --------------------------
# Notification
# --------------------------
class Notification(Base):
    __tablename__ = "notification"

    notification_id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey("statement.statement_id"))
    sent_date = Column(DateTime, default=datetime.utcnow)
    type = Column(String(50))

    statement = relationship("Statement", back_populates="notifications")

    def __repr__(self):
        return f"<Notification(id={self.notification_id})>"


# --------------------------
# Audit Log
# --------------------------
class AuditLog(Base):
    __tablename__ = "audit_log"

    log_id = Column(Integer, primary_key=True)
    statement_id = Column(Integer, ForeignKey("statement.statement_id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    action = Column(Text)

    statement = relationship("Statement", back_populates="audit_logs")

    def __repr__(self):
        return f"<AuditLog(id={self.log_id})>"
