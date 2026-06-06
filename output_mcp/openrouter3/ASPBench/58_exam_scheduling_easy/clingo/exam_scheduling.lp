% Exam Scheduling Problem

% ===== DOMAIN DECLARATIONS =====
% Exams (use quoted strings for uppercase identifiers)
exam("E1"). exam("E2"). exam("E3"). exam("E4"). exam("E5"). exam("E6").

% Students
student("S1"). student("S2"). student("S3"). student("S4").

% Rooms with capacities
room("R1"). room("R2").
capacity("R1", 3). capacity("R2", 3).

% Time slots (3 slots available)
slot(1). slot(2). slot(3).

% Student enrollments
enrolled("S1", "E1"). enrolled("S1", "E3"). enrolled("S1", "E5").
enrolled("S2", "E1"). enrolled("S2", "E4"). enrolled("S2", "E6").
enrolled("S3", "E2"). enrolled("S3", "E3"). enrolled("S3", "E6").
enrolled("S4", "E2"). enrolled("S4", "E4"). enrolled("S4", "E5").

% ===== SCHEDULE GENERATION =====
% Each exam must be assigned to exactly one time slot and room
1 { schedule(E, T, R) : slot(T), room(R) } 1 :- exam(E).

% ===== CONFLICT DETECTION =====
% Helper: Student has exam at time T
student_exam_time(S, T) :- enrolled(S, E), schedule(E, T, _).

% ===== CONSTRAINTS =====
% Constraint 1: No student conflicts (student cannot have two exams at same time)
% If a student has two different exams at the same time, it's a conflict
:- student_exam_time(S, T), enrolled(S, E1), enrolled(S, E2), E1 != E2, schedule(E1, T, _), schedule(E2, T, _).

% Constraint 2: Room capacity - count students in each exam
% For each exam, count enrolled students and ensure it doesn't exceed room capacity
exam_student_count(E, N) :- exam(E), N = #count{S : enrolled(S, E)}.
:- schedule(E, T, R), exam_student_count(E, N), capacity(R, C), N > C.

% Constraint 3: Each exam appears exactly once (already enforced by choice rule)

% ===== OBJECTIVE: VALID SCHEDULE =====
% A schedule is valid if all constraints are satisfied
valid_schedule :- exam(E), schedule(E, _, _).  % All exams scheduled

% ===== OUTPUT =====
% Show the schedule
#show schedule/3.
#show valid_schedule/0.

% Additional output for clarity
#show exam_student_count/2.