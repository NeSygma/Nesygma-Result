% Negative file: negated conclusion as conjecture
% Negated conclusion: It is NOT the case that (HWBC has legal obligations AND is a private company)
% i.e., ~(has_legal_obligations(hwbc) & private_company(hwbc))

fof(premise_1, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(premise_2, axiom, ! [X] : (company(X) => business_organization(X))).
fof(premise_3, axiom, ! [X] : (private_company(X) => company(X))).
fof(premise_4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(premise_5, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(premise_6, axiom, (created_under_law(hwbc) => ~private_company(hwbc))).

fof(distinct, axiom, true).

fof(goal, conjecture, ~(has_legal_obligations(hwbc) & private_company(hwbc))).