fof(premise_1, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(premise_2, axiom, ! [X] : (company(X) => business_organization(X))).
fof(premise_3, axiom, ! [X] : (private_company(X) => company(X))).
fof(premise_4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(premise_5, axiom, ! [X] : (legal_entity(X) => legal_obligations(X))).
fof(premise_6, axiom, created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club)).
fof(goal, conjecture, legal_obligations(harvard_weekly_book_club) & private_company(harvard_weekly_book_club)).