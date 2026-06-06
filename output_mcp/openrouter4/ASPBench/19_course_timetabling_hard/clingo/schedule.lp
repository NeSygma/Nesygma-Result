%%% DOMAIN FACTS %%%

% Courses (ID)
course(0..7).

% Course attributes: (course_id, students, department)
course_attr(0, 30, sci).
course_attr(1, 25, sci).
course_attr(2, 40, sci).
course_attr(3, 50, hum).
course_attr(4, 45, hum).
course_attr(5, 60, eng).
course_attr(6, 55, eng).
course_attr(7, 50, eng).

% Course teacher: (course_id, teacher_id)
course_teacher(0, 0).
course_teacher(1, 0).
course_teacher(2, 1).
course_teacher(3, 2).
course_teacher(4, 3).
course_teacher(5, 4).
course_teacher(6, 4).
course_teacher(7, 4).

% Rooms
room(0..3).

% Room capacity: (room_id, capacity)
room_capacity(0, 60).
room_capacity(1, 50).
room_capacity(2, 40).
room_capacity(3, 30).

% Room features: (room_id, feature)
room_feature(0, projector).
room_feature(1, projector).
room_feature(2, lab).
room_feature(2, projector).
% room 3 has no features

% Time slots
time(0..5).

% Teacher availability: (teacher_id, time_slot)
teacher_available(0, 0).
teacher_available(0, 1).
teacher_available(0, 2).
teacher_available(1, 2).
teacher_available(1, 3).
teacher_available(1, 4).
teacher_available(2, 0).
teacher_available(2, 1).
teacher_available(2, 4).
teacher_available(2, 5).
teacher_available(3, 0).
teacher_available(3, 2).
teacher_available(3, 3).
teacher_available(3, 5).
teacher_available(4, 1).
teacher_available(4, 2).
teacher_available(4, 3).
teacher_available(4, 4).
teacher_available(4, 5).

% Room feature requirements: (course_id, required_feature)
requires_feature(2, lab).
requires_feature(5, projector).
requires_feature(6, projector).
requires_feature(7, projector).

% Prerequisites: (course_id_before, course_id_after)
prerequisite(0, 1).   % Physics I before Physics II
prerequisite(5, 6).   % Intro Programming before Data Structures
prerequisite(6, 7).   % Data Structures before Algorithms

% Student conflicts: (course_id1, course_id2) - symmetric
conflict(1, 4).
conflict(4, 1).
conflict(2, 5).
conflict(5, 2).

%%% DECISION VARIABLES %%%

% Each course assigned to exactly one (room, time_slot) pair
{ assign(C, R, T) : room(R), time(T) } = 1 :- course(C).

%%% CONSTRAINTS %%%

% 2. Room Uniqueness: A room cannot host more than one course at the same time
:- assign(C1, R, T), assign(C2, R, T), C1 != C2.

% 3. Teacher Uniqueness: A teacher cannot teach two courses at the same time
:- assign(C1, _, T), assign(C2, _, T), C1 != C2,
   course_teacher(C1, Tc), course_teacher(C2, Tc).

% 4. Room Capacity: Students <= room capacity
:- assign(C, R, _), course_attr(C, S, _), room_capacity(R, Cap), S > Cap.

% 5. Teacher Availability: Course must be in a slot where teacher is available
:- assign(C, _, T), course_teacher(C, Tc), not teacher_available(Tc, T).

% 6. Room Features: Course requiring a feature must be in a room with it
:- assign(C, R, _), requires_feature(C, F), not room_feature(R, F).

% 7. Prerequisites: Prerequisite must be in an earlier time slot
:- prerequisite(C1, C2), assign(C1, _, T1), assign(C2, _, T2), T1 >= T2.

% 8. Student Conflicts: Conflicting courses cannot be at the same time
:- conflict(C1, C2), assign(C1, _, T), assign(C2, _, T).

% 9. Global Evening Limit: At most 2 courses in time slot 5
:- #count { C : assign(C, _, 5) } > 2.

%%% OBJECTIVE: Minimize adjacent same-department pairs %%%

% A pair of same-department courses in consecutive time slots
adj_same_dept_pair(C1, C2, T) :-
    assign(C1, _, T), assign(C2, _, T+1), C1 != C2,
    course_attr(C1, _, D), course_attr(C2, _, D),
    time(T), time(T+1).

% Minimize the count of such pairs
#minimize { 1@1, C1, C2, T : adj_same_dept_pair(C1, C2, T) }.

%%% OUTPUT %%%

% Show assignments
#show assign/3.

% Show the total cost
total_cost(N) :- N = #count { C1, C2, T : adj_same_dept_pair(C1, C2, T) }.
#show total_cost/1.