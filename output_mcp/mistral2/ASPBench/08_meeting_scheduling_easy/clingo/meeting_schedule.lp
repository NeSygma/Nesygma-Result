% Domains
day(1..3).
slot(1..3).
room(r1). room(r2).
meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5).
person(p1). person(p2). person(p3). person(p4). person(p5).

% Required attendees
required_attendees(m1, p1). required_attendees(m1, p2). required_attendees(m1, p3).
required_attendees(m2, p1). required_attendees(m2, p5).
required_attendees(m3, p2). required_attendees(m3, p3).
required_attendees(m4, p1). required_attendees(m4, p4).
required_attendees(m5, p1). required_attendees(m5, p2). required_attendees(m5, p3).

% Time preferences
preferred_time(m1, 1, 1).
preferred_time(m2, 1, 2).
preferred_time(m4, 3, 3).

% Assign each meeting to exactly one time slot and room
{ assigned(M, D, S, R) : day(D), slot(S), room(R) } = 1 :- meeting(M).

% Preference violation: meeting not at preferred time
preference_violation(M) :- assigned(M, D, S, _), preferred_time(M, Dp, Sp), D != Dp.
preference_violation(M) :- assigned(M, D, S, _), preferred_time(M, Dp, Sp), S != Sp.

% No person attends two meetings at the same time
:- person(P), meeting(M1), meeting(M2), M1 != M2,
   required_attendees(M1, P), required_attendees(M2, P),
   assigned(M1, D, S, _), assigned(M2, D, S, _).

% Only one meeting per room per time slot
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% Objective: minimize preference violations
#minimize { 1@1, M : preference_violation(M) }.

% Output
#show assigned/4.
#show preference_violation/1.