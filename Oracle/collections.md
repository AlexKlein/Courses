# Collections

A collection is an ordered group of elements of the same type. The PL/SQL supports three types of collections:
- nested tables;
- indexed tables;
- varray arrays (variable-size arrays).

A collection can be transferred as an input and/or output parameter to a PL/SQL block. You can use the collection to exchange with database tables and data columns, or to transfer a data column from a client application to a stored procedure or vice versa.
To create a collection, define the collection type and declare a variable of this type. The type definition is performed in the declarations section of a PL/SQL block.
Consider the most common collection option - nested tables. A nested table can be viewed as a one-dimensional array, in which the indexes are the values of the integer type in the range from 1 to 2147483647. The nested table can have empty elements that appear after they are deleted by the built-in DELETE procedure. A nested table can dynamically grow.

The following are descriptions of the built-in functions used to work with collections:
- EXISTS(n).
- COUNT.
- LIMIT.
- DELETE(m,n).
- FIRST.
- LAST.
- PRIOR(n).
- NEXT(n)L
- EXTEND(n,i).
- TRIM(n).

***
Oracle Data Cartridge Interface
====

In the first example, we will use the ODCI (Oracle Data Cartridge Interface) collection into which the ID of the US locations will be added.
The SYS.ODCINumberList collection is a PL/SQL table with one column. The advantage of these collections is that you can make queries from them by wrapping them in a table() function.
This collection will be populated by calling the named cursor in the "for" loop.
Next, an implicit cursor is called that selects the names of the departments located in the United States. The result of the program will display the names of the departments.
```sql
declare
    -- selection of location ID list in USA
    cursor cLocation
      is
    select location_id 
    from   hr.locations
    where  country_id = 'US';
    
    vLocation SYS.ODCINumberList;  -- ID list of selected locations
    
begin
    -- declaration of an empty collection for locations
    vLocation := SYS.ODCINumberList();
    
    -- call in the "for" loop to a named query
    for r in cLocation loop
        -- checking non-empty values for writing
        if r.location_id is not null then
            -- add one empty item to the end of the collection
            vLocation.extend();
            -- writing to the last item in the location ID collection
            vLocation(vLocation.last) := r.location_id;
        end if;
        
    end loop;
    
    -- selection of department names in USA locations with an unnamed cursor
    for r in (select department_name
              from   hr.departments
              where  location_id in (select column_value 
                                     from   table(vLocation))
              order by location_id,
                       department_name) loop
    
        -- display of department name
        dbms_output.put_line('Department: '||r.department_name);
    
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
Type objects
====

In the second example, to create a PL/SQL table of a certain structure, consider creating a record type (it can also be %rowtype), then based on this record type, you can specify a table type indexed by a numeric value and declare a variable of this table type.
In the collection, you can write data in batches using the bulk collect construction, which can be used to set the limit of rows inserted at a time.
Further, four passes through the collection are implemented in different ways to demonstrate options for working with data in the collection.
It is very important to remember that you can loop-the-loop forever, so you need to pay attention to the elements of the exit condition of the loop, for example, reset the counter used several times in the program.
```sql
declare
    -- record type
    type recAttrs is record (depName  varchar2(255),
                             empName  varchar2(255),
                             hireDate date,
                             salary   number,
                             country  varchar2(255));
    -- table type based on record type
    type tabAttrs is table of recAttrs index by pls_integer;
    
    vTabAttrs tabAttrs;     -- PL/SQL table
    i         number := 0;  -- counter
    
    -- cursor for departments in Seattle
    cursor cDepartment
      is
    select dep.department_name,
           emp.first_name||' '||emp.last_name as employee_name,
           emp.hire_date,
           emp.salary,
           loc.country_id
    from   hr.departments dep
    inner join hr.employees emp
            on emp.employee_id = dep.manager_id
    inner join hr.locations loc
            on loc.location_id = dep.location_id
    where  loc.city = 'Seattle';
begin
    open cDepartment;
    
    loop
        exit when cDepartment%notfound;
        
        -- writing values to a collection of 10,000 rows at a time
        fetch cDepartment bulk collect into vTabAttrs limit 10000;
        
    end loop;

    close cDepartment;
    
    -- selection of data from PL/SQL table in a loop with a condition on the number of rows
    while i < vTabAttrs.count loop
        -- increase counter
        i := i + 1;

        dbms_output.put_line('№1 Department: '||vTabAttrs(i).depName);
        
    end loop;

    begin
        -- reset counter
        i := 1;
        -- selection of data from PL/SQL table in a loop with the condition that the next row exists
        while vTabAttrs.next(i) is not null loop
            
            dbms_output.put_line('№2 Department: '||vTabAttrs(i).depName);
            
            i := i + 1;
        end loop;
        
        dbms_output.put_line('№3 Department: '||vTabAttrs(i).depName);
        
    exception
        when collection_is_null then
            dbms_output.put_line('Ошибка '||sqlerrm);
        when no_data_found then
            dbms_output.put_line('Ошибка '||sqlerrm);
    end;
    
    -- reset counter
    i := 0;
    -- selection of data from a PL / SQL table in a loop with the condition that the row number is not equal to the number of the last row
    while i != vTabAttrs.last loop

        i := i + 1;
        
        dbms_output.put_line('№4 Department: '||vTabAttrs(i).depName);
        
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
Passing a collection parameter
====

The following example shows how you can return data from a procedure through a parameter, while the output parameter will be a collection.
```sql
create or replace procedure hr.cityList (pCountry in  varchar2,
                                         pCities  out SYS.ODCIVarchar2List)
as
    -- data cursor by department in the country selected by
    cursor cCities
      is
    select distinct
           loc.city
    from   hr.departments dep
    inner join hr.locations loc
            on loc.location_id = dep.location_id
    where  loc.country_id = pCountry;
begin
    
    open cCities;
    
	fetch cCities bulk collect into pCities limit 10000;
    
	close cCities;
       
exception
    when others then
        dbms_output.put_line('Error '  ||chr(10)||
        dbms_utility.format_error_stack||
        dbms_utility.format_error_backtrace());
end;
/
```

To call this procedure, I wrote an anonymous block that displays a city line by line from a given country
```sql
declare
    pCities SYS.ODCIVarchar2List;  -- city collection
begin
    -- procedure call with passing country parameter
    hr.cityList ('US',
                 pCities);
                        
    -- loop according to the list of cities
    for r in (select column_value
              from   table(pCities)) loop
        
        dbms_output.put_line(r.column_value);
    end loop;
end;
/
```

***
The task
====

Create a procedure (and a call block of this procedure) that takes the parameters of the start and end dates of hiring employees, the country of employment and returns a list of concatenated strings. Name || Last Name || City || salary in the form of a collection.