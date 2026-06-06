% Historical Causality Analysis
% ==============================

% --- Events ---
% event(ID, name, year)
event(discovery_of_america, "Discovery of America", 1492).
event(columbian_exchange, "Columbian Exchange", 1500).
event(spanish_empire, "Spanish Empire", 1520).
event(industrial_revolution, "Industrial Revolution", 1750).
event(world_wars, "World Wars", 1914).

% --- Dependencies ---
% requires(Event, PrerequisiteEvent)
requires(columbian_exchange, discovery_of_america).
requires(spanish_empire, discovery_of_america).
requires(industrial_revolution, spanish_empire).
requires(world_wars, industrial_revolution).

% enables(EnablingEvent, EnabledEvent)
enables(discovery_of_america, columbian_exchange).
enables(discovery_of_america, spanish_empire).
enables(spanish_empire, industrial_revolution).
enables(industrial_revolution, world_wars).

% --- Intervention ---
% The intervention prevents discovery_of_america
prevented(discovery_of_america).

% --- Direct Effects ---
% Events directly prevented because their enabling event is prevented
direct_effect(E) :-
    enables(PreventedEvent, E),
    prevented(PreventedEvent),
    event(E, _, _).

% --- Cascade Effects ---
% Events prevented because their prerequisite is prevented
% Base case: events with prevented prerequisites
cascade_effect(E) :-
    requires(E, P),
    prevented(P),
    event(E, _, _),
    not direct_effect(E).

% Recursive case: events that require cascade-prevented events
cascade_effect(E) :-
    requires(E, P),
    cascade_effect(P),
    event(E, _, _),
    not direct_effect(E),
    not prevented(E).

% --- All Prevented Events ---
% An event is prevented if it's directly prevented, a direct effect, or a cascade effect
prevented(E) :-
    direct_effect(E).
prevented(E) :-
    cascade_effect(E).

% --- Preserved Events ---
% Events that are not prevented
preserved_event(E) :-
    event(E, _, _),
    not prevented(E).

% --- Intervention Events ---
% Events directly prevented by intervention
intervention_event(discovery_of_america).

% --- Original Timeline ---
% In the original timeline, all events occur in chronological order
% Base case: first event in chronological order
original_timeline(discovery_of_america).

% Events after the first in chronological order
original_timeline(E) :-
    event(E, _, Year),
    event(_, _, PrevYear),
    Year > PrevYear.

% --- Alternate Timeline ---
% In the alternate timeline, only preserved events with all prerequisites satisfied occur
% Base case: preserved events with no prerequisites
alternate_timeline(E) :-
    preserved_event(E),
    not requires(E, _).

% Recursive case: preserved events whose prerequisites are also preserved
alternate_timeline(E) :-
    preserved_event(E),
    requires(E, P),
    alternate_timeline(P).

% --- Show directives ---
#show original_timeline/1.
#show alternate_timeline/1.
#show prevented/1.
#show direct_effect/1.
#show cascade_effect/1.
#show preserved_event/1.
#show intervention_event/1.