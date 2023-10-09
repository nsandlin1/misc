DROP DATABASE IF EXISTS finalproj;
CREATE DATABASE finalproj;
USE finalproj;

CREATE TABLE Disaster (
    disasterID INT PRIMARY KEY AUTO_INCREMENT,
    disasterName varchar(30) NOT NULL,
    disasterRatingScale varchar(30) NOT NULL,
    disasterRatingValue decimal(10,3) NOT NULL   -- Don't really know what scales will be used
);                                               -- and therefore a bound on this is undecided.

CREATE TABLE Employee (
    employeeID INT PRIMARY KEY AUTO_INCREMENT,
    employeeSSN INT,
    employeeFirstName varchar(30),
    employeeLastName varchar(30)
);

CREATE TABLE Branch (
    branchID INT PRIMARY KEY AUTO_INCREMENT,
    branchName varchar(30),
    branchLocation varchar(40),
    branchPerview varchar(200),
    branchHeadID INT,
    FOREIGN KEY (branchHeadID) REFERENCES Employee(employeeID) ON DELETE SET NULL,
    UNIQUE (branchName, branchLocation)
);

CREATE TABLE Department (
    departmentID INT PRIMARY KEY AUTO_INCREMENT,
    departmentBudget decimal(15,2),
    parentBranchID INT,
    departmentManagerID INT,
    FOREIGN KEY (departmentManagerID) REFERENCES Employee(employeeID) ON DELETE SET NULL,
    FOREIGN KEY (parentBranchID) REFERENCES Branch(branchID) ON DELETE CASCADE
);

CREATE TABLE WorksFor (
    departmentID INT,
    employeeID INT,
    PRIMARY KEY (departmentID, employeeID),
    FOREIGN KEY (departmentID) REFERENCES Department(departmentID) ON DELETE CASCADE,
    FOREIGN KEY (employeeID) REFERENCES Employee(employeeID) ON DELETE CASCADE
);

-- Have a view for the hours worked.
CREATE TABLE Project (
    projectID INT PRIMARY KEY AUTO_INCREMENT,
    projectedCost decimal(15,2),
    departmentID INT NOT NULL,
    disasterID INT NOT NULL,
    FOREIGN KEY (departmentID) REFERENCES Department(departmentID) ON DELETE CASCADE,
    FOREIGN KEY (disasterID) REFERENCES Disaster(disasterID) ON DELETE CASCADE
);

-- Record hours worked on project by department for use in
-- deriving the hours-worked attribute of project.
CREATE TABLE HoursWorked(
    projectID INT AUTO_INCREMENT,
    timeStart DATETIME,
    timeStop DATETIME,
    PRIMARY KEY (projectID, timeStart, timeStop),
    FOREIGN KEY (projectID) REFERENCES Project(projectID) ON DELETE CASCADE
);

CREATE VIEW PROJECT_HOURS_VIEW AS
    SELECT projectID, SUM(dateDifference) AS totalDateDifference
    FROM (SELECT projectID, DATEDIFF(timeStop, timeStart) AS dateDifference
          FROM HoursWorked) AS S1
    GROUP BY projectID;

DELIMITER $$
CREATE TRIGGER BUDGET_CONSTRAINT
BEFORE INSERT ON Project
FOR EACH ROW
BEGIN
    DECLARE ERR_MSG varchar(200);
    IF (NEW.projectedCost > (SELECT d.departmentBudget FROM Department d WHERE NEW.departmentID = d.departmentID))
    THEN
        SET ERR_MSG = 'Projected cost is over department budget.';
        signal sqlstate '45000' set message_text = ERR_MSG;
    END IF;
END
$$
DELIMITER ;

INSERT INTO Disaster(disasterName, disasterRatingScale, disasterRatingValue) VALUES
    ('Earthquake', 'Richter', 3.5),
    ('Tsunami', 'TIS', 6.2),
    ('Earthquake', 'Richter', 3.4);

INSERT INTO Branch(branchName, branchLocation, branchPerview) VALUES
    ("The Super Branch", "Hipster, OR", "Giving hippies needles"),
    ("The Other Branch", "Pontiac Chicago", "Flashin' Rims");

INSERT INTO Department(departmentBudget, parentBranchID) VALUES
    (16000.00, 1),
    (0.00, 1),
    (100000.13, 2);

INSERT INTO Employee(employeeSSN, employeeFirstName, employeeLastName) VALUES
    (123456789, "James", "Sandlin"),
    (987654321, "Novi", "Sandlin"),
    (192837465, "Nick", "Landry");

-- Set branch heads
UPDATE Branch SET branchHeadID = 1 WHERE branchID = 1;
UPDATE Branch SET branchHeadID = 3 WHERE branchID = 2;

-- Set department mangers
UPDATE Department SET departmentManagerID = 2 WHERE departmentID = 1;

INSERT INTO Project(projectedCost, departmentID, disasterID) VALUES
    (320.39, 3, 3),
    (0, 1, 1);

INSERT INTO HoursWorked VALUES
    (1, "2020-01-01 12:00:00", "2020-01-24 17:20:05"),
    (1, "2020-03-28 09:00:30", "2021-05-4 12:00:00"),
    (2, "2020-06-14 13:00:00", "2021-11-19 16:00:03");

INSERT INTO WorksFor VALUES
    (1, 1),
    (1, 2),
    (3, 3);

-- INSERT INTO Project VALUES (3, 16000.01, 1, 3); -- This will throw error due to trigger overbudget
