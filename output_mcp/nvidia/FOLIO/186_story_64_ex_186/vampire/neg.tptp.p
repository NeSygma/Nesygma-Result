fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_implies_american, axiom, ! [X] : (born_in(X, american_city) => american(X))).
fof(book_novel_writer_implies_writer, axiom, ! [X,Y] : ((book(X) & novel(X) & written_by(X,Y)) => writer(Y))).
fof(dani_shapiro_writer, axiom, writer(dani_shapiro)).
fof(dani_shapiro_american, axiom, american(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, novel(family_history)).
fof(family_history_is_book, axiom, book(family_history)).
fof(family_secrets_is_podcast, axiom, podcast(family_secrets)).
fof(boston_is_american_city, axiom, american_city_prop(boston)).
fof(conclusion, conjecture, ~novel(family_secrets)).