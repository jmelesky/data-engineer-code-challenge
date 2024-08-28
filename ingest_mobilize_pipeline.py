import requests
from google.cloud import bigquery
import os

# Two structural things jumped out at me here
#
# First, we're parsing json, writing it out to a file, then
# re-parsing it from that file. Even if we want to keep the
# file for archival purposes, we needn't re-parse it. This
# approach smacks of cut-and-paste'd code--not a problem,
# necessarily, but worth re-examining the assumptions. We
# may be running this from a place where saving the file is
# a significant cost (monetarily or timewise), for example.
#
# The second is that we're re-connecting to BigQuery for
# every row, which is probably a more pressing problem than
# the file issue. Just moving that out of the loop should
# make things faster and more stable.
#
# Finally, I noticed that we're only ever inserting data
# into BigQuery, though the problem description describes
# updating attendances. Without knowing how that table is
# defined and used, I'm not going to make that code change,
# but it's definitely a conversation I want to have with my
# internal customers.

def download_data() -> json[list[dict]]:
    base_url = "https://api.mobilize.us/v1/"
    endpoint = "attendances"
    headers = {"Authorization": "Bearer {}".format(os.environ.get("MOBILIZE_API_KEY"))}

    response = requests.get(base_url + endpoint, headers=headers)
    result = response.json
    return result


def load_events(data: json):
    client = bigquery.Client()
    table = client.get_table("wfp-data-project.mobilize.events")
    for row in data:
        try:
            event = {
                key: value
                for key, value in row["event"].items()
                if key
                in (
                    "created_date",
                    "modified_date",
                    "id",
                    "title",
                    "event_type",
                    "summary",
                    "description",
                )
            }
            client.insert_rows(table, [event])
        except:
            print("error loading row")


data = download_data()
loadevents(data)
