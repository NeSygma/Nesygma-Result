% --- Facts: Events ---
event(discovery_of_america, "Discovery of America", 1492).
event(columbian_exchange, "Columbian Exchange", 1500).
event(spanish_empire, "Spanish Empire", 1520).
event(industrial_revolution, "Industrial Revolution", 1750).
event(world_wars, "World Wars", 1914).

% --- Facts: Prerequisites ---
requires(columbian_exchange, discovery_of_america).
requires(spanish_empire, discovery_of_america).
requires(industrial_revolution, spanish_empire).
requires(world_wars, industrial_revolution).

% --- Facts: Enabling Relationships ---
enables(discovery_of_america, columbian_exchange).
enables(discovery_of_america, spanish_empire).
enables(spanish_empire, industrial_revolution).
enables(industrial_revolution, world_wars).

% --- Intervention ---
intervention(discovery_of_america).

% --- Original Timeline (sorted by year) ---
% Sort events by year and assign order.
time(1..5).
event_order(E, T) :- event(E, _, Y), time(T), Y = 1492 + (T-1)*28.
original_timeline(E) :- event_order(E, _).

% --- Prevented Events ---
% The intervention prevents the specified event.
prevented(E) :- intervention(E).

% If an event is prevented, all events that require it are also prevented (cascade).
prevented(E2) :- requires(E2, E1), prevented(E1).

% --- Preserved Events ---
% An event is preserved if it is not prevented.
preserved(E) :- event(E, _, _), not prevented(E).

% --- Direct Effects ---
% Direct effects are events enabled by the prevented event.
direct_effect(E) :- enables(E1, E), intervention(E1).

% --- Cascade Effects ---
% Cascade effects are events prevented due to dependency chains.
cascade_effect(E) :- prevented(E), not intervention(E).

% --- Alternate Timeline ---
% An event is in the alternate timeline if it is preserved and all its prerequisites are preserved.
alternate_timeline(E) :- preserved(E), not cascade_effect(E).

% --- Intervention Events ---
intervention_event(E) :- intervention(E).

% --- #show Directives ---
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented/1.
#show direct_effect/1.
#show cascade_effect/1.
#show preserved/1.
#show intervention_event/1.