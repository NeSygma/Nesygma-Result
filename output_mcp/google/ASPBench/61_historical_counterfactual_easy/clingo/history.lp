% --- Instance Data ---
event(discovery_of_america, 1492).
event(columbian_exchange, 1500).
event(spanish_empire, 1520).
event(industrial_revolution, 1750).
event(world_wars, 1914).

prerequisite(columbian_exchange, discovery_of_america).
prerequisite(spanish_empire, discovery_of_america).
prerequisite(industrial_revolution, spanish_empire).
prerequisite(world_wars, industrial_revolution).

intervention(discovery_of_america).

% --- Logic ---

% 1. Original timeline: All events
original_timeline(E) :- event(E, _).

% 2. Prevented events:
% Directly prevented by intervention
prevented(E) :- intervention(E).
% Cascade: Any event with a prevented prerequisite is also prevented
prevented(E) :- prerequisite(E, P), prevented(P).

% 3. Alternate timeline: Events that are not prevented
alternate_timeline(E) :- event(E, _), not prevented(E).

% 4. Causal Analysis
% Direct effects: Events immediately enabled by the prevented event
direct_effect(E) :- intervention(I), prerequisite(E, I).

% Cascade effects: Events prevented indirectly through dependency chains
% (Prevented, but not the intervention itself and not a direct effect)
cascade_effect(E) :- prevented(E), not intervention(E), not direct_effect(E).

% Preserved events: Events that remain in the alternate timeline
preserved(E) :- event(E, _), not prevented(E).

% --- Output Mapping ---
original_timeline_out(E) :- original_timeline(E).
alternate_timeline_out(E) :- alternate_timeline(E).
prevented_events_out(E) :- prevented(E).
direct_effects_out(E) :- direct_effect(E).
cascade_effects_out(E) :- cascade_effect(E).
preserved_events_out(E) :- preserved(E).
intervention_events_out(E) :- intervention(E).

#show original_timeline_out/1.
#show alternate_timeline_out/1.
#show prevented_events_out/1.
#show direct_effects_out/1.
#show cascade_effects_out/1.
#show preserved_events_out/1.
#show intervention_events_out/1.