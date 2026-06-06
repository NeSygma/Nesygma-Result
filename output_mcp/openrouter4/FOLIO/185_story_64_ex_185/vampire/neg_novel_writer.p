fof(premise_1, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(premise_2, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(premise_3, axiom, ! [B, P] : ((book(B) & novel(B) & written_by(B, P)) => novel_writer(P))).
fof(premise_4, axiom, american(dani_shapiro)).
fof(premise_4b, axiom, writer(dani_shapiro)).
fof(premise_5, axiom, written_by(family_history, dani_shapiro)).
fof(premise_6, axiom, novel(family_history)).
fof(premise_6b, axiom, written_in(family_history, year_2003)).
fof(premise_7, axiom, created(dani_shapiro, family_secrets)).
fof(premise_7b, axiom, podcast(family_secrets)).
fof(premise_8, axiom, american_city(boston)).
fof(distinct, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & dani_shapiro != year_2003 & family_history != family_secrets & family_history != boston & family_history != year_2003 & family_secrets != boston & family_secrets != year_2003 & boston != year_2003)).
fof(goal, conjecture, ~novel_writer(dani_shapiro)).