fof(p1, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(p2, axiom, ! [X] : (company(X) => business_org(X))).
fof(p3, axiom, ! [X] : (private_company(X) => company(X))).
fof(p4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(p5, axiom, ! [X] : (legal_entity(X) => legal_obligations(X))).
fof(p6, axiom, created_under_law(hwbc) => ~private_company(hwbc)).
fof(goal, conjecture, ~(legal_obligations(hwbc) & private_company(hwbc))).