fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(american_city_born, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(novel_writer_rule, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(dani_american_writer, axiom, (american(dani_shapiro) & writer(dani_shapiro))).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(dani_created_family_secrets, axiom, (created(dani_shapiro, family_secrets) & podcast(family_secrets))).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, novel_writer(dani_shapiro)).