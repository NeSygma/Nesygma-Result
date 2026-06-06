% --- Event Definitions ---
event(discovery_of_america; columbian_exchange; spanish_empire; industrial_revolution; world_wars).

% Event years (chronological order)
year(discovery_of_america, 1492).
year(columbian_exchange, 1500).
year(spanish_empire, 1520).
year(industrial_revolution, 1750).
year(world_wars, 1914).

% --- Prerequisite Relationships ---
% prerequisite(Event, Prerequisite)
prerequisite(columbian_exchange, discovery_of_america).
prerequisite(spanish_empire, discovery_of_america).
prerequisite(industrial_revolution, spanish_empire).
prerequisite(world_wars, industrial_revolution).

% --- Intervention ---
% The event that is directly prevented by intervention
intervention_event(discovery_of_america).

% --- Causal Analysis ---

% 1. Original timeline: all events sorted by year
% Since years are unique and chronological, we can just list them
original_timeline_event(E) :- event(E).

% 2. Prevented events
% Directly prevented by intervention
prevented(E) :- intervention_event(E).

% Cascade: if an event's prerequisite is prevented, it is also prevented
prevented(E) :- event(E), prerequisite(E, P), prevented(P).

% 3. Alternate timeline: events that are NOT prevented and have all prerequisites satisfied
% An event occurs in alternate timeline if it's not prevented
% and all its prerequisites are not prevented (i.e., occur)
alternate_timeline_event(E) :- event(E), not prevented(E), not has_prevented_prereq(E).

% Helper: event has at least one prevented prerequisite
has_prevented_prereq(E) :- event(E), prerequisite(E, P), prevented(P).

% 4. Direct effects: events immediately enabled by the prevented event
% These are events whose prerequisite is the intervention event
direct_effect(E) :- event(E), prerequisite(E, P), intervention_event(P), prevented(E).

% 5. Cascade effects: events prevented indirectly through dependency chains
% These are prevented events that are NOT direct effects and NOT the intervention event itself
cascade_effect(E) :- prevented(E), not direct_effect(E), not intervention_event(E).

% 6. Preserved events: events not prevented by the intervention
preserved_event(E) :- event(E), not prevented(E).

% --- Output Mappings ---

% Original timeline (all events in chronological order)
% Use ordering by year
ordered(1, discovery_of_america).
ordered(2, columbian_exchange).
ordered(3, spanish_empire).
ordered(4, industrial_revolution).
ordered(5, world_wars).

original_timeline(Pos, E) :- ordered(Pos, E).

% Alternate timeline: events that occur, ordered by year
% We need to assign positions to alternate events
% First, collect alternate events
alt_event(E) :- alternate_timeline_event(E).

% Assign positions based on year ordering
alt_ordered(1, E) :- alt_event(E), year(E, Y), Y = 1492.
alt_ordered(2, E) :- alt_event(E), year(E, Y), Y = 1500.
alt_ordered(3, E) :- alt_event(E), year(E, Y), Y = 1520.
alt_ordered(4, E) :- alt_event(E), year(E, Y), Y = 1750.
alt_ordered(5, E) :- alt_event(E), year(E, Y), Y = 1914.

alternate_timeline(Pos, E) :- alt_ordered(Pos, E).

% Prevented events list
prevented_event(E) :- prevented(E).

% --- Show directives ---
#show original_timeline/2.
#show alternate_timeline/2.
#show prevented_event/1.
#show direct_effect/1.
#show cascade_effect/1.
#show preserved_event/1.
#show intervention_event/1.