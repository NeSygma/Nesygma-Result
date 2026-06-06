fof(p1, axiom, ! [X] : (at_mixer(X) => (gsc(X) | ona(X)))).
fof(p2, axiom, ! [X] : ((at_mixer(X) & gsc(X)) => ptp(X))).
fof(p3, axiom, ! [X] : ((at_mixer(X) & ona(X)) => cel(X))).
fof(p4, axiom, ! [X] : ((at_mixer(X) & ptp(X)) => ath(X))).
fof(p5, axiom, ! [X] : ((at_mixer(X) & cel(X)) => wp(X))).
fof(p6, axiom, ! [X] : ((at_mixer(X) & ath(X)) => fam(X))).
fof(p7, axiom, ! [X] : ((at_mixer(X) & wp(X)) => lth(X))).
fof(p8, axiom, at_mixer(djokovic)).
fof(p9, axiom, ((fam(djokovic) & ath(djokovic)) => wp(djokovic))).
fof(goal, conjecture, gsc(djokovic)).