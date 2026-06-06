fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(american_city_implies_american, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(novel_writer_implies, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(dani_shapiro_american_writer, axiom, american(dani_shapiro) & novel_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_novel, axiom, novel(family_history)).
fof(dani_created_family_secrets, axiom, created(dani_shapiro, family_secrets)).
fof(boston_american_city, axiom, american_city(boston)).
fof(podcast_family_secrets, axiom, podcast(family_secrets)).

fof(conclusion_negation, conjecture, ~born_in(dani_shapiro, boston)).