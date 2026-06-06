fof(ailton_silva_known_as_ailton, axiom,
    commonly_known_as(ailton_silva, ailton)).

fof(identity_rule, axiom,
    ! [X, Y] : (commonly_known_as(X, Y) => (X = Y))).

fof(ailton_football_player, axiom,
    football_player(ailton)).

fof(ailton_loaned_to_braga, axiom,
    loaned_out_to(ailton, braga)).

fof(ailton_silva_brazilian, axiom,
    brazilian_footballer(ailton_silva)).

fof(ailton_silva_plays_for_nautico, axiom,
    plays_for(ailton_silva, nautico)).

fof(nautico_is_club, axiom,
    football_club(nautico)).

fof(braga_is_club, axiom,
    football_club(braga)).

fof(fluminense_is_club, axiom,
    football_club(fluminense)).

% Conclusion: Ailton was NOT loaned out to a football club
fof(goal, conjecture,
    ~? [C] : (football_club(C) & loaned_out_to(ailton, C))).