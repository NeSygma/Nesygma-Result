% Predicates
fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).

fof(born_in_american_city, axiom, ! [P, C] : (person(P) & born_in(P, C) & american_city(C) => american(P))).

fof(novel_writer_rule, axiom, ! [B, P] : (book(B) & novel(B) & written_by(B, P) => novel_writer(P))).

% Facts
fof(dani_shapiro_person, axiom, person(dani_shapiro)).
fof(dani_shapiro_writer, axiom, writer(dani_shapiro)).
fof(dani_shapiro_american, axiom, american(dani_shapiro)).

fof(family_history_written_by, axiom, written_by(family_history, dani_shapiro)).

fof(family_history_book, axiom, book(family_history)).
fof(family_history_novel, axiom, novel(family_history)).

fof(family_secrets_podcast, axiom, podcast(family_secrets)).
fof(dani_shapiro_created, axiom, created(dani_shapiro, family_secrets)).

fof(boston_american_city, axiom, american_city(boston)).

% Distinct constants
fof(distinct_constants, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).

% Conclusion
fof(goal, conjecture, novel_writer(dani_shapiro)).