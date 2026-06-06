% History Causal Analysis in ASP

% 1. Events with years
event(discovery_of_america, 1492).
event(columbian_exchange, 1500).
event(spanish_empire, 1520).
event(industrial_revolution, 1750).
event(world_wars, 1914).

% 2. Prerequisites (E requires P)
prerequisite(columbian_exchange, discovery_of_america).
prerequisite(spanish_empire, discovery_of_america).
prerequisite(industrial_revolution, spanish_empire).
prerequisite(world_wars, industrial_revolution).

% 3. Intervention: prevent discovery_of_america
intervention(discovery_of_america).

% 4. Prevented events: intervention event and any event with a prevented prerequisite
prevented(E) :- intervention(E).
prevented(E) :- prerequisite(E, P), prevented(P).

% 5. Direct effects: events immediately enabled by the prevented event
direct_effect(E) :- prerequisite(E, P), intervention(P).

% 6. Cascade effects: prevented events that are not direct effects and not the intervention event
cascade_effect(E) :- prevented(E), not direct_effect(E), not intervention(E).

% 7. Preserved events: events that are not prevented
preserved(E) :- event(E, _), not prevented(E).

% 8. Original timeline: all events in chronological order (by year)
earlier(E1, E2) :- event(E1, Y1), event(E2, Y2), Y1 < Y2.
earlier_count(E, N) :- event(E, _), N = #count{ E2 : earlier(E2, E) }.
original_position(Pos, E) :- event(E, _), earlier_count(E, N), Pos = N + 1.

% 9. Alternate timeline: preserved events in chronological order
preserved_earlier(E1, E2) :- preserved(E1), preserved(E2), earlier(E1, E2).
preserved_earlier_count(E, N) :- preserved(E), N = #count{ E2 : preserved_earlier(E2, E) }.
alternate_position(Pos, E) :- preserved(E), preserved_earlier_count(E, N), Pos = N + 1.

% 10. Output predicates
#show original_timeline/2.
#show alternate_timeline/2.
#show prevented_event/1.
#show causal_direct_effect/1.
#show causal_cascade_effect/1.
#show causal_preserved_event/1.
#show causal_intervention_event/1.

% 11. Define output atoms
original_timeline(Pos, E) :- original_position(Pos, E).
alternate_timeline(Pos, E) :- alternate_position(Pos, E).
prevented_event(E) :- prevented(E).
causal_direct_effect(E) :- direct_effect(E).
causal_cascade_effect(E) :- cascade_effect(E).
causal_preserved_event(E) :- preserved(E).
causal_intervention_event(E) :- intervention(E).