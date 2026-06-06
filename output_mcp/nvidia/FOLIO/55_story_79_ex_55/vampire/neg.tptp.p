fof(prem1, axiom, striker(rl)).
fof(prem2, axiom, ! [X] : (striker(X) => soccer_player(X))).
fof(prem3, axiom, left(rl, bayern_munchen)).
fof(prem4, axiom, ! [X,Y] : (left(X,Y) => ~plays_for(X,Y))).
fof(goal, conjecture, ~soccer_player(rl)).