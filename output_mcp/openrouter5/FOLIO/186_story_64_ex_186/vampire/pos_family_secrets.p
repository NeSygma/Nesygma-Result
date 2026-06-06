% Positive file: original claim as conjecture
% "Family Secrets is a novel."

fof(distinct_entities, axiom, (
    family_secrets != family_history
)).

fof(premise_1, axiom, ! [X] : (podcast(X) => ~novel(X))).
fof(premise_2, axiom, ! [P, C] : ((born_in(P, C) & american_city(C)) => american(P))).
fof(premise_3, axiom, ! [B, P] : ((novel(B) & written_by(B, P)) => novel_writer(P))).
fof(premise_4, axiom, american_writer(dani_shapiro)).
fof(premise_5, axiom, written_by(family_history, dani_shapiro)).
fof(premise_6, axiom, novel(family_history)).
fof(premise_7, axiom, created(dani_shapiro, family_secrets)).
fof(premise_8, axiom, podcast(family_secrets)).
fof(premise_9, axiom, american_city(boston)).

fof(goal, conjecture, novel(family_secrets)).