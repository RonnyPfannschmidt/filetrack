-- migration add_file_accounted
-- after switch_to_fts

alter
    table file_data
    add column accounted integer default 0 not null;
