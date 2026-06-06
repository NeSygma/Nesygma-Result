fof(business_org_to_legal_entity, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(company_to_business_org, axiom, ! [X] : (company(X) => business_organization(X))).
fof(private_company_to_company, axiom, ! [X] : (private_company(X) => company(X))).
fof(legal_entity_created_under_law, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(legal_entity_has_obligations, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(book_club_conditional, axiom, (created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club))).

fof(goal, conjecture, ~has_legal_obligations(harvard_weekly_book_club)).