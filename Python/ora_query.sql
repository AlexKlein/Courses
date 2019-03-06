select owner||'.'||table_name as full_name,
       column_name,
       data_type||' ('||data_length||')'||
       case
           when nullable = 'N' then
               ' not null'
       end as column_desc
from   sys.all_tab_columns
where  owner = 'SYS' and
       table_name = 'ALL_TAB_COLUMNS'
order by owner,
         table_name,
         column_id