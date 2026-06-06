% Facts: Courses
course(0, "Math", 0, 25).
course(1, "Physics", 1, 20).
course(2, "Chemistry", 2, 30).
course(3, "Biology", 1, 15).
course(4, "Computer Science", 0, 35).

% Facts: Rooms
room(0, 40).
room(1, 25).
room(2, 20).

% Facts: Time Slots
time_slot(0).
time_slot(1).
time_slot(2).
time_slot(3).

% Facts: Teacher Availability
teacher_availability(0, 0).
teacher_availability(0, 1).
teacher_availability(0, 2).
teacher_availability(1, 1).
teacher_availability(1, 2).
teacher_availability(1, 3).
teacher_availability(2, 0).
teacher_availability(2, 2).
teacher_availability(2, 3).

% Choice Rule: Assign courses to (room, time_slot) pairs
{ assigned(C, R, T) : room(R, _), time_slot(T) } 1 :- course(C, _, _, _).

% Constraints

% Each course is assigned exactly once
:- course(C, _, _, _), not assigned(C, _, _).

% No two courses share the same (room, time_slot)
:- assigned(C1, R, T), assigned(C2, R, T), C1 != C2.

% Teacher availability: Courses can only be scheduled when the teacher is available
:- assigned(C, _, T), course(C, _, Teacher, _), not teacher_availability(Teacher, T).

% Teacher cannot teach multiple courses simultaneously
:- assigned(C1, _, T), assigned(C2, _, T), course(C1, _, Teacher, _), course(C2, _, Teacher, _), C1 != C2.

% Room capacity must accommodate course enrollment
:- assigned(C, R, _), course(C, _, _, Students), room(R, Capacity), Students > Capacity.

% Show the assignment
#show assigned/3.