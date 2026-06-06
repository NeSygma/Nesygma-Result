fof(premise1, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(premise2, axiom, ! [X] : (company(X) => business_org(X))).
fof(premise3, axiom, ! [X] : (private_company(X) => company(X))).
fof(premise4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(premise5, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(premise6, axiom, (created_under_law(hwbc) => ~private_company(hwbc))).
fof(conclusion, conjecture, (has_legal_obligations(hwbc) & private_company(hwbc))).