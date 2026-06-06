% Positive run: original conclusion as conjecture
% "Ailton Silva does not play for a football club"
fof(known_as, axiom, ailton_silva = ailton).
fof(football_player, axiom, football_player(ailton)).
fof(loaned_to_braga, axiom, loaned_to(ailton, braga)).
fof(plays_for_naurico, axiom, plays_for(ailton_silva, naurico)).
fof(club_naurico, axiom, football_club(naurico)).
fof(club_braga, axiom, football_club(braga)).
fof(club_fluminense, axiom, football_club(fluminense)).
fof(distinct, axiom, (ailton_silva != naurico & ailton_silva != braga & ailton_silva != fluminense & naurico != braga & naurico != fluminense & braga != fluminense)).
fof(goal, conjecture, ~? [C] : (football_club(C) & plays_for(ailton_silva, C))).