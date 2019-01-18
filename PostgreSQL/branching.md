# Branching

***
if-then-else
====

The if-then-else operator is used to execute some code under the condition of truth. In the most general form (elsif blocks can be an unlimited number), the scheme looks like this:
```sql
if (some condition is true) then
-- the condition is fair, do it.
elsif (another fair condition) then
-- the condition is fair, do it.
else -- conditions are not met
-- execute default code.
end if; -- end of conditional statement.
```

Let us consider, for example, two simple blocks, the first with a comparison of the result of the calculation:
```sql
do $$declare
    checkSum float;  -- the result of calculating the sum of two constants
begin
    -- calculating the sum of two constants and assigning the result to a variable
    select 10+10
    into   checkSum;
    
    -- checking for equality of the result of a calculation and a constant
    if checkSum = 20 then
        -- display on the screen of the passage of the test
        raise notice 'Passed';
    else
        -- displaying a message about not passing the test
        raise notice 'Not passed';
    end if;
end $$;
```

and second with an expression test
```sql
do $$declare
    -- variable declaration and value assignment
    сheckStatement boolean := true;  -- the expression is initially true
begin
    -- checking the state of the expression
    if сheckStatement then
        -- display of the message about the truth of the expression
        raise notice 'True';
    else
        -- display of the message about the false of the expression
        raise notice 'False';
    end if;
end $$;
```

***
The task
====

It is necessary to make the function of recalculation of parts of an apple for each participant of division. The function takes as input a numeric parameter for the number of apples and returns the numerical result of the share of each participant. The number of participants is determined by a random number using the select floor(random()*(b-a+1))+a;. At the same time, participants must be from -5 to +5 whole people, so the rounding function is used and the minimum and maximum limits are set for the random number selection function select floor(random()*(5-(-5)+1))+(-5).
In the function, you need to check the result for comparability with reality. For example, the number of apple fractions should not be a negative number.