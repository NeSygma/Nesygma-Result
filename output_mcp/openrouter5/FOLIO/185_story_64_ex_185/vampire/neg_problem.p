% Negative version: negated claim as conjecture
% Dani Shapiro is NOT a novel writer.

fof(distinct_entities, axiom,
    (podcast != novel & boston != dani_shapiro & boston != family_history & boston != family_secrets & dani_shapiro != family_history & dani_shapiro != family_secrets & family_history != family_secrets)).

% A podcast is not a novel.
fof(rule_1, axiom, ! [X] : (podcast(X) => ~novel(X))).

% If a person is born in American City, the person is American.
fof(rule_2, axiom, ! [P, C] : ((american_city(C) & born_in(P, C)) => american(P))).

% If a book is a novel and it is written by a person, then the person is a novel writer.
fof(rule_3, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).

% Dani Shapiro is an American writer.
fof(fact_1, axiom, american_writer(dani_shapiro)).

% Family History is written by Dani Shapiro.
fof(fact_2, axiom, written_by(family_history, dani_shapiro)).

% Family History is a novel written in 2003.
fof(fact_3, axiom, novel(family_history)).

% Dani Shapiro created a podcast called Family Secrets.
fof(fact_4, axiom, created(dani_shapiro, family_secrets) & podcast(family_secrets)).

% Boston is an American city.
fof(fact_5, axiom, american_city(boston)).

% Negated conclusion: Dani Shapiro is NOT a novel writer.
fof(goal, conjecture, ~novel_writer(dani_shapiro)).