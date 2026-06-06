% Negative file: Family Secrets is NOT a novel
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city, axiom, ! [X, Y] : (born_in(X, Y) & american_city(Y) => american(X))).
fof(novel_writer_rule, axiom, ! [X, Y] : (novel(X) & written_by(X, Y) => novel_writer(Y))).
fof(dani_shapiro_american, axiom, american(dani_shapiro)).
fof(dani_shapiro_writer, axiom, writer(dani_shapiro)).
fof(family_history_written_by, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_novel, axiom, novel(family_history)).
fof(dani_shapiro_created_family_secrets, axiom, created(dani_shapiro, family_secrets)).
fof(family_secrets_podcast, axiom, podcast(family_secrets)).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, ~novel(family_secrets)).