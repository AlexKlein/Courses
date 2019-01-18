# Data type CLOB

***
dbms_lob
====

The data type CLOB (character large object) can be up to 2,147,483,647 characters. CLOB is used to store data in Unicode and suitable for storing large documents in any character set.
Work with large objects is carried out using the dbms_lob package.

Let us consider an example in which we will assemble departments in which there are employees with a salary of more than 10,000 in one CLOB and display it to the user.
```sql
declare
    result clob;  -- character large object
    
    -- selection of departments
    cursor get_departments
        is
    select distinct dep.department_name 
    from   hr.employees emp
    inner join hr.departments dep
            on dep.department_id = emp.department_id
    where  emp.salary > 10000
    order by dep.department_name;
    
begin
    -- variable initialization
    result := empty_clob();
    -- allocating temporary memory for a variable
    dbms_lob.createtemporary(result,true);
    
    -- selection of data from the table with the departments
    for i in get_departments loop
        -- writing a text file from below
        dbms_lob.append(result, i.department_name||chr(10));
    
    end loop;

    -- displaying the result on the screen
    dbms_output.put_line(result);
    
    -- clear temporary memory
    dbms_lob.freetemporary(result);
    
exception
    when others then
        dbms_lob.append(result, 'Something was wrong...');
        dbms_output.put_line(result);
        dbms_lob.freetemporary(result);
        
end;
/
```

The following example creates two lists that are subsequently compared and the result of the comparison is displayed to the user on the screen.
```sql
declare
    list12000 clob;    -- list of employees with a salary > 12000
    list8000  clob;    -- list of employees with a salary > 8000
    compare   number;  -- list comparison flag
    
    -- selection of employees with a salary > 12000
    cursor get_list12000
        is
    select listagg(first_name||' '||last_name, chr(10))
               within group (order by hire_date) as emp_list 
    from   hr.employees emp
    where  salary > 12000;
    
    -- selection of employees with a salary > 8000
    cursor get_list8000
        is
    select listagg(first_name||' '||last_name, chr(10))
               within group (order by hire_date) as emp_list 
    from   hr.employees emp
    where  salary > 8000;

begin
    -- variable initialization
    list12000 := empty_clob();
    list8000  := empty_clob();
    
    -- allocating temporary memory for a variable
    dbms_lob.createtemporary(list12000,true);
    dbms_lob.createtemporary(list8000, true);
    
    -- selection of data from the table
    for i in get_list12000 loop
        -- writing a text file from below
        dbms_lob.append(list12000, i.emp_list||chr(10));
    
    end loop;

    for i in get_list8000 loop
        -- writing a text file from below
        dbms_lob.append(list8000, i.emp_list||chr(10));
    
    end loop;
    
    -- comparison of two CLOB
    compare := dbms_lob.compare(list12000, list8000);
    
    -- output of the result of the difference in the lists
    if compare = 1 then
        dbms_output.put_line('They are different...');
    else
        dbms_output.put_line('They are not different...');
    end if;
    
    -- clear temporary memory
    dbms_lob.freetemporary(list12000);
    dbms_lob.freetemporary(list8000);
    
exception
    when others then
        dbms_lob.freetemporary(list12000);
        dbms_lob.freetemporary(list8000);
        
end;
```

***
The task
====

It is necessary to create a procedure that will take the country as two characters at the entrance, choose the departments that are in this country, collect this list in the CLOB and display it on the screen.