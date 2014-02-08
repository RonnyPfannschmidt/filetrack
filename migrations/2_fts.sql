-- migration switch_to_fts
-- after initial
alter table filename_blob rename to filename_blob_old;

create table blob(
    id integer primary key,
    hash unique
);

create virtual table fts_filename using fts4(name);

create table file_data (
    id integer primary key,
    filename_rowid integer
        references fts_filename(rowid),
    blob_id integer
        references blob(id)
);


create view filename_blob as
select
    fts_filename.name as name,
    blob.hash as blob
from file_data
join fts_filename on fts_filename.rowid = filename_rowid
join blob on blob.id = file_data.blob_id;


create trigger filename_blob_insert
instead of insert on filename_blob
begin
    insert or ignore
    into blob (hash)
    values (new.blob);

    insert into fts_filename (name)
    values (new.name);

    insert into file_data (filename_rowid, blob_id) 
    values (
        last_insert_rowid(),
        (select id from blob where hash = new.blob)
    );
end;


insert into filename_blob (name, blob)
select name, blob from filename_blob_old;
drop table filename_blob_old;

