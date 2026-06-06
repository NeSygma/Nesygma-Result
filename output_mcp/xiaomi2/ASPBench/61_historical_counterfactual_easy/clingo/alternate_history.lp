% ==========================================
% Alternate History Causal Analysis
% ==========================================

% --- Domain: Events ---
event(discovery_of_america).
event(columbian_exchange).
event(spanish_empire).
event(industrial_revolution).
event(world_wars).

% --- Chronological ordering (year) ---
year(discovery_of_america, 1492).
year(columbian_exchange, 1500).
year(spanish_empire, 1520).
year(industrial_revolution, 1750).
year(world_wars, 1914).

% --- Prerequisites ---
requires(columbian_exchange, discovery_of_america).
requires(spanish_empire, discovery_of_america).
requires(industrial_revolution, spanish_empire).
requires(world_wars, industrial_revolution).

% --- Causal dependency (enables) ---
enables(discovery_of_america, columbian_exchange).
enables(discovery_of_america, spanish_empire).
enables(spanish_empire, industrial_revolution).
enables(industrial_revolution, world_wars).

% --- Intervention: Prevent discovery_of_america ---
intervention_event(discovery_of_america).

% ==========================================
% Prevention Logic (Cascade)
% ==========================================

% An event is prevented if it is directly intervened upon
prevented(E) :- intervention_event(E).

% An event is prevented if ANY of its prerequisites is prevented (cascade)
prevented(E) :- requires(E, P), prevented(P).

% ==========================================
% Occurrence Logic
% ==========================================

% An event occurs if it is NOT prevented
occurs(E) :- event(E), not prevented(E).

% ==========================================
% Classification
% ==========================================

% Direct effects: events immediately enabled by the prevented event(s)
% These are events whose prerequisite is the intervened event
direct_effect(E) :- requires(E, P), intervention_event(P).

% Cascade effects: events prevented through dependency chains (not direct)
cascade_effect(E) :- prevented(E), not intervention_event(E), not direct_effect(E).

% Preserved events: events that are NOT prevented
preserved(E) :- event(E), not prevented(E).

% ==========================================
% Timeline Construction
% ==========================================

% Original timeline: all events in chronological order
original_timeline(E) :- event(E).

% Alternate timeline: only events that occur (not prevented)
alternate_timeline(E) :- occurs(E).

% ==========================================
% Output Formatting
% ==========================================

% Show original timeline events sorted by year
#show original_timeline/1.

% Show alternate timeline events sorted by year
#show alternate_timeline/1.

% Show all prevented events
#show prevented/1.

% Show direct effects
#show direct_effect/1.

% Show cascade effects
#show cascade_effect/1.

% Show preserved events
#show preserved/1.

% Show intervention events
#show intervention_event/1.