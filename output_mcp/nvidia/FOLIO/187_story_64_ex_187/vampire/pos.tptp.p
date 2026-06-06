% Axioms
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(born_in_implies_american, axiom, ! [X,Y] : (born_in(X,Y) => american(X))).
fof(book_novel_writer, axiom, ! [X,Y] : ((book(X) & novel(X) & written_by(X,Y)) => novel_writer(Y))).
fof(american_dani, axiom, american(dani_shapiro)).
fof(writer_dani, axiom, writer(dani_shapiro)).
fof(written_by_family_history, axiom, written_by(family_history, dani_shapiro)).
fof(book_family_history, axiom, book(family_history)).
fof(novel_family_history, axiom, novel(family_history)).
fof(podcast_family_secrets, axiom, podcast(family_secrets)).
fof(created_dani_family_secrets, axiom, created(dani_shapiro, family_secrets)).
fof(american_city_boston, axiom, american_city(boston)).
% Distinctness
fof(distinct_constants, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).
% Conjecture
fof(conclusion, conjecture, born_in(dani_shapiro, boston)).