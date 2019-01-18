# Cursors

The cursor is a pointer to the data.

***
Named (explicit) cursors
====

An explicit cursor is declared by the developer in the variable declaration block; the cursor can return one line, several lines, or not a single line. The cursor can be declared in the declaration sections of any PL/SQL block.
To control the explicit cursor, use the CURSOR, OPEN, FETCH and CLOSE operators .:

- The CURSOR operator declares an explicit cursor.
- The OPEN operator opens the cursor, creating a new result set based on the specified query.
- The FETCH operator sequentially extracts rows from the result set from beginning to end.
- The CLOSE operator closes the cursor and frees up the resources it occupies.

You can use this knowledge like this:
```sql
do $$
declare
    -- a simple cursor that returns two rows with one number in each
    cRep cursor 
	    for
    select 1 as num
    union all
    select 2 as num;
    
    vResCursor record; -- record type variable
    
begin
    -- cursor opening
    open cRep;
    
    -- loop to select data from the cursor
    loop
        -- setting values to variable
        fetch cRep into vResCursor;
		
		-- exit from a loop when there are no values left
		exit when not found;
        
        -- display data
        raise notice 'Num: %', vResCursor.num;
        
    end loop;
            
    -- closing the cursor, freeing the memory
    close cRep;
end $$;
```

For more program code flexibility, the cursor can be parameterized. In the following example, parameters are added to the cursor. Also, the query in the cursor is hierarchical.
In this example, a while loop is used, in which the condition for three passes inside the loop is specified.
```sql
do $$declare
    -- select "id" by parent "id"
    cRep cursor (pParent integer)
		for
	with recursive r as (
		-- starting part of recursion ("anchor")
	   select sourceRows.id, sourceRows.parent_id, sourceRows.ccode
	   from  (select to_number(null,'99G999D9S') as parent_id,
					  1 as id,
					  'first parent' as ccode
			   union all
			   select to_number(null,'99G999D9S') as parent_id,
					  2 as id,
					  'second parent' as ccode
			   union all
			   select 1 as parent_id,
					  3 as id,
					  'first child' as ccode
			   union all
			   select 1 as parent_id,
					  4 as id,
					  'second child' as ccode
			   union all
			   select 2 as parent_id,
					  3 as id,
					  'third child' as ccode) sourceRows
		where  sourceRows.parent_id = pParent
		union all
		-- recursive part
		select sourceRows.id, sourceRows.parent_id, sourceRows.ccode
		from  (select to_number(null,'99G999D9S') as parent_id,
					  1 as id,
					  'first parent' as ccode
			   union all
			   select to_number(null,'99G999D9S') as parent_id,
					  2 as id,
					  'second parent' as ccode
			   union all
			   select 1 as parent_id,
					  3 as id,
					  'first child' as ccode
			   union all
			   select 1 as parent_id,
					  4 as id,
					  'second child' as ccode
			   union all
			   select 2 as parent_id,
					  3 as id,
					  'third child' as ccode) sourceRows
		inner join r
				on sourceRows.parent_id = r.id)
	select * from r;

    vResCursor record;
    i          integer := 0;  -- counter initially defined as 0
    
begin
    -- loop assignment for 3 iterations
    while i < 3 loop
        
        -- opening cursor
        open cRep (1);
        loop
            -- selecting values and assigning them to a variable
            fetch cRep into vResCursor;

			exit when not found;

            raise notice '%', vResCursor.ccode;
        end loop;
            

        close cRep;
        
        -- counter increment
        i := i + 1;
        
    end loop;

exception
    when others then
        raise exception 'Error is: %, %.', sqlstate, sqlerrm;
        
end $$;
```

***
Unnanmed cursors
====

Usually this type of cursor is called in a "for" loop. In the loop from the example, the variable "vRow" is used, which in structure corresponds to the selected query fields. In each pass through the loop, the rows of the selection are added to this variable. In the example, there will be a simple cursor for selecting department managers who were hired during a given period.
```sql
do $$declare
    vRow record;
begin
    -- loop from the first to the last row of the sample
    for vRow in (select *
                 from   information_schema.tables
                 where  table_schema = 'public'
                 order by table_name) loop
        

        raise notice 'Table % is in % catalog', vRow.table_name, vRow.table_catalog;
        
    end loop;

exception
    when others then
        raise exception 'Error is: %, %.', sqlstate, sqlerrm;
        
end $$;
```

***
Ref cursors
====

The scheme of working with Ref cursor looks like this:
OPEN unbound_cursor_variable[ [ NO ] SCROLL ] FOR EXECUTE query_string [USING expression [, ... ] ];
```sql
do $$declare
    vQueryCnt  varchar(255);   -- string calculation query text
	vCntQuery  integer;        -- number of rows in the table
	
	r    record;     -- record type variable
	cRep refcursor;  -- type cursor for dynamic SQL
begin
	-- selection of the names of the HR schema tables from the system table
    for r in select table_schema||'.'||table_name as fullName
             from   information_schema.tables
			 limit 5 loop
    	
		-- opens the Ref cursor for the collected query
		open cRep for execute format('select count(1) from %s', r.fullName);
        loop
            -- selection of the next query line
            fetch cRep into vCntQuery;

            exit when not found;

            raise notice 'В таблице % находится % строк.', lower(r.fullName), vCntQuery;
        end loop;
        

        close cRep;
        
    end loop;
    
exception
    when others then
        raise exception 'Error is: %, %.', sqlstate, sqlerrm;
        
end $$;
```

***
The task
====

You need to create an anonymous block in which you need to create a named query for a synthetic data set for departments with managers with a parameter to filter to a specific location.
The result of the work will be a line of displaying the text with data in which department which head is.