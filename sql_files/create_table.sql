DROP TABLE IF EXISTS employee;

CREATE TABLE employee (
    Id INT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Designation VARCHAR(50) NOT NULL,
    Salary DECIMAL(10, 2) NOT NULL
);