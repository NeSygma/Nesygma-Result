fof(plays_braga, axiom, plays_for(ailton, braga)).
fof(plays_nautico, axiom, plays_for(ailton, nautico)).
fof(brazilian_ailton, axiom, brazilian(ailton)).
fof(distinctness, axiom, (ailton != braga & ailton != nautico & ailton != fluminense & braga != nautico & braga != fluminense & nautico != fluminense)).
fof(conjecture, conjecture, ? [X] : (plays_for(X, nautico) & brazilian(X))).