fof(known_as_ailton, axiom, known_as(ailton_silva, ailton)).
fof(football_player, axiom, football_player(ailton_silva)).
fof(loaned_to_braga, axiom, loaned_to(ailton_silva, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_nautico, axiom, is_club(nautico)).
fof(club_braga, axiom, is_club(braga)).
fof(club_fluminense, axiom, is_club(fluminense)).
fof(distinct_clubs, axiom, (nautico != braga & nautico != fluminense & braga != fluminense)).
fof(goal, conjecture, played_for(ailton_silva, fluminense)).