%%% DATA %%%

% Courses
course(0;1;2;3;4;5;6;7).
course_name(0,"Physics I";1,"Physics II";2,"Chemistry";3,"History";4,"Literature";5,"Intro Programming";6,"Data Structures";7,"Algorithms").
teacher_of(0,0;1,0;2,1;3,2;4,3;5,4;6,4;7,4).
students(0,30;1,25;2,40;3,50;4,45;5,60;6,55;7,50).
dept(0,sci;1,sci;2,sci;3,hum;4,hum;5,eng;6,eng;7,eng).

% Rooms
room(0;1;2;3).
room_capacity(0,60;1,50;2,40;3,30).
room_feature(0,projector;1,projector;2,lab;2,projector).

% Time slots
time(0..5).

% Teacher availability
available(0,0;0,1;0,2).
available(1,2;1,3;1,4).
available(2,0;2,1;2,4;2,5).
available(3,0;3,2;3,3;3,5).
available(4,1;4,2;4,3;4,4;4,5).

% Room requirements
requires_feature(2,lab).
requires_feature(5,projector;6,projector;7,projector).

% Prerequisites: course A must be before course B
prereq(0,1).
prereq(5,6).
prereq(6,7).

% Student conflicts: cannot be at same time
conflict(1,4).
conflict(2,5).

%%% DOMAIN PREDICATES %%%

% Each course assigned to exactly one (room, time) pair
1 { assign(C,R,T) : room(R), time(T) } 1 :- course(C).

%%% CONSTRAINTS %%%

% Room uniqueness: a room cannot have two courses at the same time
:- assign(C1,R,T), assign(C2,R,T), C1 != C2.

% Teacher uniqueness: a teacher cannot teach two courses at the same time
:- assign(C1,_,T), assign(C2,_,T), C1 != C2, teacher_of(C1,Te), teacher_of(C2,Te).

% Room capacity: students <= room capacity
:- assign(C,R,_), students(C,S), room_capacity(R,Cap), S > Cap.

% Teacher availability
:- assign(C,_,T), teacher_of(C,Te), not available(Te,T).

% Room features
:- requires_feature(C,F), assign(C,R,_), not room_feature(R,F).

% Prerequisites: prereq(A,B) => time(A) < time(B)
:- prereq(A,B), assign(A,_,TA), assign(B,_,TB), TA >= TB.

% Student conflicts: cannot be at same time
:- conflict(A,B), assign(A,_,T), assign(B,_,T).

% Global evening limit: max 2 courses in time slot 5
:- #count { C : assign(C,_,5) } > 2.

%%% OBJECTIVE: Minimize adjacent same-department pairs %%%

% For each pair of courses from the same department scheduled in consecutive time slots
adj_same_dept(C1,C2) :- assign(C1,_,T1), assign(C2,_,T2), C1 != C2,
                        dept(C1,D), dept(C2,D),
                        |T1 - T2| = 1.

% Count them
cost(N) :- N = #count { C1,C2 : adj_same_dept(C1,C2) }.

#minimize { N : cost(N) }.

%%% OUTPUT %%%
#show assign/3.
#show cost/1.