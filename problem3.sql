/* write your SQL query below */

SELECT  FirstName,
        LastName,
        ReportsTo,
        Position,
        Age,
        CASE WHEN ReportsTo = 'Jenny Richards' THEN 'CEO'
        ELSE 'None'
        END AS 'Boss Title'
FROM maintable_S5MSV
Where (ReportsTo = 'Jenny Richards' OR ReportsTo Is Null)
Order by Age
