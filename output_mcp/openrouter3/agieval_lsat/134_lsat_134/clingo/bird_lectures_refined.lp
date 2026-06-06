% Bird Lectures Problem - Refined
% Domain declarations
bird(oystercatchers). bird(petrels). bird(rails). bird(sandpipers). bird(terns).
hall(gladwyn). hall(howard).
time(1..5).

% Each bird gets exactly one time slot
1 { time_slot(B, T) : time(T) } 1 :- bird(B).

% Each time slot gets exactly one bird
1 { time_slot(B, T) : bird(B) } 1 :- time(T).

% Location assignment for each time slot (choice rule)
{ location(T, L) : hall(L) } 1 :- time(T).

% Derive bird location from time slot location
bird_location(B, L) :- time_slot(B, T), location(T, L).

% CONSTRAINT 1: First lecture is in Gladwyn Hall
:- location(1, howard).

% CONSTRAINT 2: Fourth lecture is in Howard Auditorium
:- location(4, gladwyn).

% CONSTRAINT 3: Exactly three lectures are in Gladwyn Hall
:- N = #count{T : location(T, gladwyn)}, N != 3.

% CONSTRAINT 4: Sandpipers lecture is in Howard Auditorium and earlier than oystercatchers
:- bird_location(sandpipers, gladwyn).
:- time_slot(sandpipers, T1), time_slot(oystercatchers, T2), T1 >= T2.

% CONSTRAINT 5: Terns lecture is earlier than petrels, and petrels is in Gladwyn Hall
:- time_slot(terns, T1), time_slot(petrels, T2), T1 >= T2.
:- bird_location(petrels, howard).

% Test each answer choice
% Option A: oystercatchers, petrels, rails, sandpipers, terns
option_a :- time_slot(oystercatchers, 1), time_slot(petrels, 2), time_slot(rails, 3), 
            time_slot(sandpipers, 4), time_slot(terns, 5).

% Option B: petrels, sandpipers, oystercatchers, terns, rails
option_b :- time_slot(petrels, 1), time_slot(sandpipers, 2), time_slot(oystercatchers, 3), 
            time_slot(terns, 4), time_slot(rails, 5).

% Option C: rails, sandpipers, terns, petrels, oystercatchers
option_c :- time_slot(rails, 1), time_slot(sandpipers, 2), time_slot(terns, 3), 
            time_slot(petrels, 4), time_slot(oystercatchers, 5).

% Option D: sandpipers, terns, oystercatchers, rails, petrels
option_d :- time_slot(sandpipers, 1), time_slot(terns, 2), time_slot(oystercatchers, 3), 
            time_slot(rails, 4), time_slot(petrels, 5).

% Option E: terns, petrels, sandpipers, oystercatchers, rails
option_e :- time_slot(terns, 1), time_slot(petrels, 2), time_slot(sandpipers, 3), 
            time_slot(oystercatchers, 4), time_slot(rails, 5).

% Map the correct answer to option/1 (MANDATORY)
option(a) :- option_a.
option(b) :- option_b.
option(c) :- option_c.
option(d) :- option_d.
option(e) :- option_e.

#show option/1.