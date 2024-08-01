import requests
import json

from datetime import datetime
from waste_collection_schedule import Collection  # type: ignore[attr-defined]

TITLE = "Wyndham City Council, Melbourne"
DESCRIPTION = "Source for Wyndham City Council rubbish collection."
URL = "https://wyndham.vic.gov.au"

TEST_CASES = {
    "Coord_001": {"lat": "-37.9030792", "lng": "144.6581664"},
}
HEADERS = {
    "user-agent": "Mozilla/5.0",
}
ICON_MAP = {
    "Green_Waste": "mdi:leaf",
    "Waste": "mdi:trash-can-outline",
    "Recycle": "mdi:recycle",
}

class Source:
    def __init__(self, lat, lon):
        self._lat = lat
        self._lng = lon

    def fetch(self):

        s = requests.Session()
        r = s.get(f"https://digital.wyndham.vic.gov.au/mywyndham/JSON/show_closest_feed.php?lat={self._lat}&lng={self._lng}", headers=HEADERS)
        json_data = json.loads(r.text)["waste_collection_information"]

        entries = []

        for bin,time in json_data.items():
            entries.append(
                Collection(
                    date=datetime.strptime(time, "%A, %d %B %Y").date(),
                    t=bin,
                    icon=ICON_MAP.get(bin),
                )
            )

        return entries
