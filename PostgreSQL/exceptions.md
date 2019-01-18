# Error processing

***
Anonymous block
====

PL/pgSQL has a block structure, the scheme of which is presented below:
DO [ LANGUAGE имя_языка ] код;

For example, I will write an anonymous block in which I will display the number of tables in the public schema to the user.
```sql
do $$declare             -- variable block declaration
	cntColumn integer;   -- column number variable
begin
    select count(column_name) as counter  -- aggregate function of calculating the number of columns
	into   cntColumn                      -- operator assigning the result of a query to a variable
	from   information_schema.columns     -- the table from which the selection is
    where  table_name in 				  -- filter tables by list from subquery
						 (select table_name                 -- selection of table names
						  from   information_schema.tables  -- the table from which the selection is
						  where  table_schema = 'public');  -- filter scheme
        
end$$;
```

***
RAISE operator
====

One of the most common ways to debug is displaying text on the screen. The RAISE command is designed to display messages and cause errors. The possible values for the severity level of the error are DEBUG, LOG, INFO, NOTICE, WARNING, and EXCEPTION. The default is EXCEPTION.
```sql
do $$declare
	cntColumn integer;
begin
    select count(column_name) as counter
	into   cntColumn
	from   information_schema.columns
    where  table_name in (select table_name
						  from   information_schema.tables
						  where  table_schema = 'public');
    
	raise notice 'The number of columns in the public schema is - %', cntColumn;  -- text output to the screen after concatenation
	
end$$;
```

***
Exceptions
====

In the event of an error, the block is urgently terminated, in order to avoid exiting the block with an error, there are exceptions. Some exceptions are predefined in the DBMS.
When an error occurs, the block stops and displays the error one level higher, for example:
```sql
do $$declare
    vRes float;  -- calculation result
begin  -- the first block
    begin  -- the second block
        -- calculating the sum and assigning the result to a variable
        select 2/0 
        into   vRes;
    end;
end $$;
```

Now I will add the handling of the divide-by-zero error.
```sql
do $$declare
	cntColumn integer;
begin
    select count(column_name)/0 as counter  -- division by zero
	into   cntColumn
	from   information_schema.columns
    where  table_schema = 'public'
	group by table_name;                    -- table name grouping
	
	raise notice 'The number of columns in the public schema is - %', cntColumn;

exception
    when division_by_zero then  -- exception handling when dividing by zero
        raise exception 'Division by zero';   -- display error message
    when others then            -- handling all exceptions
        raise exception 'Error %', sqlstate;  -- display error message
	
end$$;
```

***
Function creation
====

I will make the named block from anonymous, for an example I will make function. The main difference between the procedure and the function is that the function always returns the value of the declared data type. For example, I pass a text parameter to the function, which I will use as the Y / N flag, and the function must return a numeric value. Also, the flag will fulfill the condition, if the flag is Y, then you need to calculate the average salary of the IT department, otherwise assign the value -1 to the average salary variable, return the static value -2 in case of errors.
I present the function "learning" in the hr scheme with a text parameter that returns a numeric value:
```sql
create or replace function learning (pFlag varchar) returns float  -- function creation
as $$
declare
    avgColumn float;
begin
    -- check of the average salary calculation flag
    if pFlag = 'Y' then  -- use of the parameter in the test block
        select cast(avg(countedTables.counter) as float) as average 
		into   avgColumn
		from  (select count(column_name) AS counter
			   from   information_schema.columns
			   where  table_schema = 'public'
			   group by table_name) countedTables;
    else
        avgColumn := -1;    -- variable assignment
    end if;
    
    return avgColumn;       -- return of function result
    
exception
    when division_by_zero then
        raise exception 'Division by zero';
		return -2;
    when others the
        raise exception 'Error %', sqlstate;
		return -3;
end
$$ language plpgsql;
```

***
Variants of function calls
====

To call this function, I use an anonymous block. At the same time, it is necessary to remember that the function always returns some value, respectively, it is necessary to remember about the data types conformity.
```sql
do $$
begin
    raise notice 'Average number of columns: %', to_char(learning('Y'), '9G999D9');
end $$;
```

In addition to the anonymous block, the value from the function can be obtained by a simple query:
```sql
select 'Average number of columns: '||to_char(learning('Y'), '9G999D9') as result;
```

***
The task
====

It is necessary to create a function and its call.
The function must take two numerical values of the parameters and count the bonus for the previous year.
The first parameter is salary.
The second parameter is the grade.

Formulas for calculating the bonus:
0-10 grade:
Salary * 12 * 0,08 * 1 * 1,3 * 0,87
from 11 grade and higher:
Salary * 12 * 0,15 * 1 * 1,3 * 0,87

For each branch of the solution, you need to write a message.
It is necessary to do the processing of embedded exceptional operations.