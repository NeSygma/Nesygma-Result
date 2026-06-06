% Positive version: original conclusion as conjecture
% Conclusion: Ailton was not loaned out to a football club.
% Formalized as: ~loaned_to_football_club(ailton)

fof(distinct, axiom, (ailton != braga & ailton != naurico & ailton != fluminense & braga != naurico & braga != fluminense & naurico != fluminense)).

% Ailton Silva, born in 1995, is commonly known as Ailton.
fof(known_as, axiom, ailton_silva = ailton).

% Ailton is a football player who was loaned out to Braga.
fof(is_player, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_to(ailton, braga)).

% Ailton Silva is a Brazilian footballer who plays for Náutico.
fof(plays_for_naurico, axiom, plays_for(ailton, naurico)).

% Náutico is a football club along with Braga.
fof(naurico_is_club, axiom, football_club(naurico)).
fof(braga_is_club, axiom, football_club(braga)).

% Fluminense is a football club.
fof(fluminense_is_club, axiom, football_club(fluminense)).

% Define: being loaned out to a football club
fof(loaned_to_club, axiom, ! [X, C] : ((loaned_to(X, C) & football_club(C)) => loaned_to_football_club(X))).

% Conclusion: Ailton was not loaned out to a football club.
fof(goal, conjecture, ~loaned_to_football_club(ailton)).