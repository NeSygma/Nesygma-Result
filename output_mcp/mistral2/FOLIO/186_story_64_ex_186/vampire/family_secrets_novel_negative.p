fof(podcast_not_novel, axiom, ! [X] : (is_podcast(X) => ~is_novel(X))).
fof(american_city_implies_american, axiom, ! [P, C] : (is_american_city(C) & born_in(P, C) => is_american(P))).
fof(novel_writer, axiom, ! [P, B] : (is_novel(B) & wrote(P, B) => is_novel_writer(P))).
fof(dani_shapiro_american_writer, axiom, is_american(dani_shapiro) & is_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, wrote(dani_shapiro, family_history)).
fof(family_history_is_novel, axiom, is_novel(family_history)).
fof(boston_american_city, axiom, is_american_city(boston)).
fof(dani_created_family_secrets, axiom, created(dani_shapiro, family_secrets) & is_podcast(family_secrets)).
fof(distinct_entities, axiom, family_history != family_secrets & family_history != boston & family_secrets != boston & dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston).

fof(conclusion_negation, conjecture, ~is_novel(family_secrets)).