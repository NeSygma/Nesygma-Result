% Positive file: original claim as conjecture
% Claim: Ailton was not loaned out to a football club.
% i.e., for all C, if C is a football club then Ailton was not loaned out to C.

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

% Conclusion: Ailton was not loaned out to a football club.
fof(conclusion, conjecture,
    ! [C] : (football_club(C) => ~loaned_out_to(ailton, C))).