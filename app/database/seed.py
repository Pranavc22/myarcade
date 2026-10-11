
from sqlalchemy import select

from app.database.db import SessionLocal
from app.database.models import Agreement


INITIAL_AGREEMENT = {
    "title": "Our Arcade Agreement",
    "version": 1,
    "body": ("OurArcade is a shared and safe space for us to play games and bully each other. We agree to be as disrespectful, mean and as competitive as possible. Hopefully, this platform will serve as a place that brings a smile to our funny faces. Signing this agrrement is not an option. You need to do it. If you don't, expect to be at gunpoint."),
}


def seed_initial_agreement() -> None:
    with SessionLocal() as db:
        existing = db.scalar(
            select(Agreement).where(
                Agreement.title == INITIAL_AGREEMENT["title"],
                Agreement.version == INITIAL_AGREEMENT["version"],
            )
        )

        if existing:
            print("Initial agreement already exists.")
            return

        agreement = Agreement(**INITIAL_AGREEMENT)
        db.add(agreement)
        db.commit()

        print(f"Created agreement: {agreement.title} v{agreement.version}")


if __name__ == "__main__":
    seed_initial_agreement()
