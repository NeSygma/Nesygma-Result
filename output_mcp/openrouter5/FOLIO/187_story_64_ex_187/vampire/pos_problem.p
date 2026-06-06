% Positive version: original conclusion as conjecture
% Dani Shapiro was born in Boston.

fof(distinct_entities, axiom, (
    family_history != family_secrets & 
    family_history != boston & 
    family_secrets != boston & 
    dani_shapiro != family_history & 
    dani_shapiro != family_secrets & 
    dani_shapiro != boston
)).

% A podcast is not a novel.
fof(rule_1, axiom, ! [X] : (podcast(X) => ~novel(X))).

% If a person is born in American City, the person is American.
fof(rule_2, axiom, ! [P, C] : ((american_city(C) & born_in(P, C)) => american(P))).

% If a book is a novel and it is written by a person, then the person is a novel writer.
fof(rule_3, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).

% Dani Shapiro is an American writer.
fof(fact_1, axiom, american(dani_shapiro)).
fof(fact_2, axiom, writer(dani_shapiro)).

% Family History is written by Dani Shapiro.
fof(fact_3, axiom, written_by(family_history, dani_shapiro)).

% Family History is a novel written in 2003.
fof(fact_4, axiom, novel(family_history)).
fof(fact_5, axiom, written_in(family_history, year_2003)).

% Dani Shapiro created a podcast called Family Secrets.
fof(fact_6, axiom, created(dani_shapiro, family_secrets)).
fof(fact_7, axiom, podcast(family_secrets)).

% Boston is an American city.
fof(fact_8, axiom, american_city(boston)).

% Conclusion: Dani Shapiro was born in Boston.
fof(goal, conjecture, born_in(dani_shapiro, boston)).