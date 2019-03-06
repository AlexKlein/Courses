select table_schema||'.'||table_name as full_name,
        column_name,
        data_type||
        case
            when is_nullable = 'NO' then
                ' not null'
            else
                ''
        end as column_desc
 from   information_schema.columns
 where  table_name = 'columns'
 order by table_schema,
          table_name,
          ordinal_position