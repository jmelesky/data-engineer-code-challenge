import json
import csv
from datetime import datetime

attendances = {}
# Open attendances JSON file
with open('data/attendances.json') as f:
  attendances = json.loads(f.read())

print("processed", len(attendances), "attendances")

# add your code for processing this data here! 
# see https://github.com/mobilizeamerica/api#attendances for data model documentation

# a few convenience functions

def format_datetime(epoch_seconds):
  # We're assuming UTC, which may not be valid. However, only
  # events specify a timezone, and not all datetimes are part
  # of events, so we have to assume something.
  dt = datetime.utcfromtimestamp(int(epoch_seconds))

  # conforming to BigQuery's datetime literal format
  # return "DATETIME '" + dt.strftime('%Y-%m-%d %H:%M:%S') + "'"

  # or to postgres's datetime literal format
  return dt.strftime('%Y-%m-%d %H:%M:%S')

def format_json(js_blob):
  # conforming to BigQuery's json literal format
  # return "JSON '" + json.dumps(js_blob) + "'"

  # or to postgres's json format
  return json.dumps(js_blob)

def write_csv(data, filename):
  # sort the field names to guarantee stability
  fieldnames = sorted(data[0].keys())

  with open(filename, 'w') as csvf:
    writer = csv.DictWriter(csvf, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerows(data)


# functions to build our data

def build_event(event_dict):
  # event may be a dimension table, but, once you collapse its nested data
  # upwards, it has the most fields of any of our tables.
  #
  # We're ignoring some data, here. Tags, for example, is always an empty
  # array in our data set, so we're not building that out. Likewise
  # timeslots. Other data we're making simplifying assumptions about. A
  # Location's address_lines, for example, never has more than one non-empty
  # string in it in this data set, so we're simply promoting that to its own
  # field.
  #
  # These assumptions may not hold when presented with novel data, so we
  # must keep our eyes open.
  #
  # One final caveat for events: often, they're largely empty, generally
  # when we don't have permission for more.

  event = {
    'id': None,
    'created_date': None,
    'modified_date': None,
    'title': None,
    'description': None,
    'event_type': None,
    'visibility': None,
    'timezone': None,
    'featured_image_url': None,
    'browser_url': None,
    'high_priority': None,
    'is_virtual': None,
    'visibility': None,
    'address_visibility': None,
    'created_by_volunteer_host': None,
    'virtual_action_url': None,
    'accessibility_status': None,
    'accessibility_notes': None,
    'approval_status': None,
    'instructions': None,
    'sponsor_id': None,
    'sponsor_slug': None,
    'sponsor_name': None,
    'sponsor_type': None,
    'venue': None,
    'address': None,
    'locality': None,
    'region': None,
    'country': None,
    'postal_code': None,
    'latitude': None,
    'longitude': None,
    'congressional_district': None,
    'state_leg_district': None,
    'state_senate_district': None,
    'contact_name': None,
    'contact_email': None,
    'contact_phone': None,
    'campaign_slug': None,
    'event_create_page_url': None,
  }

  event['event_type'] = event_dict['event_type']
  event['is_virtual'] = event_dict['is_virtual']

  if event_dict['id']:
    event['id'] = int(event_dict['id'])
    # if we have an id, then we have everything else, too
    event['created_date'] = format_datetime(event_dict['created_date'])
    event['modified_date'] = format_datetime(event_dict['modified_date'])
    event['title'] = event_dict['title']
    event['description'] = event_dict['description']
    event['visibility'] = event_dict['visibility']
    event['timezone'] = event_dict['timezone']
    event['featured_image_url'] = event_dict['featured_image_url']
    event['browser_url'] = event_dict['browser_url']
    event['high_priority'] = event_dict['high_priority']
    event['visibility'] = event_dict['visibility']
    event['address_visibility'] = event_dict['address_visibility']
    event['created_by_volunteer_host'] = event_dict['created_by_volunteer_host']
    event['virtual_action_url'] = event_dict['virtual_action_url']
    event['accessibility_status'] = event_dict['accessibility_status']
    event['accessibility_notes'] = event_dict['accessibility_notes']
    event['approval_status'] = event_dict['approval_status']
    event['instructions'] = event_dict['instructions']

    # sponsor fields
    event['sponsor_id'] = event_dict['sponsor']['id']
    event['sponsor_slug'] = event_dict['sponsor']['slug']
    event['sponsor_name'] = event_dict['sponsor']['name']
    event['sponsor_type'] = event_dict['sponsor']['org_type']

    # location fields
    if event_dict['location']:
      event['venue'] = event_dict['location']['venue']
      event['address'] = event_dict['location']['address_lines'][0]
      event['locality'] = event_dict['location']['locality']
      event['region'] = event_dict['location']['region']
      event['country'] = event_dict['location']['country']
      event['postal_code'] = event_dict['location']['postal_code']
      event['congressional_district'] = event_dict['location']['congressional_district']
      event['state_leg_district'] = event_dict['location']['state_leg_district']
      event['state_senate_district'] = event_dict['location']['state_senate_district']
      if event_dict['location']['location']:
        event['latitude'] = event_dict['location']['location']['latitude']
        event['longitude'] = event_dict['location']['location']['longitude']

    # contact fields
    if event_dict['contact']:
      event['contact_name'] = event_dict['contact']['name']
      event['contact_email'] = event_dict['contact']['email_address']
      event['contact_phone'] = event_dict['contact']['phone_number']

    # EventCampaign fields
    if event_dict['event_campaign']:
      event['campaign_slug'] = event_dict['event_campaign']['slug']
      event['event_create_page_url'] = event_dict['event_campaign']['event_create_page_url']

  return event


def build_timeslot(timeslot_dict):
  start_date = format_datetime(timeslot_dict['start_date'])
  end_date = format_datetime(timeslot_dict['end_date'])
  timeslot = {
    'id': None,
    'start_date': start_date,
    'end_date': end_date,
    'is_full': timeslot_dict['is_full'],
    'instructions': timeslot_dict['instructions'],
  }

  if timeslot_dict['id']:
    timeslot['id'] = int(timeslot_dict['id'])

  return timeslot


def build_person(person_dict):
  created_date = format_datetime(person_dict['created_date'])
  modified_date = format_datetime(person_dict['modified_date'])
  blocked_date = None
  if person_dict['blocked_date']:
    blocked_date = format_datetime(person_dict['blocked_date'])

  # Person is interesting because it has a few arrays
  # (email_addresses, phone_numbers, postal_addresses) that
  # are always length 1 (per the API doc as of this writing).
  # It's reasonable to assume that some day they may have more
  # than one element, in which case we'll want to search for
  # `element['primary']==True`.
  #
  # Until then, though, just extract the one element.
  
  person = {
    'id': None,
    'created_date': created_date,
    'modified_date': modified_date,
    'blocked_date': blocked_date,
    'given_name': person_dict['given_name'],
    'family_name': person_dict['family_name'],
    'sms_opt_in_status': person_dict['sms_opt_in_status'],
    'email': person_dict['email_addresses'][0]['address'],
    'phone': person_dict['phone_numbers'][0]['number'],
    'postal_code': person_dict['postal_addresses'][0]['postal_code'],
  }

  if person_dict['id']:
    person['id'] = int(person_dict['id'])

  return person


def build_attendance(attendance_dict):
  created_date = format_datetime(attendance_dict['created_date'])
  modified_date = format_datetime(attendance_dict['modified_date'])

  custom_signup_str = format_json(attendance_dict['custom_signup_field_values'])

  att = {
    'id': None,
    'promoter_id': None,
    'promoter_slug': None,
    'promoter_name': None,
    'promoter_type': None,
    'event_id': None,
    'timeslot_id': None,
    'person_id': None,
    'event_type': None,
    'event_is_virtual': None,
    'timeslot_start': None,
    'timeslot_end': None,
    'custom_signup_fields': custom_signup_str,
    'created_date': created_date,
    'modified_date': modified_date,
    'rating': attendance_dict['rating'],
    'status': attendance_dict['status'],
    'attended': attendance_dict['attended'],
    'referrer_source': attendance_dict['referrer']['utm_source'],
    'referrer_medium': attendance_dict['referrer']['utm_medium'],
    'referrer_campaign': attendance_dict['referrer']['utm_campaign'],
    'referrer_term': attendance_dict['referrer']['utm_term'],
    'referrer_content': attendance_dict['referrer']['utm_content'],
    'referrer_url': attendance_dict['referrer']['url'],
  }

  if attendance_dict['id']:
    att['id'] = int(attendance_dict['id'])

  # if the attendance and event *both* have a sponsor, with a *different* id
  if (attendance_dict['sponsor'] and 'id' in attendance_dict['sponsor']
      and attendance_dict['event']['sponsor']
      and 'id' in attendance_dict['event']['sponsor']
      and attendance_dict['sponsor']['id'] != attendance_dict['event']['sponsor']['id']):
    att['promoter_id'] = attendance_dict['sponsor']['id']
    att['promoter_name'] = attendance_dict['sponsor']['name']
    att['promoter_slug'] = attendance_dict['sponsor']['slug']
    att['promoter_type'] = attendance_dict['sponsor']['org_type']

  return att



if __name__ == '__main__':
  # Okay, some of our data comes back without ids. Rather than populate
  # our csv with data we can't reference, we'll only record the ones
  # with ids. That means we can use dicts for easy de-duping.
  #
  # Later on, we'll collapse some of the data upwards into the attendance
  # record so it's still queryable.
  (events, timeslots, persons) = ({}, {}, {})

  # And we're going to build an array of attendances. Like events and
  # timeslots, sometimes attendance ids are null, but since nothing
  # references them, we can safely move forward without them.
  atts = []

  for attendance in attendances:
    event = build_event(attendance['event'])
    if event['id'] and event['id'] not in events:
      events[event['id']] = event

    timeslot = build_timeslot(attendance['timeslot'])
    if timeslot['id'] and timeslot['id'] not in timeslots:
      timeslots[timeslot['id']] = timeslot

    person = build_person(attendance['person'])
    if person['id'] and person['id'] not in persons:
      persons[person['id']] = person

    att = build_attendance(attendance)

    # let's collapse upwards a few bits we don't want to lose
    # to missing ids
    att['event_type'] = event['event_type']
    att['event_is_virtual'] = event['is_virtual']
    att['timeslot_start'] = timeslot['start_date']
    att['timeslot_end'] = timeslot['end_date']

    # and finally we populate the references to the dimension tables
    att['event_id'] = event['id']
    att['timeslot_id'] = timeslot['id']
    att['person_id'] = person['id']

    atts.append(att)


  # listify the dicts (the keys were only used for de-duping, so we
  # only need the values).

  event_list = [e for e in events.values()]
  person_list = [p for p in persons.values()]
  timeslot_list = [t for t in timeslots.values()]

  write_csv(event_list, 'data/events.csv')
  write_csv(person_list, 'data/persons.csv')
  write_csv(timeslot_list, 'data/timeslots.csv')
  write_csv(atts, 'data/attendances.csv')



