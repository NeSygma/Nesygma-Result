fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_american_city, axiom, ! [X] : (born_in_american_city(X) => american(X))).
fof(book_novel_writer, axiom, ! [X,Y] : ((book(X) & novel(X) & writtenBy(X,Y)) => novel_writer(Y))).
fof(dani_shapiro_american, axiom, american(dani_shapiro)).
fof(written_by_dani_shapiro, axiom, writtenBy(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(podcast_family_secrets, axiom, podcast(family_secrets)).
fof(boston_is_american, axiom, american(boston)).
fof(distinct_constants, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
fof(conjecture, conjecture, novel_writer(dani_shapiro)).