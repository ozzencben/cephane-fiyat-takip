import sys
from sqlalchemy.orm import Session

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from .db import Base, SessionLocal, engine
from .models import Competitor

DEFAULT_COMPETITORS = [
    {
        "ad": "PttAVM (En Ucuz Rakip)",
        "base_url": "https://www.pttavm.com",
    },
    {
        "ad": "N11 / Pazarama (En Ucuz Rakip)",
        "base_url": "http://localhost:8001",
    },
    {
        "ad": "Hepsiburada (En Ucuz Rakip)",
        "base_url": "https://www.hepsiburada.com",
    },
]


def seed_competitors(db: Session) -> None:
    for comp_data in DEFAULT_COMPETITORS:
        existing = db.query(Competitor).filter(Competitor.ad == comp_data["ad"]).first()
        if not existing:
            db.add(Competitor(ad=comp_data["ad"], base_url=comp_data["base_url"]))
    db.commit()


def main() -> None:
    Base.metadata.create_all(bind=engine)
    session = SessionLocal()
    try:
        seed_competitors(session)
        print("✓ Tablolar ve Cep-Hane Teknoloji pazaryeri rakipleri (PttAVM, Hepsiburada, N11/Pazarama) oluşturuldu.")
    finally:
        session.close()


if __name__ == "__main__":
    main()
