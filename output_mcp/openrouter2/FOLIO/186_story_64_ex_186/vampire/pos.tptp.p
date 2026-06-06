fof(distinct, axiom, (family_history != family_secrets & family_history != dani_shapiro & family_history != boston & family_secrets != dani_shapiro & family_secrets != boston & dani_shapiro != boston)).
fof(rule1, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(rule2, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(rule3, axiom, ! [B, P] : ((book(B) & novel(B) & written_by(B, P)) => novel_writer(P))).
fof(fact1, axiom, born_in(dani_shapiro, boston)).
fof(fact2, axiom, american_city(boston)).
fof(fact3, axiom, american(dani_shapiro)).
fof(fact4, axiom, writer(dani_shapiro)).
fof(fact5, axiom, written_by(family_history, dani_shapiro)).
fof(fact6, axiom, novel(family_history)).
fof(fact7, axiom, book(family_history)).
fof(fact8, axiom, podcast(family_secrets)).
fof(fact9, axiom, created_podcast(dani_shapiro, family_secrets)).
fof(goal, conjecture, novel(family_secrets)).