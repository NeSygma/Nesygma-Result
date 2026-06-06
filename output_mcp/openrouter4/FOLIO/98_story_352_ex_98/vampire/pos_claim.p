% Positive: conclusion as conjecture
fof(p1, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(p2, axiom, ! [X] : (company(X) => business_org(X))).
fof(p3, axiom, ! [X] : (private_company(X) => company(X))).
fof(p4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(p5, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(p6, axiom, (created_under_law(hwbc) => ~private_company(hwbc))).
fof(conclusion, conjecture, (private_company(hwbc) => (has_legal_obligations(hwbc) | created_under_law(hwbc)))).