% ============================================
% Meeting Scheduling Problem
% ============================================

% --- Domain Definitions ---
day(1). day(2). day(3).
slot(1). slot(2). slot(3).
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
pref(m1, 1, 1).  % day 1, slot 1
pref(m2, 1, 2).  % day 1, slot 2
pref(m4, 3, 3).  % day 3, slot 3

% --- Decision Variables ---
% Each meeting must be assigned exactly one time slot and one room
1 { scheduled(M, D, S, R) : day(D), slot(S), room(R) } 1 :- meeting(M).

% --- Constraint 1: No person can attend two meetings at the same time slot ---
% Two meetings conflict if they share an attendee and are scheduled at the same day+slot
conflict(M1, M2) :- 
    scheduled(M1, D, S, _), 
    scheduled(M2, D, S, _), 
    M1 < M2, 
    attendee(M1, P), 
    attendee(M2, P).

% Forbid any conflicts
:- conflict(M1, M2).

% --- Constraint 2: Only one meeting per room per time slot ---
room_conflict(M1, M2) :- 
    scheduled(M1, D, S, R), 
    scheduled(M2, D, S, R), 
    M1 < M2.

:- room_conflict(M1, M2).

% --- Preference Violations ---
% A meeting violates its preference if it's not scheduled at its preferred time
pref_violated_day(M) :- 
    meeting(M), 
    pref(M, PD, _), 
    scheduled(M, D, _, _), 
    D != PD.

pref_violated_slot(M) :- 
    meeting(M), 
    pref(M, _, PS), 
    scheduled(M, _, S, _), 
    S != PS.

pref_violated(M) :- pref_violated_day(M).
pref_violated(M) :- pref_violated_slot(M).

% Count preference violations
preference_violations(N) :- N = #count{M : pref_violated(M)}.

% --- Feasibility ---
% A schedule is feasible if no conflicts exist
has_conflict :- conflict(_, _).
has_room_conflict :- room_conflict(_, _).
feasible :- not has_conflict, not has_room_conflict.

% --- Optimization ---
#minimize { 1,M : pref_violated(M) }.

% --- Output ---
#show scheduled/4.
#show preference_violations/1.
#show feasible/0.