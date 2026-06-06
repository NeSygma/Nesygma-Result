% Exam Scheduling Problem
% =========================

% --- Domains ---
exam(E) :- E = "E1"; E = "E2"; E = "E3"; E = "E4"; E = "E5"; E = "E6".
student(S) :- S = "S1"; S = "S2"; S = "S3"; S = "S4".
room(R) :- R = "R1"; R = "R2".
slot(1..3).  % 3 time slots available

% --- Enrollment Facts ---
enrollment("S1", "E1"). enrollment("S1", "E3"). enrollment("S1", "E5").
enrollment("S2", "E1"). enrollment("S2", "E4"). enrollment("S2", "E6").
enrollment("S3", "E2"). enrollment("S3", "E3"). enrollment("S3", "E6").
enrollment("S4", "E2"). enrollment("S4", "E4"). enrollment("S4", "E5").

% --- Room Capacities ---
room_capacity("R1", 3).
room_capacity("R2", 3).

% --- Assignment Choice Rule ---
% Each exam must be assigned to exactly one slot and room
1 { assigned(E, S, R) : slot(S), room(R) } 1 :- exam(E).

% --- Constraint 1: No student conflicts ---
% A student cannot have two exams at the same time slot
:- enrollment(Student, E1), enrollment(Student, E2), E1 != E2,
   assigned(E1, Slot, _), assigned(E2, Slot, _).

% --- Constraint 2: Room capacity ---
% Count students enrolled in each exam and ensure it doesn't exceed room capacity
% For each exam-room assignment, count enrolled students
exam_student_count(E, R, Count) :-
    assigned(E, _, R),
    Count = #count{ Student : enrollment(Student, E) }.

% Room capacity constraint
:- exam_student_count(E, R, Count), room_capacity(R, Cap), Count > Cap.

% --- Constraint 3: Unique assignments (implicit in choice rule) ---
% Already enforced by "1 { ... } 1" choice rule

% --- Output: Schedule ---
schedule(E, Slot, Room) :- assigned(E, Slot, Room).

% --- Output: Conflicts Resolved ---
conflicts_resolved :- not conflict_exists.
conflict_exists :- violation.
violation :- enrollment(Student, E1), enrollment(Student, E2), E1 != E2,
             assigned(E1, Slot, _), assigned(E2, Slot, _).
violation :- exam_student_count(E, R, Count), room_capacity(R, Cap), Count > Cap.

% --- Output: Room Utilization ---
room_utilization(R, ExamCount) :-
    room(R),
    ExamCount = #count{ E : assigned(E, _, R) }.

% --- Show directives ---
#show schedule/3.
#show conflicts_resolved/0.
#show room_utilization/2.
#show assigned/3.