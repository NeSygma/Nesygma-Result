fof(podcast_not_novel, axiom,
    ! [X] : (podcast(X) => ~novel(X))).

fof(american_city_born, axiom,
    ! [X, Y] : ((person(X) & american_city(Y) & born_in(X, Y)) => american(X))).

fof(novel_writer_rule, axiom,
    ! [X, Y] : ((book(X) & novel(X) & person(Y) & written_by(X, Y)) => novel_writer(Y))).

fof(dani_is_american, axiom, american(dani_shapiro)).
fof(dani_is_writer, axiom, writer(dani_shapiro)).
fof(dani_is_person, axiom, person(dani_shapiro)).

fof(family_history_written_by_dani, axiom,
    written_by(family_history, dani_shapiro)).

fof(family_history_is_novel, axiom, novel(family_history)).
fof(family_history_is_book, axiom, book(family_history)).

fof(dani_created_family_secrets, axiom,
    created(dani_shapiro, family_secrets)).
fof(family_secrets_is_podcast, axiom, podcast(family_secrets)).

fof(boston_is_american_city, axiom, american_city(boston)).

fof(goal, conjecture, novel_writer(dani_shapiro)).