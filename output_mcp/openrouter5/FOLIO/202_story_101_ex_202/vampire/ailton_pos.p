% Positive version: original claim as conjecture
% Premises:

% Ailton Silva, born in 1995, is commonly known as Ailton.
fof(premise_1, axiom, ailton_silva = ailton).
fof(premise_1b, axiom, born_in_1995(ailton_silva)).

% Ailton is a football player who was loaned out to Braga.
fof(premise_2, axiom, football_player(ailton)).
fof(premise_2b, axiom, loaned_to(ailton, braga)).

% Ailton Silva is a Brazilian footballer who plays for Náutico.
fof(premise_3, axiom, brazilian_footballer(ailton_silva)).
fof(premise_3b, axiom, plays_for(ailton_silva, nautico)).

% Náutico is a football club along with Braga.
fof(premise_4, axiom, football_club(nautico)).
fof(premise_4b, axiom, football_club(braga)).

% Fluminense is a football club.
fof(premise_5, axiom, football_club(fluminense)).

% Distinctness
fof(distinct_clubs, axiom, (nautico != braga & nautico != fluminense & braga != fluminense)).

% Conclusion: Ailton Silva played for Fluminense.
fof(goal, conjecture, played_for(ailton_silva, fluminense)).