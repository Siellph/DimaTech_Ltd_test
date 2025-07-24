import json
import asyncio
import argparse
from datetime import datetime
from pathlib import Path
from typing import List

from sqlalchemy import insert

from webapp.db.postgres import async_session
from webapp.models.meta import metadata

parser = argparse.ArgumentParser()
parser.add_argument('fixtures', nargs='+', help='<Required> Set flag')
args = parser.parse_args()


def parse_dates_in_values(values: list, datetime_fields: set = None):
    """Преобразует ISO-строки в datetime объекты"""
    datetime_fields = datetime_fields or {'timestamp', 'account_date'}

    for row in values:
        for key in row:
            if key in datetime_fields and isinstance(row[key], str):
                try:
                    row[key] = datetime.fromisoformat(row[key].replace('Z', '').split('+')[0])
                except Exception:
                    pass


async def main(fixtures: List[str]) -> None:
    for fixture in fixtures:
        fixture_path = Path(fixture)
        model = metadata.tables[fixture_path.stem]

        with open(fixture_path, 'r') as file:
            values = json.load(file)

        parse_dates_in_values(values)

        async with async_session() as session:
            await session.execute(insert(model).values(values))
            await session.commit()


if __name__ == '__main__':
    asyncio.run(main(args.fixtures))
