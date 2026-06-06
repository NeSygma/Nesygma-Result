% Domain
time(1). time(2). time(3). time(4).
room(r1). room(r2). room(r3).

% Types
room_type(r1, classroom). room_type(r2, classroom). room_type(r3, lab).
exam_type(e1, classroom). exam_type(e2, classroom). exam_type(e3, classroom). exam_type(e4, classroom).
exam_type(e5, classroom). exam_type(e6, classroom). exam_type(e7, lab). exam_type(e8, lab).

% Enrollments
student_enrolled(s1, e1). student_enrolled(s1, e3). student_enrolled(s1, e7).
student_enrolled(s2, e2). student_enrolled(s2, e4). student_enrolled(s2, e8).
student_enrolled(s3, e1). student_enrolled(s3, e5).
student_enrolled(s4, e2). student_enrolled(s4, e6).
student_enrolled(s5, e3). student_enrolled(s5, e5). student_enrolled(s5, e8).
student_enrolled(s6, e4). student_enrolled(s6, e6). student_enrolled(s6, e7).

% Allowed exam-room combos
allowed(E,R) :- exam_type(E,T), room_type(R,T).

% Schedule rule
schedule(E,T,R) :- allowed(E,R), time(T).

% Each exam exactly one assignment
1 { schedule(E,T,R) : time(T), room(R) } 1 :- exam(E).

% Room conflict: at most one exam per room per time slot
:- schedule(E1,T,R), schedule(E2,T,R), E1 != E2.

% Student conflict constraints (pairwise)
:- schedule(e1,T,R1), schedule(e3,T,R2), student_enrolled(s1, e1), student_enrolled(s1, e3).
:- schedule(e1,T,R1), schedule(e7,T,R2), student_enrolled(s1, e1), student_enrolled(s1, e7).
:- schedule(e3,T,R1), schedule(e7,T,R2), student_enrolled(s1, e3), student_enrolled(s1, e7).

:- schedule(e2,T,R1), schedule(e4,T,R2), student_enrolled(s2, e2), student_enrolled(s2, e4).
:- schedule(e2,T,R1), schedule(e8,T,R2), student_enrolled(s2, e2), student_enrolled(s2, e8).
:- schedule(e4,T,R1), schedule(e8,T,R2), student_enrolled(s2, e4), student_enrolled(s2, e8).

:- schedule(e1,T,R1), schedule(e5,T,R2), student_enrolled(s3, e1), student_enrolled(s3, e5).

:- schedule(e2,T,R1), schedule(e6,T,R2), student_enrolled(s4, e2), student_enrolled(s4, e6).

:- schedule(e3,T,R1), schedule(e5,T,R2), student_enrolled(s5, e3), student_enrolled(s5, e5).
:- schedule(e3,T,R1), schedule(e8,T,R2), student_enrolled(s5, e3), student_enrolled(s5, e8).
:- schedule(e5,T,R1), schedule(e8,T,R2), student_enrolled(s5, e5), student_enrolled(s5, e8).

:- schedule(e4,T,R1), schedule(e6,T,R2), student_enrolled(s6, e4), student_enrolled(s6, e6).
:- schedule(e4,T,R1), schedule(e7,T,R2), student_enrolled(s6, e4), student_enrolled(s6, e7).
:- schedule(e6,T,R1), schedule(e7,T,R2), student_enrolled(s6, e6), student_enrolled(s6, e7).

% Show schedule
#show schedule/3.