% --- Facts ---
% Event definitions
event(discovery_of_america; columbian_exchange; spanish_empire; industrial_revolution; world_wars).

% Chronological ordering (years)
year(discovery_of_america, 1492).
year(columbian_exchange, 1500).
year(spanish_empire, 1520).
year(industrial_revolution, 1750).
year(world_wars, 1914).

% Prerequisite relationships
prerequisite(columbian_exchange, discovery_of_america).
prerequisite(spanish_empire, discovery_of_america).
prerequisite(industrial_revolution, spanish_empire).
prerequisite(world_wars, industrial_revolution).

% Intervention: prevent discovery_of_america
intervention(discovery_of_america).

% --- Rules ---

% An event is prevented if it is the intervention event
prevented(E) :- intervention(E).

% An event is prevented if any of its prerequisites is prevented (cascade)
prevented(E) :- event(E), prerequisite(E, P), prevented(P).

% An event occurs in the alternate timeline if it is not prevented
occurs(E) :- event(E), not prevented(E).

% Original timeline: all events (original history)
original_timeline(E) :- event(E).

% Alternate timeline: events that occur after intervention
alternate_timeline(E) :- occurs(E).

% Direct effects: events immediately enabled by the prevented intervention event
direct_effect(E) :- prerequisite(E, P), intervention(P).

% Cascade effects: events prevented through dependency chains (not direct, not intervention)
cascade_effect(E) :- prevented(E), not intervention(E), not direct_effect(E).

% Preserved events: events not prevented by the intervention
preserved_event(E) :- event(E), not prevented(E).

% --- Output ---
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented/1.
#show direct_effect/1.
#show cascade_effect/1.
#show preserved_event/1.
#show intervention/1.