% Domains
course(0..7).
room(0..3).
time(0..5).
teacher(0..4).
feature(projector). feature(lab).

% Course data: name omitted, only needed attributes
teacher_of(0,0). teacher_of(1,0). teacher_of(2,1). teacher_of(3,2). teacher_of(4,3). teacher_of(5,4). teacher_of(6,4). teacher_of(7,4).
students(0,30). students(1,25). students(2,40). students(3,50). students(4,45). students(5,60). students(6,55). students(7,50).
dept(0,sci). dept(1,sci). dept(2,sci). dept(3,hum). dept(4,hum). dept(5,eng). dept(6,eng). dept(7,eng).

% Room capacities
capacity(0,60). capacity(1,50). capacity(2,40). capacity(3,30).
% Room features
feature_of(0,projector). feature_of(1,projector). feature_of(2,lab). feature_of(2,projector). % room 2 has both
% No features for room 3

% Teacher availability
avail(0,0). avail(0,1). avail(0,2).
avail(1,2). avail(1,3). avail(1,4).
avail(2,0). avail(2,1). avail(2,4). avail(2,5).
avail(3,0). avail(3,2). avail(3,3). avail(3,5).
avail(4,1). avail(4,2). avail(4,3). avail(4,4). avail(4,5).

% Course feature requirements
require_feature(2,lab).
require_feature(5,projector).
require_feature(6,projector).
require_feature(7,projector).

% Prerequisites (A before B)
prereq(0,1).
prereq(5,6).
prereq(6,7).

% Student conflicts (cannot be same time)
conflict(1,4).
conflict(2,5).

% ---------- Assignment ----------
% Exactly one room and time per course
1 { assign(C,R,T) : room(R), time(T) } 1 :- course(C).

% ---------- Constraints ----------
% Room uniqueness
:- assign(C1,R,T), assign(C2,R,T), C1 != C2.
% Teacher uniqueness
:- assign(C1,_,T), assign(C2,_,T), teacher_of(C1,Tr), teacher_of(C2,Tr), C1 != C2.
% Teacher availability
:- assign(C,_,T), teacher_of(C,Tr), not avail(Tr,T).
% Room capacity
:- assign(C,R,_), students(C,N), capacity(R,Cap), N > Cap.
% Room feature requirements
:- assign(C,R,_), require_feature(C,F), not feature_of(R,F).
% Prerequisites (strictly earlier)
:- assign(A,_,Ta), assign(B,_,Tb), prereq(A,B), not Ta < Tb.
% Student conflicts
:- assign(C1,_,T), assign(C2,_,T), conflict(C1,C2), C1 != C2.
% Global evening limit (slot 5 max 2 courses)
:- #count{ C : assign(C,_,5) } > 2.

% ---------- Cost: adjacent same-department pairs ----------
adjacent_same_dept(C1,C2) :- assign(C1,_,T1), assign(C2,_,T2), dept(C1,D), dept(C2,D), T2 = T1 + 1, C1 < C2.
cost(N) :- N = #count{ C1,C2 : adjacent_same_dept(C1,C2) }.

% Optimize
#minimize { 1@1, C1,C2 : adjacent_same_dept(C1,C2) }.

#show assign/3.
#show cost/1.