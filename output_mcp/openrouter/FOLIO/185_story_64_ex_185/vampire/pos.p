% Positive version
fof(distinct, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_american, axiom, ! [P,C] : ((born_in(P,C) & american_city(C)) => american(P))).
fof(novel_writer_rule, axiom, ! [B,P] : ((novel(B) & written_by(B,P)) => novel_writer(P))).
fof(american_writer, axiom, american(dani_shapiro)).
fof(written_by_fh, axiom, written_by(family_history, dani_shapiro)).
fof(fh_is_novel, axiom, novel(family_history)).
fof(created_podcast, axiom, (created(dani_shapiro, family_secrets) & podcast(family_secrets))).
fof(boston_american_city, axiom, american_city(boston)).
fof(goal, conjecture, novel_writer(dani_shapiro)).