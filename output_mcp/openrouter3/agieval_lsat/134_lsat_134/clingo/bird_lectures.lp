% Bird Lectures Problem
% Domain declarations
bird(oystercatchers). bird(petrels). bird(rails). bird(sandpipers). bird(terns).
hall(gladwyn). hall(howard).
time(1..5).

% Base constraints from problem statement
% 1. First lecture is in Gladwyn Hall
:- time(1), location(1, howard).

% 2. Fourth lecture is in Howard Auditorium
:- time(4), location(4, gladwyn).

% 3. Exactly three lectures are in Gladwyn Hall
:- N = #count{T : location(T, gladwyn)}, N != 3.

% 4. Sandpipers lecture is in Howard Auditorium and earlier than oystercatchers
:- location(sandpipers, gladwyn).
:- time(sandpipers) >= time(oystercatchers).

% 5. Terns lecture is earlier than petrels, and petrels is in Gladwyn Hall
:- time(terns) >= time(petrels).
:- location(petrels, howard).

% Each bird gets exactly one time slot
1 { time_slot(B, T) : time(T) } 1 :- bird(B).

% Each time slot gets exactly one bird
1 { time_slot(B, T) : bird(B) } 1 :- time(T).

% Location assignment based on time slot
location(T, L) :- time_slot(B, T), bird_location(B, L).

% Helper: bird location (derived from time slot location)
bird_location(B, L) :- time_slot(B, T), location(T, L).

% Define location for each time slot (choice rule)
{ location(T, L) : hall(L) } 1 :- time(T).

% Now let's test each answer choice
% For each choice, we'll create a rule that checks if the order matches

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