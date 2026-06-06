fof(p1, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(p2, axiom, ! [X] : (company(X) => business_org(X))).
fof(p3, axiom, ! [X] : (private_company(X) => company(X))).
fof(p4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(p5, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(p6, axiom, (created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club))).
fof(goal, conjecture, has_legal_obligations(harvard_weekly_book_club)).