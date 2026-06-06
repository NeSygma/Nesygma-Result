fof(all_business_organizations_are_legal_entities, axiom, ! [X] : (business_organization(X) => legal_entity(X))).
fof(all_companies_are_business_organizations, axiom, ! [X] : (company(X) => business_organization(X))).
fof(all_private_companies_are_companies, axiom, ! [X] : (private_company(X) => company(X))).
fof(all_legal_entities_are_created_under_law, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(all_legal_entities_have_legal_obligations, axiom, ! [X] : (legal_entity(X) => has_legal_obligations(X))).
fof(if_created_under_law_then_not_private_company, axiom, (created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club))).
fof(conclusion_neg, conjecture, ~(has_legal_obligations(harvard_weekly_book_club) & private_company(harvard_weekly_book_club))).