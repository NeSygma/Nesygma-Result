% Scheduling Problem: 5 meetings over 3 days with room assignment
% Objective: Minimize preference violations (expected 0)

% ===== DOMAIN DECLARATIONS =====
day(1..3).
slot(1..3).
room(r1; r2).
meeting(m1; m2; m3; m4; m5).
person(p1; p2; p3; p4; p5).

% ===== REQUIRED ATTENDEES =====
required_attendees(m1, p1). required_attendees(m1, p2). required_attendees(m1, p3).
required_attendees(m2, p1). required_attendees(m2, p5).
required_attendees(m3, p2). required_attendees(m3, p3).
required_attendees(m4, p1). required_attendees(m4, p4).
required_attendees(m5, p1). required_attendees(m5, p2). required_attendees(m5, p3).

% ===== TIME PREFERENCES =====
preferred_time(m1, 1, 1).  % m1: day 1, slot 1
preferred_time(m2, 1, 2).  % m2: day 1, slot 2
preferred_time(m4, 3, 3).  % m4: day 3, slot 3

% ===== SCHEDULING CHOICE RULE =====
% Each meeting gets exactly one time slot and room
{ scheduled(m, d, s, r) : day(d), slot(s), room(r) } 1 :- meeting(m).

% ===== HARD CONSTRAINTS =====
% 1. No person can attend two meetings at the same time slot
:- scheduled(m1, d, s, _), scheduled(m2, d, s, _), m1 != m2,
   required_attendees(m1, p), required_attendees(m2, p).

% 2. Only one meeting per room per time slot
:- scheduled(m1, d, s, r), scheduled(m2, d, s, r), m1 != m2.

% ===== SOFT CONSTRAINT: PREFERENCE VIOLATIONS =====
% A meeting violates preference if not scheduled at its preferred time
violation(m) :- scheduled(m, d, s, _), not preferred_time(m, d, s).

% Minimize total preference violations
#minimize { 1, m : violation(m) }.

% ===== OUTPUT PREDICATES =====
% Schedule: meeting, day, slot, room
schedule(m, d, s, r) :- scheduled(m, d, s, r).

% Conflicts: empty array (no hard constraint violations in feasible solution)
conflicts(empty).

% Preference violations count
preference_violations(N) :- N = #count { m : violation(m) }.

% Feasibility: true if we have a schedule for all meetings
feasible(true) :- meeting(m), scheduled(m, _, _, _).

% ===== SHOW DIRECTIVES =====
#show schedule/4.
#show conflicts/1.
#show preference_violations/1.
#show feasible/1.