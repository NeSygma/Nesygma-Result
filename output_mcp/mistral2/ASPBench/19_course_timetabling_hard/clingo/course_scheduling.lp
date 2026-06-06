% Domains
course(0..7).
room(0..3).
time(0..5).
teacher(0..4).
department(sci; hum; eng).

% Course attributes: course(C, Teacher, Students, Department)
course_attr(0, 0, 30, sci).
course_attr(1, 0, 25, sci).
course_attr(2, 1, 40, sci).
course_attr(3, 2, 50, hum).
course_attr(4, 3, 45, hum).
course_attr(5, 4, 60, eng).
course_attr(6, 4, 55, eng).
course_attr(7, 4, 50, eng).

% Room attributes: room(R, Capacity, Features)
room_attr(0, 60, "projector").
room_attr(1, 50, "projector").
room_attr(2, 40, "lab;projector").
room_attr(3, 30, "").

% Teacher availability: teacher_avail(Tch, T)
teacher_avail(0, 0). teacher_avail(0, 1). teacher_avail(0, 2).
teacher_avail(1, 2). teacher_avail(1, 3). teacher_avail(1, 4).
teacher_avail(2, 0). teacher_avail(2, 1). teacher_avail(2, 4). teacher_avail(2, 5).
teacher_avail(3, 0). teacher_avail(3, 2). teacher_avail(3, 3). teacher_avail(3, 5).
teacher_avail(4, 1). teacher_avail(4, 2). teacher_avail(4, 3). teacher_avail(4, 4). teacher_avail(4, 5).

% Room requirements: requires_feature(C, F)
requires_feature(2, lab).
requires_feature(5, projector).
requires_feature(6, projector).
requires_feature(7, projector).

% Prerequisites: prereq(C1, C2)
prereq(0, 1).
prereq(5, 6).
prereq(6, 7).

% Student conflicts: conflict(C1, C2)
conflict(1, 4).
conflict(2, 5).

% Helper predicate: has_feature(R, F)
has_feature(R, F) :- room_attr(R, _, Features), F = "lab", Features = "lab;projector".
has_feature(R, F) :- room_attr(R, _, Features), F = "projector", Features = "projector".
has_feature(R, F) :- room_attr(R, _, Features), F = "projector", Features = "lab;projector".

% Assignment choice rule
1 { assigned(C, R, T) : room(R), time(T) } 1 :- course(C).

% Constraints

% Room uniqueness: No two courses in the same room at the same time
:- assigned(C1, R, T), assigned(C2, R, T), C1 != C2.

% Teacher uniqueness: No two courses taught by the same teacher at the same time
:- assigned(C1, _, T), assigned(C2, _, T), C1 != C2, course_attr(C1, Tch, _, _), course_attr(C2, Tch, _, _).

% Room capacity: Course students <= room capacity
:- assigned(C, R, T), course_attr(C, _, Students, _), room_attr(R, Capacity, _), Students > Capacity.

% Teacher availability: Course can only be scheduled when teacher is available
:- assigned(C, _, T), course_attr(C, Tch, _, _), not teacher_avail(Tch, T).

% Room features: Course must be in a room with required features
:- assigned(C, R, T), requires_feature(C, F), not has_feature(R, F).

% Course prerequisites: C1 must be scheduled before C2
:- assigned(C2, _, T2), assigned(C1, _, T1), prereq(C1, C2), T1 >= T2.

% Student conflicts: Conflicting courses cannot be scheduled at the same time
:- assigned(C1, _, T), assigned(C2, _, T), conflict(C1, C2).

% Global evening limit: At most 2 courses in time slot 5
:- #count { C : assigned(C, _, 5) } > 2.

% Objective: Minimize adjacent same-department course pairs
same_dept_adjacent(C1, C2, T) :- assigned(C1, _, T), assigned(C2, _, T+1), course_attr(C1, _, _, Dept1), course_attr(C2, _, _, Dept2), Dept1 == Dept2.

% Minimize the number of adjacent same-department course pairs
#minimize { 1, C1, C2, T : same_dept_adjacent(C1, C2, T) }.

% Show assignments
#show assigned/3.
#show same_dept_adjacent/3.