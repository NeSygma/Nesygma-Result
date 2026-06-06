fof(ailton_is_ailton_silva, axiom,
    ailton = ailton_silva).

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

fof(distinct_clubs, axiom,
    (braga != nautico & braga != fluminense & nautico != fluminense)).

fof(goal, conjecture,
    ~? [C] : (loaned_out_to(ailton_silva, C) & football_club(C))).