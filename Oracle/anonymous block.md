***
Anonymous block
====

PL / SQL is a block structure, the scheme of which is presented below:
```sql
[ <<label_name>> ] - Block label
[DECLARE]          - Declaration section
BEGIN              - Body block

[EXCEPTION]        - Exception handlers
END [label_name];
```

A PL / SQL block can contain up to four sections, but only one of them is required.
- Title. Used only in named blocks, determines the method of calling a named block or program. Not required.
- Section ads. It contains descriptions of variables, cursors and nested blocks referenced in the executable section and the exception section. Not required.
- Executable section. Commands executed by the PL / SQL kernel while the application is running. Required.
- Section exceptions. Handles exceptions (warnings and errors). Not required.

For example, I will write an anonymous block (there is no heading section) in which I will declare one numeric variable and put in it the average salary in the IT department:
```sql
declare             -- variable block declaration
    avgSal number;  -- variable of average salary
begin
    select avg(salary) as avg_sal  -- aggregate function of calculating the average value for the salary field
    into   avgSal                  -- operator assigning the result of a query to a variable
    from   hr.employees            -- the table from which the selection is
    where  department_id in        -- filter departments list from subquery
                            (select department_id             -- department ID selection
                             from   hr.departments            -- the table from which the selection is
                             where  department_name = 'IT');  -- filter by department name
end;
/
```

***
dbms_output.put_line
====

One of the most common methods of debugging is to display text on the screen, for convenience, they often use the concatenation of static and dynamic texts. In the resulting anonymous block, I will add a message to the user through the standard Oracle text output package:
```sql
declare
    avgSal number;
begin
    select avg(salary) as avg_sal
    into   avgSal
    from   hr.employees
    where  department_id in (select department_id
                             from   hr.departments
                             where  department_name = 'IT');
    dbms_output.put_line('The average salary of IT staff is: '||
                         avgSal||' $ USA');  -- text output to the screen after concatenation
end;
/
```