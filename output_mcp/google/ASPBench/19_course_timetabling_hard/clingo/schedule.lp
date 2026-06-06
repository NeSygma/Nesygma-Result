% --- Data ---
course(0, 0, 30, sci).
course(1, 0, 25, sci).
course(2, 1, 40, sci).
course(3, 2, 50, hum).
course(4, 3, 45, hum).
course(5, 4, 60, eng).
course(6, 4, 55, eng).
course(7, 4, 50, eng).

room(0, 60). room_feature(0, projector).
room(1, 50). room_feature(1, projector).
room(2, 40). room_feature(2, lab). room_feature(2, projector).
room(3, 30).

time_slot(0..5).

teacher_availability(0, 0). teacher_availability(0, 1). teacher_availability(0, 2).
teacher_availability(1, 2). teacher_availability(1, 3). teacher_availability(1, 4).
teacher_availability(2, 0). teacher_availability(2, 1). teacher_availability(2, 4). teacher_availability(2, 5).
teacher_availability(3, 0). teacher_availability(3, 2). teacher_availability(3, 3). teacher_availability(3, 5).
teacher_availability(4, 1). teacher_availability(4, 2). teacher_availability(4, 3). teacher_availability(4, 4). teacher_availability(4, 5).

course_requirement(2, lab).
course_requirement(5, projector). course_requirement(6, projector). course_requirement(7, projector).

prerequisite(0, 1).
prerequisite(5, 6).
prerequisite(6, 7).

student_conflict(1, 4).
student_conflict(2, 5).

% --- Logic ---
{ assign(C, R, S) : room(R, _), time_slot(S) } 1 :- course(C, _, _, _).

% Ensure every course is assigned
:- course(C, _, _, _), not assign(C, _, _).

% Room Uniqueness
:- assign(C1, R, S), assign(C2, R, S), C1 != C2.

% Teacher Uniqueness
:- assign(C1, R1, S), assign(C2, R2, S), course(C1, T, _, _), course(C2, T, _, _), C1 != C2.

% Room Capacity
:- assign(C, R, S), course(C, _, Students, _), room(R, Capacity), Students > Capacity.

% Teacher Availability
:- assign(C, _, S), course(C, T, _, _), not teacher_availability(T, S).

% Room Features
:- assign(C, R, _), course_requirement(C, F), not room_feature(R, F).

% Prerequisites
:- prerequisite(C1, C2), assign(C1, _, S1), assign(C2, _, S2), S1 >= S2.

% Student Conflicts
:- student_conflict(C1, C2), assign(C1, _, S), assign(C2, _, S).

% Global Evening Limit
:- #count { C : assign(C, _, 5) } > 2.

% Objective: Minimize adjacent same-department course pairs
same_dept(C1, C2) :- course(C1, _, _, D), course(C2, _, _, D), C1 < C2.
consecutive(S1, S2) :- time_slot(S1), time_slot(S2), S2 = S1 + 1.

adjacent_same_dept(C1, C2) :- same_dept(C1, C2), assign(C1, _, S1), assign(C2, _, S2), consecutive(S1, S2).
adjacent_same_dept(C1, C2) :- same_dept(C1, C2), assign(C1, _, S2), assign(C2, _, S1), consecutive(S1, S2).

#minimize { 1, C1, C2 : adjacent_same_dept(C1, C2) }.

#show assign/3.