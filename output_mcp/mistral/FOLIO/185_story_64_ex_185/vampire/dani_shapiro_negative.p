fof(podcast_not_novel, axiom, ! [X] : (is_podcast(X) => ~is_novel(X))).
fof(born_in_american_city_implies_american, axiom, ! [Person, City] : ((born_in_city(Person, City) & is_american_city(City)) => is_american(Person))).
fof(novel_and_written_by_implies_writer, axiom, ! [Book, Person] : ((is_novel(Book) & written_by(Book, Person)) => is_novel_writer(Person))).
fof(dani_shapiro_is_american_writer, axiom, is_american(dani_shapiro) & is_writer(dani_shapiro)).
fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).
fof(family_history_is_novel, axiom, is_novel(family_history)).
fof(family_history_created_by_dani, axiom, created_podcast(dani_shapiro, family_secrets)).
fof(family_secrets_is_podcast, axiom, is_podcast(family_secrets)).
fof(boston_is_american_city, axiom, is_american_city(boston)).
fof(conclusion_negation, conjecture, ~is_novel_writer(dani_shapiro)).