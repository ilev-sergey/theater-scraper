from sqlmodel import Session, select

from .db import engine
from .models import Stage, Theater


def seed_theaters_and_stages(session: Session) -> None:
    """
    Seed the database with initial theater and stage data.
    This should only be run once when setting up a new database.
    """
    try:
        # Check if we already have theaters (to avoid duplicates)
        theater = session.exec(select(Theater)).first()
        if theater is not None:
            print("Database already seeded with theaters.")
            return

        # Create theaters
        theaters = [
            Theater(
                name="fomenki",
                full_name="Мастерская Петра Фоменко",
                url="https://fomenko.theatre.ru/",
            ),
            Theater(
                name="ramt",
                full_name="Российский академический молодежный театр",
                url="https://ramt.ru/",
            ),
            Theater(
                name="sti",
                full_name="Студия театрального искусства",
                url="https://sti.ru/",
            ),
        ]
        session.add_all(theaters)

        # Create stages
        stages = [
            # Fomenki stages
            Stage(
                name="Основная сцена",
                theater_id=1,
                address="Набережная Тараса Шевченко, 30",
            ),
            Stage(
                name="Новая сцена",
                theater_id=1,
                address="Набережная Тараса Шевченко, 29",
            ),
            # RAMT stages
            Stage(
                name="Большая сцена",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Маленькая сцена",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Черная комната",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Театральный двор",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Белая комната",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Большая сцена*",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            # STI stages
            Stage(
                name="Основная сцена",
                theater_id=3,
                address="ул. Станиславского, 21 стр. 7",
            ),
        ]
        session.add_all(stages)

        session.commit()
        print("Successfully seeded database with theaters and stages.")

    except Exception as e:
        session.rollback()
        print(f"Error seeding database: {e}")


def initialize_database():
    """
    Initialize the database with seed data using a new session.
    """
    with Session(engine) as session:
        seed_theaters_and_stages(session)
