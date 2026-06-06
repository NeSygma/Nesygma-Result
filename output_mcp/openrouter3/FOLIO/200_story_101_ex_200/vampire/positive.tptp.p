% Premises about Ailton Silva and football clubs
fof(premise_1, axiom, football_player(ailton_silva)).
fof(premise_2, axiom, plays_for(ailton_silva, nautico)).
fof(premise_3, axiom, loaned_to(ailton_silva, braga)).
fof(premise_4, axiom, football_club(nautico)).
fof(premise_5, axiom, football_club(braga)).
fof(premise_6, axiom, football_club(fluminense)).

% Distinctness axioms
fof(distinct_clubs, axiom, (nautico != braga & nautico != fluminense & braga != fluminense)).

% Conclusion to evaluate: Ailton Silva does not play for a football club
fof(goal, conjecture, ~plays_for(ailton_silva, nautico)).