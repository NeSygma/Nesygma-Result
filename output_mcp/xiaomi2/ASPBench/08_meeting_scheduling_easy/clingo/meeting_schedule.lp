% =============================================
% Meeting Scheduling with Room Assignment
% Minimize preference violations
% =============================================

% --- Domains ---
day(1..3).
slot(1..3).
room(r1). room(r2).
meeting(m1). meeting(m2). meeting(m3). meeting(m4). meeting(m5).
person(p1). person(p2). person(p3). person(p4). person(p5).

% --- Required Attendees ---
attendee(m1, p1). attendee(m1, p2). attendee(m1, p3).
attendee(m2, p1). attendee(m2, p5).
attendee(m3, p2). attendee(m3, p3).
attendee(m4, p1). attendee(m4, p4).
attendee(m5, p1). attendee(m5, p2). attendee(m5, p3).

% --- Time Preferences ---
preference(m1, 1, 1).   % Project kickoff: day 1, slot 1
preference(m2, 1, 2).   % Budget review: day 1, slot 2
preference(m4, 3, 3).   % Client presentation: day 3, slot 3

% =============================================
% Decision Variables (Choice Rules)
% =============================================

% Each meeting is assigned to exactly one (day, slot, room)
1 { scheduled(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% =============================================
% Hard Constraints
% =============================================

% Constraint 2: No person can attend two meetings at the same time slot
% If two meetings share a required attendee, they cannot be at the same (day, slot)
:- attendee(M1, P), attendee(M2, P), M1 != M2,
   scheduled(M1, D, S, _), scheduled(M2, D, S, _).

% Constraint 3: Only one meeting per room per time slot
:- scheduled(M1, D, S, R), scheduled(M2, D, S, R), M1 != M2.

% =============================================
% Preference Violation Detection
% =============================================

% A meeting has a preference if it's listed in preference/3
has_preference(M) :- preference(M, _, _).

% A meeting is at its preferred time if scheduled at (D,S) matching preference
at_preferred_time(M) :- scheduled(M, D, S, _), preference(M, D, S).

% A preference violation occurs when a meeting with a preference is NOT at preferred time
preference_violation(M) :- has_preference(M), not at_preferred_time(M).

% =============================================
% Optimization Objective
% =============================================

% Minimize the number of preference violations
#minimize { 1, M : preference_violation(M) }.

% =============================================
% Output
% =============================================

#show scheduled/4.
#show preference_violation/1.