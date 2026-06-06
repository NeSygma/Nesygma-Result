% Negative file: Negated claim as conjecture
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city_makes_american, axiom, ! [X, Y] : (born_in(X, Y) & american_city(Y) => american(X))).
fof(novel_writer_rule, axiom, ! [X, Y] : (novel(X) & written_by(X, Y) => novel_writer(Y))).
fof(dani_shapiro_american_writer, axiom, american(dani_shapiro) & writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_novel, axiom, novel(family_history)).
fof(dani_created_family_secrets, axiom, podcast(family_secrets) & created(dani_shapiro, family_secrets)).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, ~born_in(dani_shapiro, boston)).