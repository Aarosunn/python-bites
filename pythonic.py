from pathlib import Path
from datetime import datetime
from dataclasses import dataclass, field
from typing import Iterator
import logging
import csv

logger = logging.getLogger(__name__)

FOOD_CSV = Path("pythonic-nibble/food.csv")
ACTIVITIES_CSV = Path("pythonic-nibble/activities.csv")


def today() -> datetime:
    return datetime.now()


@dataclass
class Entry:
    description: str
    calories: int
    date: datetime = field(default_factory=today)


def append_entry(filename: Path, entry: Entry) -> None:
    with open(filename, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(
            [entry.date.strftime("%Y-%m-%d"), entry.description, entry.calories]
        )
    logger.info(
        "Appended to %s: %s (%s kcal)", filename, entry.description, entry.calories
    )


def read_entries(filename: Path) -> Iterator[Entry]:
    with open(filename, "r", newline="") as f:
        reader = csv.reader(f)
        for row in reader:
            if row:
                yield Entry(
                    description=row[1],
                    calories=int(row[2]),
                    date=datetime.strptime(row[0], "%Y-%m-%d"),
                )


def run_day_summary(date: datetime) -> None:
    food = read_entries(FOOD_CSV)
    activity = read_entries(ACTIVITIES_CSV)

    food_total = sum(
        entry.calories for entry in food if entry.date.date() == date.date()
    )
    activity_total = sum(
        entry.calories for entry in activity if entry.date.date() == date.date()
    )
    net = food_total - activity_total

    print(f"\nSummary for {date}")
    print(f"     Food:     {food_total} kcal")
    print(f"     Activity: {activity_total} kcal")
    print(f"     Net:      {net} kcal")


def main() -> None:
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s"
    )
    append_entry(FOOD_CSV, Entry("Banana", 100))
    append_entry(ACTIVITIES_CSV, Entry("Running", 300))
    run_day_summary(today())


if __name__ == "__main__":
    main()
