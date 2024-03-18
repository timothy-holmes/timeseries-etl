# move to root project dir to generate

from genson import SchemaBuilder
import requests

from src.timeseries_etl.config import BOMConfig

params = BOMConfig.PARAMS
sites = BOMConfig.SITES
objects = [
    (
        requests.get(
            site["url"], headers=params["headers"], params=params["cookies"]
        ).json()
    )
    for site in sites
]

builder = SchemaBuilder()

for obj in objects:
    builder.add_object(obj)

with open("./tests/data/bom_schema.json", "w") as f:
    f.write(builder.to_json(indent=4))
