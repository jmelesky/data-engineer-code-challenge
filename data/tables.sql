-- postgres syntax, for local testing
-- columns are alpha-sorted, to match the csv output


drop table if exists attendance;
create table attendance (
    attended boolean,
    created_date timestamp with time zone,
    custom_signup_fields jsonb,
    event_id bigint,
    event_is_virtual boolean,
    event_type text,
    id bigint,
    modified_date timestamp with time zone,
    person_id bigint,
    promoter_id bigint,
    promoter_name text,
    promoter_slug text,
    promoter_type text,
    rating text,
    referrer_campaign text,
    referrer_content text,
    referrer_medium text,
    referrer_source text,
    referrer_term text,
    referrer_url text,
    status text,
    timeslot_end timestamp with time zone,
    timeslot_id bigint,
    timeslot_start timestamp with time zone
);

drop table if exists event;
create table event (
    accessibility_notes text,
    accessibility_status text,
    address text,
    address_visibility text,
    approval_status text,
    browser_url text,
    campaign_slug text,
    congressional_district text,
    contact_email text,
    contact_name text,
    contact_phone text,
    country text,
    created_by_volunteer_host boolean,
    created_date timestamp with time zone,
    description text,
    event_create_page_url text,
    event_type text,
    featured_image_url text,
    high_priority boolean,
    id bigint,
    instructions text,
    is_virtual boolean,
    latitude float,
    locality text,
    longitude float,
    modified_date timestamp with time zone,
    postal_code text,
    region text,
    sponsor_id bigint,
    sponsor_name text,
    sponsor_slug text,
    sponsor_type text,
    state_leg_district text,
    state_senate_district text,
    timezone text,
    title text,
    venue text,
    virtual_action_url text,
    visibility text
);

drop table if exists person;
create table person (
    blocked_date timestamp with time zone,
    created_date timestamp with time zone,
    email text,
    family_name text,
    given_name text,
    id bigint,
    modified_date timestamp with time zone,
    phone text,
    postal_code text,
    sms_opt_in_status text
);

drop table if exists timeslot;
create table timeslot (
    end_date timestamp with time zone,
    id bigint,
    instructions text,
    is_full boolean,
    start_date timestamp with time zone
);
