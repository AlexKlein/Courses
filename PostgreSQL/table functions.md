# Table functions

Often it is necessary to make a parameterized query to the data and the usual presentation does not help, but a table function will come to the rescue.
Table functions are functions that return data in the form of a collection, to which we can refer to the from section of the query, as if this collection were a relational table.

In the example, a report is created with full column naming, in tables according to a given mask.
In the first case, a set of columns is defined as in the specified table:
```sql
create or replace function colls_full_names(pTableName varchar)
returns setof information_schema.columns as
$body$
declare
    r information_schema.columns%rowtype;
begin
    for r in select *
             from information_schema.columns col
             where  lower(col.table_name) like '%'||pTableName||'%'
             order by col.table_schema,
                      col.table_name,
                      col.column_name loop
        -- returns the current line from the query
        return next r;
    end loop;
    return;
end
$body$
language plpgsql;
```

And in the second case, the given set of columns is arbitrary:
```sql
create or replace function colls_full_names(pTableName varchar)
returns table(full_name varchar) as
$code$
    select col.table_schema||'.'||
           col.table_name||'.'||
           col.column_name as full_name
    from information_schema.tables tab
    inner join information_schema.columns col
            on col.table_schema = tab.table_schema and
               col.table_name = tab.table_name
    where  lower(tab.table_name) like '%'||pTableName||'%'
    order by col.table_schema,
             col.table_name,
             col.column_name
$code$
language sql;
```

***
Function calls
====

The call of this report is made by query with parameter.
```sql
select * from colls_full_names('agg');
```

***
The task
====

It is necessary to make a table function that creates a report accessed. In this case, the parameters will be users who have given and gained access (information_schema.usage_privileges). The fields that the function will return:
• object_schema;
• fobject_type;
• privilege_type.