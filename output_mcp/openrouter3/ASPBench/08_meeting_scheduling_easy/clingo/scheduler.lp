% Scheduling Problem - 5 meetings over 3 days with room assignment

% ===== DOMAINS =====
day(1..3).
slot(1..3).
room(r1); room(r2).
meeting(m1); meeting(m2); meeting(m3); meeting(m4); meeting(m5).
person(p1); person(p2); person(p3); person(p4); person(p5).

% ===== REQUIRED ATTENDEES =====
required(m1, p1). required(m1, p2). required(m1, p3).
required(m2, p1). required(m2, p5).
required(m3, p2). required(m3, p3).
required(m4, p1). required(m4, p4).
required(m5, p1). required(m5, p2). required(m5, p3).

% ===== PREFERRED TIME SLOTS =====
preferred(m1, 1, 1).  % m1: day 1, slot 1
preferred(m2, 1, 2).  % m2: day 1, slot 2
preferred(m4, 3, 3).  % m4: day 3, slot 3

% ===== DECISION VARIABLES =====
% Each meeting is scheduled exactly once in a room and time slot
1 { scheduled(Meeting, Day, Slot, Room) : day(Day), slot(Slot), room(Room) } 1 :- meeting(Meeting).

% ===== CONSTRAINTS =====

% 1. No person can attend two meetings at the same time slot
% For each person, for each (day, slot), at most one meeting they're required for
:- required(Meeting1, Person), required(Meeting2, Person), 
   scheduled(Meeting1, Day, Slot, _), scheduled(Meeting2, Day, Slot, _),
   Meeting1 != Meeting2.

% 2. Only one meeting per room per time slot
:- scheduled(Meeting1, Day, Slot, Room), scheduled(Meeting2, Day, Slot, Room),
   Meeting1 != Meeting2.

% 3. All required attendees must be available (ensured by constraint 1)

% ===== PREFERENCE VIOLATIONS =====
% A meeting violates preference if it's not scheduled at its preferred time
preference_violation(Meeting) :- meeting(Meeting), 
                                  scheduled(Meeting, Day, Slot, _),
                                  not preferred(Meeting, Day, Slot).

% Count total violations
total_violations(N) :- N = #count { Meeting : preference_violation(Meeting) }.

% ===== OPTIMIZATION =====
% Minimize preference violations
#minimize { 1, Meeting : preference_violation(Meeting) }.

% ===== OUTPUT =====
% Show schedule assignments
#show scheduled/4.

% Show preference violations
#show preference_violation/1.

% Show total violations count
#show total_violations/1.

% Show if schedule is feasible (always true if model is satisfiable)
feasible :- #count { Meeting : meeting(Meeting) } = 5.
#show feasible/0.