fof(ailton_silva_identity, axiom, ailton_silva = ailton).
fof(ailton_plays_for_braga, axiom, plays_for(ailton, braga)).
fof(ailton_silva_plays_for_nautico, axiom, plays_for(ailton_silva, nautico)).
fof(braga_is_club, axiom, football_club(braga)).
fof(nautico_is_club, axiom, football_club(nautico)).
fof(fluminense_is_club, axiom, football_club(fluminense)).
fof(distinct_entities, axiom, (ailton_silva != braga & ailton_silva != nautico & ailton_silva != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(conclusion_negation, conjecture, ? [C] : (football_club(C) & plays_for(ailton_silva, C))).