% Positive file: original claim as conjecture
% Dani Shapiro was born in Boston.

% Premise 1: A podcast is not a novel.
fof(premise_1, axiom, ! [X] : (podcast(X) => ~novel(X))).

% Premise 2: If a person is born in an American city, the person is American.
fof(premise_2, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).

% Premise 3: If a book is a novel and written by a person, then the person is a novel writer.
fof(premise_3, axiom, ! [B, P] : ((book(B) & novel(B) & written_by(B, P)) => novel_writer(P))).

% Premise 4: Dani Shapiro is an American writer.
fof(premise_4, axiom, american(dani_shapiro) & writer(dani_shapiro)).

% Premise 5: Family History is written by Dani Shapiro.
fof(premise_5, axiom, written_by(family_history, dani_shapiro)).

% Premise 6: Family History is a novel written in 2003.
fof(premise_6, axiom, novel(family_history) & written_in(family_history, year_2003)).
% A novel is a book.
fof(novel_is_book, axiom, ! [X] : (novel(X) => book(X))).

% Premise 7: Dani Shapiro created a podcast called Family Secrets.
fof(premise_7, axiom, created(dani_shapiro, family_secrets) & podcast(family_secrets)).

% Premise 8: Boston is an American city.
fof(premise_8, axiom, american_city(boston)).

% Distinctness axioms for constants
fof(distinct_constants, axiom, (dani_shapiro != family_history & dani_shapiro != family_secrets & dani_shapiro != boston & dani_shapiro != year_2003 & family_history != family_secrets & family_history != boston & family_history != year_2003 & family_secrets != boston & family_secrets != year_2003 & boston != year_2003)).

% Conclusion: Dani Shapiro was born in Boston.
fof(conclusion, conjecture, born_in(dani_shapiro, boston)).