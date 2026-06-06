fof(axiom_business_org_imp_legal, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(axiom_company_imp_business, axiom, ! [X] : (company(X) => business_org(X))).
fof(axiom_private_to_company, axiom, ! [X] : (private_company(X) => company(X))).
fof(axiom_legal_to_created, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(axiom_legal_to_obligation, axiom, ! [X] : (legal_entity(X) => has_legal_obligation(X))).
fof(axiom_6, axiom, ~created_under_law(harvard_weekly_book_club) | ~private_company(harvard_weekly_book_club)).
fof(conclusion_neg, conjecture, ~has_legal_obligation(harvard_weekly_book_club) | ~private_company(harvard_weekly_book_club)).