fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(novel_writer_rule, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(dani_shapiro_facts, axiom, (american(dani_shapiro) & writer(dani_shapiro))).
fof(family_history_written_by, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(dani_shapiro_podcast, axiom, (created(dani_shapiro, family_secrets) & podcast(family_secrets))).
fof(boston_is_american_city, axiom, american_city(boston)).
fof(distinct_entities, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(goal, conjecture, novel_writer(dani_shapiro)).