% Negative version (negated claim)
fof(premise1, axiom, sporting_event(summer_olympic_games)).
fof(premise2, axiom, location_of(summer_olympic_games, tokyo)).
fof(premise3, axiom, won_most_medals(united_states, tokyo)).
fof(rule1, axiom, ! [C,E,L] : (location_of(E,L) & won_most_medals(C,L) => won_most_medals(C,E))).
fof(distinct1, axiom, united_states != tokyo).
fof(distinct2, axiom, united_states != summer_olympic_games).
fof(distinct3, axiom, tokyo != summer_olympic_games).
fof(goal, conjecture, ~won_most_medals(united_states, summer_olympic_games)).