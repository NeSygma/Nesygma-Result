fof(prem1, axiom, striker(robert_lewandowski)).
fof(prem2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(prem3, axiom, leaves(robert_lewandowski, bayern_munchen)).
fof(prem4, axiom, ! [X,Y] : (leaves(X,Y) => ~plays_for(X, bayern_munchen))).
fof(conjecture, conjecture, ~plays_for(robert_lewandowski, bayern_munchen)).