% Domain
day(1). day(2). day(3).
slot(1). slot(2). slot(3).
room(r1). room(r2).

% Meetings and persons
meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5).
person(p1). person(p2). person(p3). person(p4). person(p5).

% Attendance
attend(m1,p1). attend(m1,p2). attend(m1,p3).
attend(m2,p1). attend(m2,p5).
attend(m3,p2). attend(m3,p3).
attend(m4,p1). attend(m4,p4).
attend(m5,p1). attend(m5,p2). attend(m5,p3).

% Preferences
pref(m1,1,1). pref(m2,1,2). pref(m4,3,3).

% Assignment rule
{ assign(M,D,S,R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Constraints
% At most one meeting per (D,S,R)
:- assign(M1,D,S,R), assign(M2,D,S,R), M1 != M2.

% No person can attend two meetings at the same (D,S)
:- assign(M1,D,S,R1), assign(M2,D,S,R2), attend(M1,P), attend(M2,P), M1 != M2.

% Preference violation
vio(M) :- assign(M,D,S,R), not pref(M,D,S).

% Show assignments and violations
#show assign/4.
#show vio/1.