fof(distinct, axiom, (dani_shapiro != boston & dani_shapiro != family_history & dani_shapiro != family_secrets & boston != family_history & boston != family_secrets & family_history != family_secrets)).
fof(rule_podcast_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(rule_born_american, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(rule_novel_writer, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(fact_podcast, axiom, podcast(family_secrets)).
fof(fact_novel, axiom, novel(family_history)).
fof(fact_written_by, axiom, written_by(family_history, dani_shapiro)).
fof(fact_american_city, axiom, american_city(boston)).
fof(fact_american_writer, axiom, american_writer(dani_shapiro)).
fof(goal, conjecture, ~born_in(dani_shapiro, boston)).