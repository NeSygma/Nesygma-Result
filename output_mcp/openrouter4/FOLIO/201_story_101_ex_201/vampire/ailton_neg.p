% Negative file: negated claim as conjecture
% Negation: There exists a football club C such that Ailton was loaned out to C.

fof(distinct_entities, axiom,
    (ailton != braga & ailton != nautico & ailton != fluminense
    & braga != nautico & braga != fluminense & nautico != fluminense)).

fof(premise_1, axiom,
    ailton = ailton_silva).

fof(premise_2, axiom,
    football_player(ailton)).

fof(premise_2b, axiom,
    loaned_out_to(ailton, braga)).

fof(premise_3, axiom,
    brazilian(ailton)).

fof(premise_3b, axiom,
    plays_for(ailton, nautico)).

fof(premise_4, axiom,
    football_club(nautico)).

fof(premise_4b, axiom,
    football_club(braga)).

fof(premise_5, axiom,
    football_club(fluminense)).

% Negated conclusion: There exists a football club C such that Ailton was loaned out to C.
fof(negated_conclusion, conjecture,
    ? [C] : (football_club(C) & loaned_out_to(ailton, C))).