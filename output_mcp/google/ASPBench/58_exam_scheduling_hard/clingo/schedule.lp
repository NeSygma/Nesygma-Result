% --- Domains ---
exam(e1; e2; e3; e4; e5; e6; e7; e8).
student(s1; s2; s3; s4; s5; s6).
time_slot(1..4).
room(r1; r2; r3).

% --- Data ---
enrollment(s1, e1). enrollment(s1, e3). enrollment(s1, e7).
enrollment(s2, e2). enrollment(s2, e4). enrollment(s2, e8).
enrollment(s3, e1). enrollment(s3, e5).
enrollment(s4, e2). enrollment(s4, e6).
enrollment(s5, e3). enrollment(s5, e5). enrollment(s5, e8).
enrollment(s6, e4). enrollment(s6, e6). enrollment(s6, e7).

room_type(r1, classroom). room_type(r2, classroom). room_type(r3, lab).
room_capacity(r1, 2). room_capacity(r2, 2). room_capacity(r3, 2).

exam_requirement(e1, classroom). exam_requirement(e2, classroom).
exam_requirement(e3, classroom). exam_requirement(e4, classroom).
exam_requirement(e5, classroom). exam_requirement(e6, classroom).
exam_requirement(e7, lab).       exam_requirement(e8, lab).

% Calculate exam size
exam_size(E, N) :- exam(E), N = #count { S : enrollment(S, E) }.

% --- Decision Variables ---
% Every exam must be assigned to exactly one time slot and one room.
{ assigned(E, T, R) : time_slot(T), room(R) } = 1 :- exam(E).

% --- Constraints ---

% 2. Student Conflict: A student cannot be scheduled for two different exams in the same time slot.
:- assigned(E1, T, _), assigned(E2, T, _), E1 != E2, 
   enrollment(S, E1), enrollment(S, E2).

% 3. Room Conflict: A room cannot host more than one exam in the same time slot.
:- assigned(E1, T, R), assigned(E2, T, R), E1 != E2.

% 4. Room Type: An exam must be scheduled in a room that matches its required type.
:- assigned(E, T, R), exam_requirement(E, Req), room_type(R, Type), Req != Type.

% 5. Room Capacity: The number of students enrolled in an exam cannot exceed the capacity of the room.
:- assigned(E, T, R), exam_size(E, Size), room_capacity(R, Cap), Size > Cap.

% --- Output ---
#show assigned/3.