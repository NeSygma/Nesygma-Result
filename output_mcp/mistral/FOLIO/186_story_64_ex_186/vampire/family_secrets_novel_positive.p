fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city_implies_american, axiom, ! [P, C] : (born_in(P, C) & american_city(C) => american(P))).
fof(novel_and_written_by_implies_writer, axiom, ! [B, P] : ((book(B) & novel(B) & written_by(B, P)) => novel_writer(P))).
fof(dani_shapiro_is_american_writer, axiom, american_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(family_history_is_book, axiom, book(family_history)).
fof(family_secrets_is_podcast, axiom, podcast(family_secrets)).
fof(family_secrets_created, axiom, created(dani_shapiro, family_secrets)).
fof(boston_is_american_city, axiom, american_city(boston)).
fof(distinct_works, axiom, family_history != family_secrets).
fof(conclusion, conjecture, novel(family_secrets)).