% Define the years and students
year(1921). year(1922). year(1923). year(1924).
student(louis). student(mollie). student(onyx). student(ryan). student(tiffany). student(yoshio).

% Assign exactly one student to each year
1 { assigned(Year, Student) : student(Student) } 1 :- year(Year).

% Constraint 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(1923, Student), Student != louis, Student != tiffany.

% Constraint 2: If Mollie is assigned, she must be assigned to 1921 or 1922
:- assigned(Year, mollie), Year != 1921, Year != 1922.

% Constraint 3: If Tiffany is assigned, Ryan must be assigned
:- assigned(_, tiffany), not assigned(_, ryan).

% Constraint 4: If Ryan is assigned, Onyx must be assigned to the year immediately prior
:- assigned(RyanYear, ryan), not assigned(PriorYear, onyx),
   PriorYear = RyanYear - 1.

% Check if a student can be assigned to 1922 in any valid assignment
% We use a choice rule to allow checking all possibilities
{ can_be_assigned_to_1922(Student) } :- student(Student).

% For each student, if they are assigned to 1922 in a valid assignment, mark them as assignable
can_be_assigned_to_1922(Student) :- assigned(1922, Student).

% Ensure that the assignment is valid (all constraints are satisfied)
valid_assignment :- not constraint_violated.
constraint_violated :- assigned(1923, Student), Student != louis, Student != tiffany.
constraint_violated :- assigned(Year, mollie), Year != 1921, Year != 1922.
constraint_violated :- assigned(_, tiffany), not assigned(_, ryan).
constraint_violated :- assigned(RyanYear, ryan), not assigned(PriorYear, onyx), PriorYear = RyanYear - 1.

% If the assignment is valid and a student is assigned to 1922, they are assignable
% Now, derive the answer: the student who CANNOT be assigned to 1922

% The answer is the student for whom can_be_assigned_to_1922 is false in all valid assignments
% We map the answer to option/1 based on the logic below

% If Louis cannot be assigned to 1922 in any valid assignment, then option(a) is correct
option(a) :- student(louis), not can_be_assigned_to_1922(louis), valid_assignment.

% If Mollie cannot be assigned to 1922 in any valid assignment, then option(b) is correct
option(b) :- student(mollie), not can_be_assigned_to_1922(mollie), valid_assignment.

% If Onyx cannot be assigned to 1922 in any valid assignment, then option(c) is correct
option(c) :- student(onyx), not can_be_assigned_to_1922(onyx), valid_assignment.

% If Ryan cannot be assigned to 1922 in any valid assignment, then option(d) is correct
option(d) :- student(ryan), not can_be_assigned_to_1922(ryan), valid_assignment.

% If Yoshio cannot be assigned to 1922 in any valid assignment, then option(e) is correct
option(e) :- student(yoshio), not can_be_assigned_to_1922(yoshio), valid_assignment.

#show option/1.