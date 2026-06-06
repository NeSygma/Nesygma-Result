fof(p1, axiom, born_in_1995(ailton_silva)).
fof(p2, axiom, commonly_known_as(ailton_silva, ailton)).
fof(p3, axiom, football_player(ailton)).
fof(p4, axiom, loaned_to(ailton, braga)).
fof(p5, axiom, brazilian_footballer(ailton_silva)).
fof(p6, axiom, plays_for(ailton_silva, nautico)).
fof(p7, axiom, football_club(nautico)).
fof(p8, axiom, football_club(braga)).
fof(p9, axiom, football_club(fluminense)).

fof(distinct, axiom, (
    ailton_silva != ailton &
    ailton_silva != braga &
    ailton_silva != nautico &
    ailton_silva != fluminense &
    ailton != braga &
    ailton != nautico &
    ailton != fluminense &
    braga != nautico &
    braga != fluminense &
    nautico != fluminense
)).

% Conclusion: Ailton Silva does not play for a football club.
fof(goal, conjecture, ~? [C] : (plays_for(ailton_silva, C) & football_club(C))).