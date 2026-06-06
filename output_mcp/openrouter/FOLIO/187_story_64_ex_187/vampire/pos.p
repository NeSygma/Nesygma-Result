% Positive conjecture: Dani Shapiro was born in Boston.
fof(distinct, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(rule_podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(rule_born_american, axiom, ! [P,C] : (born_in(P,C) & american_city(C) => american(P))).
fof(rule_novel_writer, axiom, ! [W,P] : (novel(W) & written_by(W,P) => novel_writer(P))).
fof(fact_american_writer, axiom, american(dani_shapiro)).
fof(fact_writer, axiom, writer(dani_shapiro)).
fof(fact_written, axiom, written_by(family_history, dani_shapiro)).
fof(fact_novel, axiom, novel(family_history)).
fof(fact_podcast, axiom, podcast(family_secrets)).
fof(fact_american_city, axiom, american_city(boston)).
fof(goal, conjecture, born_in(dani_shapiro, boston)).