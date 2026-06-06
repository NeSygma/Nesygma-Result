fof(ailton_is_ailton_silva, axiom,
    ailton = ailton_silva).

fof(premise_2, axiom,
    (football_player(ailton) & loaned_out_to(ailton, braga))).

fof(premise_3, axiom,
    (footballer(ailton_silva) & plays_for(ailton_silva, nautico))).

fof(premise_4, axiom,
    (football_club(nautico) & football_club(braga))).

fof(premise_5, axiom,
    football_club(fluminense)).

fof(conclusion, conjecture,
    ! [X] : (football_club(X) => ~loaned_out_to(ailton, X))).