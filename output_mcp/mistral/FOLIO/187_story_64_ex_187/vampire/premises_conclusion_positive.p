fof(podcast_not_novel, axiom, ! [X] : (is_podcast(X) => ~is_novel(X))).
fof(born_in_american_city_implies_american, axiom, ! [P, C] : ((born_in_person_city(P, C) & is_american_city(C)) => is_american(P))).
fof(novel_written_by_implies_writer, axiom, ! [B, P] : ((is_novel(B) & written_by(B, P)) => is_novel_writer(P))).
fof(dani_shapiro_american_writer, axiom, is_american(dani_shapiro) & is_novel_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, is_novel(family_history)).
fof(dani_created_family_secrets, axiom, created_podcast(dani_shapiro, family_secrets) & is_podcast(family_secrets)).
fof(boston_american_city, axiom, is_american_city(boston)).
fof(conclusion, conjecture, born_in_person_city(dani_shapiro, boston)).