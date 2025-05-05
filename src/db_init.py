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
        theater_count = session.exec(select(Theater)).count()
        if theater_count > 0:
            print("Database already seeded with theaters.")
            return

        # Create theaters
        theaters = [
            Theater(
                theater_id=1,
                name="fomenki",
                full_name="Мастерская Петра Фоменко",
                url="https://fomenko.theatre.ru/",
            ),
            Theater(
                theater_id=2,
                name="ramt",
                full_name="Российский академический молодежный театр",
                url="https://ramt.ru/",
            ),
            Theater(
                theater_id=3,
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
                stage_id=1,
                name="Основная сцена",
                theater_id=1,
                address="Набережная Тараса Шевченко, 30",
            ),
            Stage(
                stage_id=2,
                name="Новая сцена",
                theater_id=1,
                address="Набережная Тараса Шевченко, 29",
            ),
            # RAMT stages
            Stage(
                stage_id=3,
                name="Большая сцена",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                stage_id=4,
                name="Маленькая сцена",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                stage_id=5,
                name="Черная комната",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                stage_id=6,
                name="Театральный двор",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                stage_id=7,
                name="Белая комната",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            Stage(
                stage_id=8,
                name="Большая сцена*",
                theater_id=2,
                address="Театральная площадь, 2",
            ),
            # STI stages
            Stage(
                stage_id=5,
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
