CREATE TABLE neatapp (
    id serial primary key,
    payload jsonb not null,
    image_path text not null
);
