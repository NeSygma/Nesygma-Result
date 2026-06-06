fof(ailton_silva_is_footballer, axiom, is_football_player(ailton_silva)).
fof(ailton_plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(nautico_is_club, axiom, is_football_club(nautico)).
fof(braga_is_club, axiom, is_football_club(braga)).
fof(fluminense_is_club, axiom, is_football_club(fluminense)).
fof(distinct_entities, axiom, (ailton_silva != nautico & ailton_silva != braga & ailton_silva != fluminense & nautico != braga & nautico != fluminense & braga != fluminense)).
fof(goal, conjecture, ? [C] : (is_football_club(C) & plays_for(ailton_silva, C))).