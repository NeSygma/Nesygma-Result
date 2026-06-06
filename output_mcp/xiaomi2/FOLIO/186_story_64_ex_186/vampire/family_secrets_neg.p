fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(american_if_born, axiom, ! [X, Y] : ((person(X) & born_in(X, Y) & american_city(Y)) => american(X))).
fof(novel_writer_rule, axiom, ! [X, Y] : ((book(X) & novel(X) & written_by(X, Y) & person(Y)) => novel_writer(Y))).
fof(dani_shapiro_american_writer, axiom, (american(dani_shapiro) & writer(dani_shapiro) & person(dani_shapiro))).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_novel, axiom, (novel(family_history) & book(family_history))).
fof(dani_created_family_secrets, axiom, (created(dani_shapiro, family_secrets) & podcast(family_secrets))).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, ~novel(family_secrets)).