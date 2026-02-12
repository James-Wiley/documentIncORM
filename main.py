from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, Client, User, Account, Preference, Statement, Notification, AuditLog
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = (
    f"postgresql+psycopg2://"
    f"{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:"
    f"{os.getenv('DB_PORT')}/"
    f"{os.getenv('DB_NAME')}"
)

engine = create_engine(DATABASE_URL, echo=True)
Session = sessionmaker(bind=engine)


def pause(text):
    input(f"\n--- {text} ---\nPress Enter to continue...\n")


def run():
    print("\nResetting tables for clean demo")
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    pause("Fresh tables created")

    session = Session()

    
    # CREATE CLIENT
    print("\nCreating parent client...")
    client = Client(name="PARENT_COMPANY")
    session.add(client)
    session.commit()
    pause("Client inserted")

    
    # CREATE USER
    print("\nCreating user record...")
    new_user = User(
        client_id=client.client_id,
        email="USER_12345@example.com",
        phone_number="999-999-9999",
        role="STANDARD"
    )

    session.add(new_user)
    session.commit()
    pause("User inserted (CREATE)")

    
    # READ USERS
    print("\nReading users from database...")
    users = session.query(User).all()
    for u in users:
        print(
            f"[USER] ID={u.user_id} | "
            f"EMAIL={u.email} | "
            f"PHONE={u.phone_number} | "
            f"ROLE={u.role}"
        )
    pause("Users retrieved (READ)")

    
    # UPDATE USER
    print("\nUpdating user email and role...")
    user_to_update = session.query(User).filter_by(
        email="USER_12345@example.com"
    ).first()

    user_to_update.email = "DIFFERENT@example.com"
    user_to_update.role = "ADMIN"
    session.commit()
    pause("User updated (UPDATE)")
    
    # DELETE USER
    print("\nDeleting updated user...")
    user_to_delete = session.query(User).filter_by(
        email="DIFFERENT@example.com"
    ).first()

    session.delete(user_to_delete)
    session.commit()
    pause("User deleted (DELETE)")

    print("\nDemo complete.")
    session.close()



if __name__ == "__main__":
    run()
