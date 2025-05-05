from sqlmodel import Session, select

from .db import engine
from .models import Stage, Theater
from .services.theater_service import TheaterService


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
        session.commit()

        fomenki = TheaterService().get_by_theater_name(session, "fomenki")
        ramt = TheaterService().get_by_theater_name(session, "ramt")
        sti = TheaterService().get_by_theater_name(session, "sti")

        # Create stages
        stages = [
            # Fomenki stages
            Stage(
                name="Старая сцена, Зелёный зал",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 30",
            ),
            Stage(
                name="Старая сцена, Серый зал",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 30",
            ),
            Stage(
                name="Новая сцена, Малый зал",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 29",
            ),
            Stage(
                name="Новая сцена, Малый зал",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 29",
            ),
            Stage(
                name="Новая сцена, Большой зал",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 29",
            ),
            Stage(
                name="Новая сцена, Фойе",
                theater_id=fomenki.theater_id,
                address="Набережная Тараса Шевченко, 29",
            ),
            # RAMT stages
            Stage(
                name="Большая сцена",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Маленькая сцена",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Черная комната",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Театральный двор",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Белая комната",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            Stage(
                name="Большая сцена*",
                theater_id=ramt.theater_id,
                address="Театральная площадь, 2",
            ),
            # STI stages
            Stage(
                name="Основная сцена",
                theater_id=sti.theater_id,
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
