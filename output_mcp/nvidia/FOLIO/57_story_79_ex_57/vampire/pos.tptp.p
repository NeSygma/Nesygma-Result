fof(prem1, axiom, striker(robert_lewandowski)).
fof(prem2, axiom, ! [X] : (~striker(X) | soccer_player(X))).
fof(prem3, axiom, left(robert_lewandowski, bayern_munchen)).
fof(prem4, axiom, ! [X,Y] : (~left(X,Y) | ~plays_for(X,Y))).
fof(conjecture, conjecture, star(robert_lewandowski)).