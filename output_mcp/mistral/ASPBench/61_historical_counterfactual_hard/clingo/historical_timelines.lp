% --- DOMAINS ---
% Events with their years
event(ancient_knowledge, 100).
event(fall_of_rome, 476).
event(dark_ages, 500).
event(renaissance, 1300).
event(age_of_sail, 1400).
event(age_of_steam, 1700).
event(discovery_of_new_world, 1492).
event(global_trade_routes, 1550).
event(industrial_revolution, 1760).
event(information_age, 1970).
event(alternate_industrial_revolution, 1780).
event(digital_renaissance, 1980).

% Pivot groups (mutually exclusive)
pivot_group(paradigm, age_of_sail).
pivot_group(paradigm, age_of_steam).

% Prerequisites (direct requirements)
requires(age_of_sail, renaissance).
requires(age_of_steam, renaissance).
requires(renaissance, dark_ages).
requires(dark_ages, fall_of_rome).
requires(fall_of_rome, ancient_knowledge).
requires(discovery_of_new_world, age_of_sail).
requires(global_trade_routes, age_of_sail).
requires(industrial_revolution, age_of_steam).
requires(information_age, industrial_revolution).
requires(digital_renaissance, alternate_industrial_revolution).

% Conditional prerequisite: alternate_industrial_revolution requires global_trade_routes UNLESS age_of_steam occurs
conditional_requires(alternate_industrial_revolution, global_trade_routes, age_of_steam).

% Interventions (prevented events)
prevented(age_of_sail).

% --- TIMELINE GENERATION ---
% Original timeline: deterministic choice based on earliest year in pivot groups
{ original_occurs(E) : event(E, _) }.

% Alternate timeline: apply interventions
{ alternate_occurs(E) : event(E, _) }.

% --- PREREQUISITE SATISFACTION ---
% Original timeline
:- original_occurs(E), requires(E, R), not original_occurs(R).

% Conditional prerequisite for original timeline
:- original_occurs(alternate_industrial_revolution), 
   not original_occurs(global_trade_routes), 
   not original_occurs(age_of_steam).

% Alternate timeline
:- alternate_occurs(E), requires(E, R), not alternate_occurs(R).

% Conditional prerequisite for alternate timeline
:- alternate_occurs(alternate_industrial_revolution), 
   not alternate_occurs(global_trade_routes), 
   not alternate_occurs(age_of_steam).

% --- PIVOT GROUP CONSTRAINTS ---
% At most one event from each pivot group can occur in each timeline
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, original_occurs(E1), original_occurs(E2).
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2, alternate_occurs(E1), alternate_occurs(E2).

% If any pivot event is possible (prerequisites met), exactly one must be chosen
% Original timeline
:- pivot_group(G, _),
   #count{ E : pivot_group(G, E), original_occurs(E) } > 0,
   #count{ E : pivot_group(G, E), original_occurs(E) } != 1.

% Alternate timeline
:- pivot_group(G, _),
   #count{ E : pivot_group(G, E), alternate_occurs(E) } > 0,
   #count{ E : pivot_group(G, E), alternate_occurs(E) } != 1.

% Original timeline pivot selection: choose earliest year if multiple possible
% Enforce that if an earlier year pivot event is possible but not chosen,
% then no later year pivot event can be chosen
:- pivot_group(G, E1), pivot_group(G, E2), E1 != E2,
   event(E1, Y1), event(E2, Y2), Y1 < Y2,
   original_occurs(E1), not original_occurs(E2),
   original_occurs(E2).

% --- INTERVENTION ENFORCEMENT ---
% Prevented events cannot occur in alternate timeline
:- alternate_occurs(E), prevented(E).

% --- PARADOX DETECTION ---
% A paradox occurs if we have contradictory constraints
paradox :- alternate_occurs(E), prevented(E).

% --- OUTPUT SPECIFICATION ---
% Define timeline events sorted by year
original_timeline(E) :- original_occurs(E), event(E, Y).
alternate_timeline(E) :- alternate_occurs(E), event(E, Y).

% Prevented events: in original but not in alternate
prevented_event(E) :- original_occurs(E), not alternate_occurs(E).

% Activated events: in alternate but not in original
activated_event(E) :- alternate_occurs(E), not original_occurs(E).

% Show the required outputs
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_event/1.
#show activated_event/1.
#show paradox/0.