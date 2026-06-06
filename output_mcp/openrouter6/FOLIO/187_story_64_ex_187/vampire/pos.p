fof(distinct_constants, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & family_history != family_secrets & family_history != boston & family_secrets != boston)).

fof(podcast_not_novel, axiom, ! [X] : (podcast(X) => ~novel(X))).

fof(born_in_american_city_implies_american, axiom, ! [P, C] : (person(P) & born_in(P, C) & american_city(C) => american(P))).

fof(novel_book_implies_novel_writer, axiom, ! [B, P] : (book(B) & novel(B) & written_by(B, P) => novel_writer(P))).

fof(dani_shapiro_american_writer, axiom, writer(dani_shapiro) & american(dani_shapiro)).

fof(dani_shapiro_person, axiom, person(dani_shapiro)).

fof(family_history_written_by_dani, axiom, written_by(family_history, dani_shapiro)).

fof(family_history_novel, axiom, novel(family_history) & book(family_history)).

fof(dani_created_family_secrets, axiom, podcast(family_secrets) & created(dani_shapiro, family_secrets)).

fof(boston_american_city, axiom, american_city(boston)).

fof(goal, conjecture, born_in(dani_shapiro, boston)).