# data_storage
Initialize the database, import data from excel to MySQL, PostgreSQL, Oracle

## main lib
- pandas
- toml
- logbook

## main function
1. Recursively search the specified path, find excel files and csv files

2. Recursively traverse all the sheets of excel and return the DataFrame. If there is a null value on the first line, it will drop it and crawl the second line is the table field, and so on.

3. Now tested, it can import Mysql/Postgresql/Oracle database. Thanks for all the pandas developers.

4. Take the sheet name as the table name.

5. But at some point, pandas to excel data to identify the error, or their own data problems, will be an error, such as timestamp object without translate attributes.
