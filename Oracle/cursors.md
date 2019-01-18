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

To work with the cursor, you can use the following attributes specified after the cursor name:
- %ISOPEN - returns TRUE if the cursor is open.
- %FOUND - determines whether a string is found that satisfies the condition.
- %NOTFOUND - returns TRUE if the string is not found.
- %ROWCOUNT - returns the current row number.

You can use this knowledge like this:
```sql
declare
    -- a simple cursor that returns two lines with one number in each
    cursor cRep
      is
    select 1 as num
    from   dual
    union all
    select 2 as num
    from   dual;
    
    vResCursor cRep%rowtype; -- cursor row type string
    
begin
    -- cursor opening
    open cRep;
    
    -- loop to select data from the cursor
    loop
        -- exit from the loop when there are no values left
        exit when cRep%notfound;
        
        -- writing values to variable
        fetch cRep into vResCursor;
        
        -- checking for the existence of a line in the cursor
        if not cRep%notfound then
            
            -- display data
            dbms_output.put_line('Num: '||vResCursor.num);
        
        end if;
      
    end loop;
            
    -- closing the cursor, freeing the memory
    close cRep;
end;
/
```

For greater flexibility of the program code, the cursor can be parameterized, and at the same time creating the result set, you can lock selectable rows. To do this, in the SELECT statement, you must specify the phrase FOR UPDATE.
The following example adds parameters to the cursor and changes the values ​​of the selected rows. Also, the query in the cursor is hierarchical, it highlights the condition of the first row for which there is no parent, and the condition of joining the parent rows with descendants. Sorting is carried out between the values ​​at the same level and in the same dependency.
In this example, a while loop is used, in which the condition for three passes inside the loop is specified.
```sql
declare
    -- selection of department employees with hierarchy
    cursor cRep (pDepartment varchar2) 
      is
    select dep.department_name,
           level,
           emp.first_name,
           emp.last_name 
    from   hr.employees emp
    inner join hr.departments dep
            on emp.department_id = dep.department_id 
    where  dep.department_name = pDepartment
    start with emp.manager_id is null
    connect by prior emp.employee_id = emp.manager_id
    order siblings by emp.department_id, 
                      emp.first_name||' '||emp.last_name;

    vResCursor cRep%rowtype; -- cursor row type string
    i          number := 0;  -- counter initially defined as 0
    
begin
    -- cycle assignment for 3 iterations
    while i < 3 loop
        
        -- opening cursor for IT department
        open cRep ('IT');
        loop
            -- exit from loop when no value is left
            exit when cRep%notfound;
            -- writing values to a collection
            fetch cRep into vResCursor;
                    
            -- outputting results if string is found
            if not cRep%notfound then
                -- variable update
                vResCursor.last_name := 'Mc' || vResCursor.last_name;
                -- display of modified text
                dbms_output.put_line('Pass №'||i||' Employee: '||vResCursor.first_name||' '||vResCursor.last_name ||', with hierarchy level '||vResCursor.level);
                
            end if;
              
        end loop;
            
        -- closing the cursor, freeing the memory
        close cRep;
        
        -- counter increment
        i := i + 1;
        
    end loop;

exception
    when others then
        dbms_output.put_line('Ошибка '  ||chr(10)||
        dbms_utility.format_error_stack||
        dbms_utility.format_error_backtrace());
        
end;
/
```

***
Unnanmed cursors
====

Usually this type of cursor is called in a "for" loop. In the loop from the example, the variable "vRow" is used, which in structure corresponds to the selected query fields. In each pass through the loop, the rows of the selection are added to this variable. In the example, there will be a simple cursor for selecting department managers who were hired during a given period.
```sql
declare
    vFromDate date;  -- the start date of selection
    vToDate   date;  -- the end date of selection
begin
    
    -- one of ways to define variables
    select date'2003-05-01' as vFromDate,
           date'2005-10-31' as vToDate
    into   vFromDate,
           vToDate
    from   dual;
    
    -- loop from the first to the last row of the selection
    for vRow in (select emp.first_name||' '||emp.last_name as manager_name,
                        dep.department_name,
                        emp.hire_date
                 from   hr.departments dep
                 inner join hr.employees emp
                         on dep.manager_id = emp.employee_id
                 where  hire_date between vFromDate and
                                          vToDate
                 order by dep.department_name) loop
        
        -- data output by department managers
        dbms_output.put_line('Department: '||vRow.department_name||'. Manager: '||vRow.manager_name||'. Hired at: '||vRow.hire_date);
        
    end loop;

exception
    when others then
        dbms_output.put_line('Error '  ||chr(10)||
        dbms_utility.format_error_stack||
        dbms_utility.format_error_backtrace());
        
end;
/
```

***
Ref cursors
====

The scheme of working with Ref cursor looks like this:
TYPE ref_type_name IS REF CURSOR [ RETURN return_type ];

If the RETURN option is not specified, then the cursor variable can be used more flexibly by referring to different queries that have different record types. However, using the RETURN option provides a higher level of reliability, allowing the PL / SQL compiler to check the compatibility of the cursor variable type with the query result type. The cursor variable cannot be stored in the database. You can use the attributes %FOUND, %NOTFOUND, %ISOPEN, and %ROWCOUNT for the cursor variable.
In the example below, an unnamed cursor is used to select table names from a system table with descriptions, then a query is assembled using the concatenation of static text and a dynamically changing table name. After that, the Ref cursor opens, which executes the query that is in the text variable. The result of the query is written to the variable and then displayed on the screen.
```sql
declare
    vTabName   varchar2(255);   -- table name
    vCntQuery  number;          -- number of rows in the table
    
    type curTyp is ref cursor;  -- type cursor for dynamic SQL
    cCursorCnt curTyp;          -- cursor for dynamic calculation of rows
    vQueryCnt  varchar2(255);   -- rows calculation query text
begin
    -- selection of the names of the HR schema tables from the system table
    for r in (select owner||'.'||table_name as fullName
              from   sys.all_tables
              where  owner = 'HR' and 
                     num_rows > 20
              order by table_name) loop
		-- concatenation the query
        vQueryCnt := 'select count(1) from ' || r.fullName;
        
        -- opens the Ref cursor for the collected query
        open cCursorCnt for vQueryCnt;
        
        loop
            -- selection of the next query row
            fetch cCursorCnt into vCntQuery;
            -- exit condition
            exit when cCursorCnt%notfound;
            
            -- checking that there is something in the cursor
            if not cCursorCnt%notfound then
                
                -- output user message
                dbms_output.put_line('There are '||vCntQuery||' rows in the table '||lower(r.fullName)||'.');
                
            end if;
        
        end loop;
        
        -- close cursor
        close cCursorCnt;
        
    end loop;
    
exception
    when others then
        dbms_output.put_line('Error '  ||chr(10)||
        dbms_utility.format_error_stack||
        dbms_utility.format_error_backtrace());
        
end;
/
```

***
The task
====

You need to create an anonymous block in which you need to create a named query to a list of departments (hr.departments) with a parameter to filter to a specific location (hr.locations). For each department (within the loop of selecting a named query), you need to select a department manager (hr.employees) and count the number of employees in this department (hr.employees). 
The result of the work will be a line of displaying the text with the data in which department which manager and how many people work in the department, not including this manager.