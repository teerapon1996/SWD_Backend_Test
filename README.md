# SWD Backend Test
## Solution for test

- Open your terminal and enter command ...
```
 python manage.py runserver
```
# This test have 2 part

## Part 1 

#### Convert number to thai word (logical_test.py)

```
python logical_test.py
```

#### Convert number to roman (logical_test_2.py)

```
python logical_test2.py
```
## Part 2 - School API 3 Endpoint

#### Test on terminal with command ... (test_api.py)

```
python test_api.py
```

## > OR Django Restframework Template

1. Student Score  

``` 
[GET] - student_score/<int:id>
``` 
- Click Link for test with Parameter > id = 2

Request <a href="http://localhost:8000/api/student_score/2/" target="_blank">GET Student Score</a>

2. Personnel Details

``` 
[GET] - personnel_details/<str:school_title>/
``` 

- Click Link for test with Parameter > school_title="Rose Garden School"

Request <a href="http://localhost:8000/api/personnel_details/Rose Garden School/" target="_blank">GET Personnel Details</a>

3. School Hierarchy

``` 
[GET] - school_hierarchy/
``` 

- Click Link for test School Hierarchy

Request <a href="http://localhost:8000/api/school_hierarchy/" target="_blank">GET Personnel Details</a>


# Thanks for the opportunity.
### Mr.Teerapon Meesuk (Developer)