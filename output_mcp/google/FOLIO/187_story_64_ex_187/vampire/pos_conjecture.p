fof(p1, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(p2, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(p3, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(p4, axiom, (american(dani_shapiro) & writer(dani_shapiro))).
fof(p5, axiom, written_by(family_history, dani_shapiro)).
fof(p6, axiom, novel(family_history)).
fof(p7, axiom, (created(dani_shapiro, family_secrets) & podcast(family_secrets))).
fof(p8, axiom, american_city(boston)).
fof(goal, conjecture, born_in(dani_shapiro, boston)).