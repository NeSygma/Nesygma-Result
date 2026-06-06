% Positive file: original claim "Ailton Silva played for Fluminense" as conjecture
fof(distinct_clubs, axiom, (braga != nautico & braga != fluminense & nautico != fluminense)).
fof(same_person, axiom, ailton_silva = ailton).
fof(football_player, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(club_nautico, axiom, football_club(nautico)).
fof(club_braga, axiom, football_club(braga)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(conclusion, conjecture, plays_for(ailton_silva, fluminense)).