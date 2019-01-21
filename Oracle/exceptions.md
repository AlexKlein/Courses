# Error processing

***
Exceptions
====

In case of an error, the PL / SQL block completes urgently, but in order for the program not to be interrupted, there is an exception handling.
Some exceptions are predefined, such as:
ACCESS_INTO_NULL, CASE_NOT_FOUND, COLLECTION_IS_NULL, CURSOR_ALREADY_OPENED, DUP_VAL_ON_INDEX, INVALID_CURSOR, INVALID_NUMBER, NO_DATA_FOUND, PROGRAM_ERROR, ROWTYPE_MISMATCH, STORAGE_ERROR, SUBSCRIPT_BEYOND_COUNT, SUBSCRIPT_OUTSIDE_LIMIT, SYS_INVALID_ROWID, TOO_MANY_ROW, SVALUE_ERROR, ZERO_DIVIDE
In the following example, I will add handling of two frequently encountered exceptions.
In this block, the error will be caused by waiting for one value to assign it to a variable, but the query will produce a list of values ​​in the context of departments:
```sql
declare
    avgSal number;
begin
    select avg(salary) as avg_sal  -- aggregate function always returns at least one row
    into   avgSal
    from   hr.employees
    group by department_id;        -- grouping medium salary by department
    dbms_output.put_line('The average salary of an IT department is: '||
                         avgSal||' $ USA');

exception
    when too_many_rows then  -- exception handling when the query returns more rows than expected
        dbms_output.put_line('Too many rows');  -- display error message
    when no_data_found then  -- exception handling when the query does not return any row
        dbms_output.put_line('No rows found');  -- display error message
    when others then         -- handling all exceptions
        dbms_output.put_line('Error');          -- display error message
end;
/
```

When an error occurs, the block stops and displays the error one level higher, for example:
```sql
declare
    vRes number;  -- calculation result
begin  -- the first block
    begin  -- the second block
        
        -- calculating the sum and assigning the result to a variable
        select 2/0 
        into   vRes
        from   dual;

    end;

end;
/
```

When dividing by 0 within the structure of the second block "begin - end", the error will go to a higher level, to the first "begin - end".
Oracle DBMS defines 14 named exceptions plus the "others" exception for all errors, each exception places the program in a separate branch.
```sql
declare
    vRes number;
begin
    
    select 2/0 
    into   vRes
    from   dual;

exception  -- exception handling
    when zero_divide then  -- dividing by 0 exceptions
        -- displaying an error message with an error message
        dbms_output.put_line('Error '||sqlerrm);
 end;
/
```

You can get information about the error in different ways, for example, with the functions sqlerrm, sqlcode, but you can display the entire stack of error messages:
```sql
declare
    vRes number;
begin
    
    select 2/0 
    into   vRes
    from   dual;

exception
    when others then  -- exception for any error
        -- display the string "Error"
        dbms_output.put_line('Ошибка '  ||chr(10)||
        -- displaying the code and error message
        dbms_utility.format_error_stack||
        -- display of the line in which the error occurred
        dbms_utility.format_error_backtrace());
end;
/
```

***
User defined exceptions
====

In Oracle DBMS, you can do processing custom exceptions for branching a program or handling business logic errors.
```sql
declare
    vSalary number;     -- salary
    exCustom exception; -- custom exception declaration
    
    pragma exception_init(exCustom, -20001); -- setting the error number
begin
    select (10000*12*0.87*(-1)) as salary
    into   vSalary
    from   dual;
    
    -- negative pay check
    if vSalary < 0 then
        -- 
        raise_application_error(-20001,'Salary cannot be negative');
        -- option without additional message
        -- raise exCustom; 
    end if;
    
exception
    when exCustom then  -- user defined exception
        dbms_output.put_line(sqlerrm);
        begin
            -- salary recalculation with another parameters
            select 10000*12*0.87 as salary
            into   vSalary
            from   dual; 
        
            -- display recalculated salary
            dbms_output.put_line('Salary for the year is '||vSalary||'$');
            
        exception
            when others then
                dbms_output.put_line('Error '  ||chr(10)||
                dbms_utility.format_error_stack||
                dbms_utility.format_error_backtrace());
        end;
    when zero_divide then
        dbms_output.put_line('Error '||sqlerrm);
    when others then
        dbms_output.put_line('Error '  ||chr(10)||
        dbms_utility.format_error_stack||
        dbms_utility.format_error_backtrace());
end;
/
```

***
Function creation
====

I will make the named block from anonymous, for an example I will make function. The main difference between the procedure and the function is that the function always returns the value of the declared data type. For example, I pass a text parameter to the function, which I will use as the Y / N flag, and the function must return a numeric value. Also, the flag will fulfill the condition, if the flag is Y, then you need to calculate the average salary of the IT department, otherwise assign the value -1 to the average salary variable, return the static value -2 in case of errors.
I present the function "learning" in the hr scheme with a text parameter that returns a numeric value:
```sql
create or replace function hr.learning (pFlag varchar2) return number  -- function creation
is
    avgSal number;
begin
    -- check of the average salary calculation flag
    if pFlag = 'Y' then  -- use of the parameter in the test block
        select avg(salary) as avg_sal
        into   avgSal
        from   hr.employees
        where  department_id in (select department_id
                                 from   hr.departments
                                 where  department_name = 'IT');
    else
        avgSal := -1;    -- variable assignment
    end if;
    
    return avgSal;       -- return of function result
    
exception
    when too_many_rows then
        dbms_output.put_line('Too many rows');
        return -2;
    when no_data_found then
        dbms_output.put_line('No rows found');
        return -3;
    when others then
        dbms_output.put_line('Error');
        return -4;
end;
/
```

***
Variants of function calls
====

To call this function, I use an anonymous block. At the same time, it is necessary to remember that the function always returns some value, respectively, it is necessary to remember about the data types conformity.
```sql
begin
    dbms_output.put_line('The average salary of IT staff is: '||hr.learning('Y'));
end;
/
```

In addition to the anonymous block, the value from the function can be obtained by a simple query:
```sql
select 'The average salary of IT staff is: '||hr.learning('Y') as result 
from   dual;
```

***
The task
====

It is necessary to create a function and its call.
The function must take two numerical values of the parameters and count the bonus for the previous year.
The first parameter is salary.
The second parameter is the grade.

Formulas for calculating the bonus:
```
0-10 grade:
Salary * 12 * 0,08 * 1 * 1,3 * 0,87
from 11 grade and higher:
Salary * 12 * 0,15 * 1 * 1,3 * 0,87
```

For each branch of the solution, you need to write a message through the dbms_output package.
It is necessary to do the processing of embedded exceptional operations:
- invalid_number;
- value_error;
- zero_devide;
- others.