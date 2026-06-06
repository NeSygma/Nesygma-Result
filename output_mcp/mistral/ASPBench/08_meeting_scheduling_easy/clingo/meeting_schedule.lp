% Domains
meeting(m1; m2; m3; m4; m5).
person(p1; p2; p3; p4; p5).
day(1; 2; 3).
slot(1; 2; 3).
room(r1; r2).

% Required attendees for each meeting
required_attendee(m1, p1).
required_attendee(m1, p2).
required_attendee(m1, p3).

required_attendee(m2, p1).
required_attendee(m2, p5).

required_attendee(m3, p2).
required_attendee(m3, p3).

required_attendee(m4, p1).
required_attendee(m4, p4).

required_attendee(m5, p1).
required_attendee(m5, p2).
required_attendee(m5, p3).

% Time preferences for meetings
preferred_time(m1, 1, 1).
preferred_time(m2, 1, 2).
preferred_time(m4, 3, 3).

% Choice rule: Assign each meeting to exactly one day, slot, and room
1 { assigned(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% Derive who attends which meeting
attends(P, M, D, S) :- assigned(M, D, S, _), required_attendee(M, P).

% Constraint: No person attends two meetings at the same time slot
:- attends(P, M1, D, S), attends(P, M2, D, S), M1 != M2.

% Constraint: Only one meeting per room per time slot
:- assigned(M1, D, S, R), assigned(M2, D, S, R), M1 != M2.

% Identify preference violations
preference_violation(M) :- assigned(M, D, S, _), preferred_time(M, D, S0), S != S0.
preference_violation(M) :- assigned(M, D, S, _), preferred_time(M, D0, S), D != D0.

% Objective: Minimize preference violations
#minimize { 1@1, M : preference_violation(M) }.

% Helper to count preference violations
num_preference_violations(N) :- N = #count { M : preference_violation(M) }.

% Helper to check feasibility (no preference violations and no constraint violations)
feasible :- not preference_violation(_).

% Output predicates
#show assigned/4.
#show num_preference_violations/1.
#show feasible/0.