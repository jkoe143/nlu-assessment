create table violations (
    id int primary key, -- unique identifier
    date date not null, -- mandatory
    code text,
    status text,
    description text,
    inspector_comments text,
    address text not null -- mandatory
);

create table scofflaws (
    record_id text primary key, -- unique identifier
    address text not null -- mandatory
);

create table comments (
    id serial primary key, -- generated with table creation
    author text,
    datetime timestamp,
    address text,
    comment text
);

-- indexes for better performance, faster lookup when querying
create index idx_violations_address on violations(address);
create index idx_violations_date on violations(date);
create index idx_scofflaws_address on scofflaws(address);