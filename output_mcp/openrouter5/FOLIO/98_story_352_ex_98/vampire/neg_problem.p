% Negative version: negated conclusion as conjecture
fof(premise_1, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(premise_2, axiom, ! [X] : (company(X) => business_organization(X))).
fof(premise_3, axiom, ! [X] : (private_company(X) => company(X))).
fof(premise_4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(premise_5, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(premise_6, axiom, (created_under_law(hwbc) => ~private_company(hwbc))).

% Negated conclusion: ~(private_company(hwbc) => (has_legal_obligations(hwbc) | created_under_law(hwbc)))
% Which is equivalent to: private_company(hwbc) & ~has_legal_obligations(hwbc) & ~created_under_law(hwbc)
fof(negated_conclusion, conjecture,
    (private_company(hwbc) & ~has_legal_obligations(hwbc) & ~created_under_law(hwbc))).