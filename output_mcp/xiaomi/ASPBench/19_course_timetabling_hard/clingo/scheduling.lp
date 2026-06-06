% ==================== DOMAINS ====================
course(0..7).
room(0..3).
time_slot(0..5).
teacher(0..4).
dept(sci). dept(hum). dept(eng).

% ==================== COURSE DATA ====================
course_teacher(0, 0). course_teacher(1, 0). course_teacher(2, 1).
course_teacher(3, 2). course_teacher(4, 3).
course_teacher(5, 4). course_teacher(6, 4). course_teacher(7, 4).

course_students(0, 30). course_students(1, 25). course_students(2, 40).
course_students(3, 50). course_students(4, 45).
course_students(5, 60). course_students(6, 55). course_students(7, 50).

course_dept(0, sci). course_dept(1, sci). course_dept(2, sci).
course_dept(3, hum). course_dept(4, hum).
course_dept(5, eng). course_dept(6, eng). course_dept(7, eng).

% ==================== ROOM DATA ====================
room_capacity(0, 60). room_capacity(1, 50).
room_capacity(2, 40). room_capacity(3, 30).

room_feature(0, projector). room_feature(1, projector).
room_feature(2, lab). room_feature(2, projector).

% ==================== TEACHER AVAILABILITY ====================
available(0, 0). available(0, 1). available(0, 2).
available(1, 2). available(1, 3). available(1, 4).
available(2, 0). available(2, 1). available(2, 4). available(2, 5).
available(3, 0). available(3, 2). available(3, 3). available(3, 5).
available(4, 1). available(4, 2). available(4, 3). available(4, 4). available(4, 5).

% ==================== ROOM REQUIREMENTS ====================
requires_feature(2, lab).
requires_feature(5, projector). requires_feature(6, projector). requires_feature(7, projector).

% ==================== PREREQUISITES ====================
prereq(0, 1).  % Physics I before Physics II
prereq(5, 6).  % Intro Programming before Data Structures
prereq(6, 7).  % Data Structures before Algorithms

% ==================== STUDENT CONFLICTS ====================
conflict(1, 4). conflict(4, 1).
conflict(2, 5). conflict(5, 2).

% ==================== DECISION VARIABLE ====================
% Each course assigned to exactly one (room, time_slot) pair
{ assigned(C, R, S) : room(R), time_slot(S) } 1 :- course(C).

% ==================== CONSTRAINTS ====================

% 1. Room Uniqueness: No two courses in same room at same time
:- assigned(C1, R, S), assigned(C2, R, S), C1 < C2.

% 2. Teacher Uniqueness: No two courses by same teacher at same time
:- assigned(C1, R1, S), assigned(C2, R2, S), C1 < C2,
   course_teacher(C1, T), course_teacher(C2, T).

% 3. Room Capacity: Course students <= room capacity
:- assigned(C, R, S), course_students(C, N), room_capacity(R, Cap), N > Cap.

% 4. Teacher Availability: Course scheduled only when teacher available
:- assigned(C, R, S), course_teacher(C, T), not available(T, S).

% 5. Room Features: Course requiring feature must be in room with feature
:- assigned(C, R, S), requires_feature(C, F), not room_feature(R, F).

% 6. Prerequisites: Prereq course must be in strictly earlier slot
:- assigned(C1, R1, S1), assigned(C2, R2, S2), prereq(C1, C2), S1 >= S2.

% 7. Student Conflicts: Conflicting courses cannot be at same time
:- assigned(C1, R1, S), assigned(C2, R2, S), conflict(C1, C2).

% 8. Global Evening Limit: Max 2 courses in time slot 5
:- 3 { assigned(C, R, 5) : course(C), room(R) }.

% ==================== OBJECTIVE ====================
% Count adjacent same-department pairs (consecutive time slots)
% A pair (C1, C2) is adjacent-same-dept if:
%   - They are in consecutive time slots (S2 = S1 + 1)
%   - They share the same department

adjacent_same_dept(C1, C2) :-
    assigned(C1, R1, S1), assigned(C2, R2, S2),
    S2 = S1 + 1,
    course_dept(C1, D), course_dept(C2, D),
    C1 != C2.

cost(N) :- N = #count { C1, C2 : adjacent_same_dept(C1, C2) }.

#minimize { N, N : cost(N) }.

% ==================== OUTPUT ====================
#show assigned/3.
#show cost/1.