% Days, slots, rooms
day(1..3).
slot(1..3).
room(r1; r2).
time_slot(D, S) :- day(D), slot(S).

% Meetings
meeting(m1; m2; m3; m4; m5).

% People
person(p1; p2; p3; p4; p5).

% Required attendees
required_attendee(m1, p1).  % Alice
required_attendee(m1, p2).  % Bob
required_attendee(m1, p3).  % Carol
required_attendee(m2, p1).  % Alice
required_attendee(m2, p5).  % Eve
required_attendee(m3, p2).  % Bob
required_attendee(m3, p3).  % Carol
required_attendee(m4, p1).  % Alice
required_attendee(m4, p4).  % Dave
required_attendee(m5, p1).  % Alice
required_attendee(m5, p2).  % Bob
required_attendee(m5, p3).  % Carol

% Time preferences
preference(m1, 1, 1).  % day 1, slot 1
preference(m2, 1, 2).  % day 1, slot 2
preference(m4, 3, 3).  % day 3, slot 3

% 1. Each meeting assigned exactly one (day, slot, room)
1 { assigned(M, D, S, R) : time_slot(D, S), room(R) } 1 :- meeting(M).

% 2. No person can attend two meetings at the same time slot
:- person(P), day(D), slot(S), 
   #count { M : assigned(M, D, S, _), required_attendee(M, P) } > 1.

% 3. Only one meeting per room per time slot
:- room(R), day(D), slot(S),
   #count { M : assigned(M, D, S, R) } > 1.

% 4. All required attendees must be available (ensured by constraint 2 and 1)

% Preference violation: meeting with a preference not scheduled at its preferred (day, slot)
violation(M) :- meeting(M), preference(M, Dp, Sp), not assigned(M, Dp, Sp, _).

% Minimize violations
#minimize { 1, M : violation(M) }.

% Show output
#show assigned/4.
#show violation/1.