% ============================================
% Alternate History Causal Analysis
% ============================================

% ---- Domain: Events with their years ----
event(discovery_of_america).
event(columbian_exchange).
event(spanish_empire).
event(industrial_revolution).
event(world_wars).

year(discovery_of_america, 1492).
year(columbian_exchange, 1500).
year(spanish_empire, 1520).
year(industrial_revolution, 1750).
year(world_wars, 1914).

% ---- Causal Dependencies (prerequisites) ----
% Event E requires prerequisite P
requires(columbian_exchange, discovery_of_america).
requires(spanish_empire, discovery_of_america).
requires(industrial_revolution, spanish_empire).
requires(world_wars, industrial_revolution).

% ---- Intervention: Prevent discovery_of_america ----
intervention(discovery_of_america).

% ---- Original Timeline: All events occur ----
occurs_original(E) :- event(E).

% ---- Alternate Timeline Logic ----

% An event is prevented if it is directly intervened upon
prevented(E) :- intervention(E).

% An event is prevented if ANY of its prerequisites is prevented (cascade)
prevented(E) :- event(E), requires(E, P), prevented(P).

% An event occurs in the alternate timeline if it is NOT prevented
occurs_alternate(E) :- event(E), not prevented(E).

% ---- Causal Analysis Classification ----

% Direct effects: events immediately enabled by the prevented event
direct_effect(E) :- intervention(P), requires(E, P).

% Cascade effects: events prevented indirectly through dependency chains
% (prevented but not directly intervened upon, and not a direct effect of intervention)
cascade_effect(E) :- prevented(E), not intervention(E), not direct_effect(E).

% Preserved events: events that remain in the alternate timeline
preserved(E) :- occurs_alternate(E).

% ---- Output Formatting ----

% Original timeline in chronological order
original_timeline(E) :- occurs_original(E).

% Alternate timeline in chronological order
alternate_timeline(E) :- occurs_alternate(E).

% All prevented events
prevented_events(E) :- prevented(E).

% Causal analysis sub-fields
causal_direct_effects(E) :- direct_effect(E).
causal_cascade_effects(E) :- cascade_effect(E).
causal_preserved_events(E) :- preserved(E).
causal_intervention_events(E) :- intervention(E).

% ---- Show Directives ----
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented_events/1.
#show causal_direct_effects/1.
#show causal_cascade_effects/1.
#show causal_preserved_events/1.
#show causal_intervention_events/1.