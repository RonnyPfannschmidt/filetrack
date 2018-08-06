-- migration blob_add_size
-- after switch_to_fts

alter table blob
  add column size default null;
