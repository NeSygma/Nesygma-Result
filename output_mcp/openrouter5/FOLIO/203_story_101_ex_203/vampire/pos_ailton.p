% Positive version: original conclusion as conjecture
% Ailton Silva was loaned out to a football club.

% Ailton Silva, born in 1995, is commonly known as Ailton.
fof(fact_1, axiom, ailton_silva = ailton).

% Ailton is a football player who was loaned out to Braga.
fof(fact_2, axiom, football_player(ailton)).
fof(fact_3, axiom, loaned_to(ailton, braga)).

% Ailton Silva is a Brazilian footballer who plays for Náutico.
fof(fact_4, axiom, brazilian_footballer(ailton_silva)).
fof(fact_5, axiom, plays_for(ailton_silva, nautico)).

% Náutico is a football club along with Braga.
fof(fact_6, axiom, football_club(nautico)).
fof(fact_7, axiom, football_club(braga)).

% Fluminense is a football club.
fof(fact_8, axiom, football_club(fluminense)).

% Distinctness
fof(distinct, axiom, (braga != nautico & braga != fluminense & nautico != fluminense)).

% Conclusion: Ailton Silva was loaned out to a football club.
% Since ailton_silva = ailton, and loaned_to(ailton, braga) and football_club(braga),
% it follows that there exists a football club X such that loaned_to(ailton_silva, X).
fof(goal, conjecture, ? [X] : (football_club(X) & loaned_to(ailton_silva, X))).