% Positive conjecture: Family Secrets is a novel
fof(distinct_entities, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(podcast_not_novel, axiom, ![X] : (podcast(X) => ~novel(X))).
fof(born_american, axiom, ![P,C] : (born_in(P,C) & american_city(C) => american(P))).
fof(novel_writer_rule, axiom, ![B,P] : (novel(B) & written_by(B,P) => novel_writer(P))).
fof(dani_american, axiom, american(dani_shapiro)).
fof(dani_writer, axiom, writer(dani_shapiro)).
fof(fh_written_by, axiom, written_by(family_history, dani_shapiro)).
fof(fh_is_novel, axiom, novel(family_history)).
fof(family_secrets_podcast, axiom, podcast(family_secrets)).
fof(dani_created_fs, axiom, created(dani_shapiro, family_secrets)).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, novel(family_secrets)).