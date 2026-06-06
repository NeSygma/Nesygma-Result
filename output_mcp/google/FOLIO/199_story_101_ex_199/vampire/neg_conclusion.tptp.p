fof(ailton_silva_is_brazilian, axiom, is_brazilian(ailton_silva)).
fof(ailton_silva_plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(nautico_is_club, axiom, is_football_club(nautico)).
fof(braga_is_club, axiom, is_football_club(braga)).
fof(fluminense_is_club, axiom, is_football_club(fluminense)).
fof(distinct_entities, axiom, (ailton_silva != nautico & ailton_silva != braga & ailton_silva != fluminense & nautico != braga & nautico != fluminense & braga != fluminense)).
fof(negated_conclusion, conjecture, ? [X] : (plays_for(X, nautico) & is_brazilian(X))).