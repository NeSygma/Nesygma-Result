% Scheduling 8 courses into 4 rooms across 6 time slots

% Domains
course(0..7).
room(0..3).
time(0..5).
teacher(0..4).
department(sci; hum; eng).

% Course data
course_teacher(0,0). course_students(0,30). course_dept(0,sci).
course_teacher(1,0). course_students(1,25). course_dept(1,sci).
course_teacher(2,1). course_students(2,40). course_dept(2,sci).
course_teacher(3,2). course_students(3,50). course_dept(3,hum).
course_teacher(4,3). course_students(4,45). course_dept(4,hum).
course_teacher(5,4). course_students(5,60). course_dept(5,eng).
course_teacher(6,4). course_students(6,55). course_dept(6,eng).
course_teacher(7,4). course_students(7,50). course_dept(7,eng).

% Room data
room_capacity(0,60). room_has_projector(0).
room_capacity(1,50). room_has_projector(1).
room_capacity(2,40). room_has_projector(2). room_has_lab(2).
room_capacity(3,30).

% Course requirements
course_requires_lab(2).
course_requires_projector(5). course_requires_projector(6). course_requires_projector(7).

% Teacher availability
teacher_available(0,0). teacher_available(0,1). teacher_available(0,2).
teacher_available(1,2). teacher_available(1,3). teacher_available(1,4).
teacher_available(2,0). teacher_available(2,1). teacher_available(2,4). teacher_available(2,5).
teacher_available(3,0). teacher_available(3,2). teacher_available(3,3). teacher_available(3,5).
teacher_available(4,1). teacher_available(4,2). teacher_available(4,3). teacher_available(4,4). teacher_available(4,5).

% Prerequisites (must be before)
prerequisite(0,1).
prerequisite(5,6).
prerequisite(6,7).

% Student conflicts (cannot be same time)
conflict(1,4).
conflict(2,5).

% Assignment: each course assigned exactly one room and time slot
1 { assigned(C, R, T) : room(R), time(T) } 1 :- course(C).

% Room uniqueness: at most one course per room per time slot
0 { assigned(C, R, T) : course(C) } 1 :- room(R), time(T).

% Teacher uniqueness: at most one course per teacher per time slot
% We'll use a constraint with count
:- teacher(Tchr), time(T), #count{ C : assigned(C,_,T), course_teacher(C,Tchr) } >= 2.

% Room capacity
:- assigned(C,R,T), course_students(C,S), room_capacity(R,Cap), S > Cap.

% Teacher availability
:- assigned(C,R,T), course_teacher(C,Tchr), not teacher_available(Tchr,T).

% Room features
:- assigned(C,R,T), course_requires_lab(C), not room_has_lab(R).
:- assigned(C,R,T), course_requires_projector(C), not room_has_projector(R).

% Prerequisites
:- prerequisite(C1,C2), assigned(C1,_,T1), assigned(C2,_,T2), T1 >= T2.

% Student conflicts
:- conflict(C1,C2), assigned(C1,_,T), assigned(C2,_,T).

% Global evening limit: max 2 courses in time slot 5
:- time(5), #count{ C : assigned(C,_,5) } > 2.

% Objective: minimize adjacent same-department pairs
% Count courses per department per time slot
dept_time_count(D, T, N) :- department(D), time(T), N = #count{ C : assigned(C,_,T), course_dept(C,D) }.

% For each consecutive time slots t and t+1, compute product of counts per department
pair_product(t, D, P) :- time(t), t < 5, department(D),
    dept_time_count(D, t, N1),
    dept_time_count(D, t+1, N2),
    P = N1 * N2.

% Total cost
cost(C) :- C = #sum{ P : pair_product(t, D, P) }.

% Minimize cost
#minimize{ C : cost(C) }.

% Show assignments and cost
#show assigned/3.
#show cost/1.