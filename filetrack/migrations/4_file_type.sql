-- migration add_file_type
-- after switch_to_fts

alter
    table file_data
    add column type varchar;


create index i_filetype on file_data(type);
