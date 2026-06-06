fof(business_org_are_legal, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(companies_are_business_orgs, axiom, ! [X] : (company(X) => business_organization(X))).
fof(private_companies_are_companies, axiom, ! [X] : (private_company(X) => company(X))).
fof(legal_entities_created_under_law, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(legal_entities_have_obligations, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(created_under_law_implies_not_private, axiom, created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club)).
fof(conclusion, conjecture, private_company(harvard_weekly_book_club) => (has_legal_obligations(harvard_weekly_book_club) | created_under_law(harvard_weekly_book_club))).