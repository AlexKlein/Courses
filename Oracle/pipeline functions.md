# Pipeline functions

Often it is required to perform data transformations using PL/SQL code with the ability to access this data in an sql query. To do this, oracle uses table functions.
Table functions are functions that return data in the form of a collection, to which we can refer to the from section of the query, as if this collection were a relational table. The collection is converted into a relational dataset using the "table()" function.
However, such functions have one drawback, since they first completely fill the collection, and only then this collection returns to the calling processing. Each such collection is stored in memory and in high-load systems, this can be a problem. Also, in the calling processing, the idle time happens at the time of filling the collection. To solve this drawback are called table pipeline functions.
Pipeline functions are called table functions that return data as a collection, but do it asynchronously, that is, one collection entry is received and this entry is immediately given to the calling code in which it is immediately processed. In this case, the memory is saved, idle time is eliminated.

In the example, a report is created with the fields employee, department, city and salary, which is included in the specified range.
```sql
create or replace package hr.employee_report
/******************************* HISTORY *******************************************\
Date        Author           ID       Description
----------  ---------------  -------- -----------------------------------------------
05.12.2018  Klein A.M.      [000000]  Build Package.
\******************************* HISTORY *******************************************/
is
    -- report row type
    type report_str is record (emp_name        varchar2(255),
                               department_name varchar2(255),
                               salary          number,
                               city            varchar2(255));
    -- report collection type
    type report_tab is table of report_str;
        
    -- procedures
    procedure my_exception;
    -- functions
    function get_report (pStartSal number,
                         pEndSal   number) return report_tab pipelined;
    
end employee_report;
/
create or replace package body hr.employee_report
/******************************* HISTORY *******************************************\
Date        Author            ID       Description
----------  ---------------  -------- -----------------------------------------------
05.12.2018  Klein A.M.      [000000]  Build Package.
\******************************* HISTORY *******************************************/
is
-- exception handling procedure
    procedure my_exception
      is
    begin
        dbms_output.put_line('Error '  ||chr(10)||
        dbms_utility.format_error_stack||chr(10)||
        dbms_utility.format_error_backtrace());

    end my_exception;

-- employee salary report function
    function get_report (pStartSal number,
                         pEndSal   number) return report_tab pipelined
          is
        report_rec report_str;  -- report line
    begin
        
        -- data selection
        for rec in (select emp.first_name||' '||emp.last_name as emp_name,
                           dep.department_name,
                           emp.salary,
                           loc.city
                    from   hr.employees emp
                    inner join hr.departments dep
                            on emp.department_id = dep.department_id
                    inner join hr.locations loc
                            on dep.location_id = loc.location_id
                    where  emp.salary between pStartSal and pEndSal
                    order by loc.city,
                             dep.department_name,
                             emp.first_name||' '||emp.last_name,
                             emp.salary desc) loop
            -- clearing the data of the previous sampling line
            report_rec := null;
            -- data record of the current sampling line
            report_rec.emp_name        := rec.emp_name;
            report_rec.department_name := rec.department_name;
            report_rec.salary          := rec.salary;
            report_rec.city            := rec.city;
            
            -- data transfer to the call block
            pipe row (report_rec);
        end loop;
        
    exception
        when others then
            my_exception;
            
    end get_report;
   
end employee_report;
/
```

***
Function calls
====

```sql
select *
from   table(hr.employee_report.get_report(8000,9000));
/
```

***
The task
====

It is necessary to make a pipeline function that creates a report on the employees in a particular department. Accordingly, the filter for the function will be the department id, and the fields that the function will return:
• employee_id;
• first_name;
• last_name;
• email;
• phone_number;
• salary;
• salary_recom;
• department_id;
• department_name;
• city.