% Domain
student(louis; mollie; onyx; ryan; tiffany; yoshio).
year(1921; 1922; 1923; 1924).

% For each student, test if they can be assigned to 1921
% We'll run the solver once for each student, but need to encode all in one file.
% Instead, use a choice rule to pick one student as the "test" candidate.

% Pick exactly one student to test for being at 1921
{test_student(S)} :- student(S).
% Exactly one test student
:- not 1 { test_student(S) : student(S) } 1.

% If test_student(S), then S is assigned to 1921
assigned(S, 1921) :- test_student(S).

% Assignment: each year gets exactly one student
1 { assigned(S, Y) : student(S) } 1 :- year(Y).
:- assigned(S, Y1), assigned(S, Y2), Y1 != Y2.

% Condition 1: Only Louis or Tiffany can be assigned to 1923
:- assigned(S, 1923), S != louis, S != tiffany.

% Condition 2: If Mollie is assigned, she must be 1921 or 1922
:- assigned(mollie, Y), Y != 1921, Y != 1922.

% Helper: a student is assigned to the project
assigned_to_project(S) :- assigned(S, _).

% Condition 3: If Tiffany is assigned, then Ryan must be assigned
:- assigned_to_project(tiffany), not assigned_to_project(ryan).

% Condition 4: If Ryan is assigned, then Onyx must be assigned
:- assigned_to_project(ryan), not assigned_to_project(onyx).

% Condition 4 continued: Onyx must be assigned to the year immediately prior to Ryan's
:- assigned(ryan, Y), assigned(onyx, Y2), Y2 != Y - 1.

% A student is feasible at 1921 if the model is satisfiable with test_student(S)
feasible_1921(S) :- test_student(S).

% Now count feasible students (this will be per model, but only one test student per model)
% We need a different approach to count across all models.

% Instead, let's collect which students are feasible via a different strategy.
% We can use #count over all feasible students.

% Actually, in each model we have exactly one feasible student (the test student).
% The number of models with feasible students tells us the answer.
% But we need to count how many distinct students can be at 1921.

% Let me use a different approach: use #minimize to explore all possibilities
% and then collect the results.

% Let's just enumerate test_student and see which ones give satisfiable.

#show test_student/1.
#show feasible_1921/1.