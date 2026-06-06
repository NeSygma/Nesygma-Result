% Negative file: Dani Shapiro is NOT a novel writer
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city_makes_american, axiom, ! [X, Y] : (born_in(X, Y) & american_city(Y) => american(X))).
fof(novel_writer_rule, axiom, ! [X, Y] : (novel(X) & written_by(X, Y) => novel_writer(Y))).
fof(dani_shapiro_american_writer, axiom, american(dani_shapiro) & writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(dani_created_family_secrets, axiom, podcast(family_secrets) & created(dani_shapiro, family_secrets)).
fof(boston_american_city, axiom, american_city(boston)).
fof(distinct_entities, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & family_history != family_secrets & boston != dani_shapiro & boston != family_history & boston != family_secrets)).
fof(goal, conjecture, ~novel_writer(dani_shapiro)).