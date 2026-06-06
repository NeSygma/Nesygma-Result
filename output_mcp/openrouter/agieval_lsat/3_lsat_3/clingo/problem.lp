% Students
student(george).
student(helen).
student(irving).
student(kyle).
student(lenore).
student(nina).
student(olivia).
student(robert).

% Days and times
day(mon). day(tue). day(wed).
time(morning). time(afternoon).

next(mon,tue). next(tue,wed).

% ---------- Schedule template for each option ----------
% Schedule A (for option A)
1 { assignA(S,D,T) : student(S) } 1 :- day(D), time(T).
:- assignA(S,D1,T1), assignA(S,D2,T2), (D1,T1) != (D2,T2).
% constraints
:- assignA(george,D,_), D != tue.
:- assignA(olivia,_,afternoon).
:- assignA(robert,_,afternoon).
:- assignA(nina,D,_), D != wed, next(D,D2), not assignA(helen,D2,_).
:- assignA(nina,D,_), D != wed, next(D,D2), not assignA(irving,D2,_).

% Schedule B (for option B)
1 { assignB(S,D,T) : student(S) } 1 :- day(D), time(T).
:- assignB(S,D1,T1), assignB(S,D2,T2), (D1,T1) != (D2,T2).
:- assignB(george,D,_), D != tue.
:- assignB(olivia,_,afternoon).
:- assignB(robert,_,afternoon).
:- assignB(nina,D,_), D != wed, next(D,D2), not assignB(helen,D2,_).
:- assignB(nina,D,_), D != wed, next(D,D2), not assignB(irving,D2,_).

% Schedule C (for option C)
1 { assignC(S,D,T) : student(S) } 1 :- day(D), time(T).
:- assignC(S,D1,T1), assignC(S,D2,T2), (D1,T1) != (D2,T2).
:- assignC(george,D,_), D != tue.
:- assignC(olivia,_,afternoon).
:- assignC(robert,_,afternoon).
:- assignC(nina,D,_), D != wed, next(D,D2), not assignC(helen,D2,_).
:- assignC(nina,D,_), D != wed, next(D,D2), not assignC(irving,D2,_).

% Schedule D (for option D)
1 { assignD(S,D,T) : student(S) } 1 :- day(D), time(T).
:- assignD(S,D1,T1), assignD(S,D2,T2), (D1,T1) != (D2,T2).
:- assignD(george,D,_), D != tue.
:- assignD(olivia,_,afternoon).
:- assignD(robert,_,afternoon).
:- assignD(nina,D,_), D != wed, next(D,D2), not assignD(helen,D2,_).
:- assignD(nina,D,_), D != wed, next(D,D2), not assignD(irving,D2,_).

% Schedule E (for option E)
1 { assignE(S,D,T) : student(S) } 1 :- day(D), time(T).
:- assignE(S,D1,T1), assignE(S,D2,T2), (D1,T1) != (D2,T2).
:- assignE(george,D,_), D != tue.
:- assignE(olivia,_,afternoon).
:- assignE(robert,_,afternoon).
:- assignE(nina,D,_), D != wed, next(D,D2), not assignE(helen,D2,_).
:- assignE(nina,D,_), D != wed, next(D,D2), not assignE(irving,D2,_).

% ---------- Same day non-Wednesday conditions ----------
same_day_nonwed_a :- assignA(george,D,_), assignA(lenore,D,_), D != wed.
same_day_nonwed_b :- assignB(helen,D,_), assignB(nina,D,_), D != wed.
same_day_nonwed_c :- assignC(irving,D,_), assignC(robert,D,_), D != wed.
same_day_nonwed_d :- assignD(kyle,D,_), assignD(nina,D,_), D != wed.
same_day_nonwed_e :- assignE(olivia,D,_), assignE(kyle,D,_), D != wed.

% ---------- Use flags to test possibility ----------
{useA}.
{useB}.
{useC}.
{useD}.
{useE}.

% If we use a flag, the corresponding same_day_nonwed must hold
:- useA, not same_day_nonwed_a.
:- useB, not same_day_nonwed_b.
:- useC, not same_day_nonwed_c.
:- useD, not same_day_nonwed_d.
:- useE, not same_day_nonwed_e.

% Option is true when the corresponding use flag cannot be true (i.e., impossible)
option(a) :- not useA.
option(b) :- not useB.
option(c) :- not useC.
option(d) :- not useD.
option(e) :- not useE.

% Exactly one option must be selected
1 { option(a); option(b); option(c); option(d); option(e) } 1.

#show option/1.