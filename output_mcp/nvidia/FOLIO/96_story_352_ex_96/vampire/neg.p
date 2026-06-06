fof(all_business_entities_are_legal_entities, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(all_companies_are_business_orgs, axiom, ! [X] : (company(X) => business_org(X))).
fof(all_private_companies_are_companies, axiom, ! [X] : (private_company(X) => company(X))).
fof(all_legal_entities_are_created_under_law, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(all_legal_entities_have_legal_obligations, axiom, ! [X] : (legal_entity(X) => has_legal_obligation(X))).
fof(hwbc_created_under_law_implies_not_private, axiom, (created_under_law(hwbc) => ~private_company(hwbc))).
fof(neg_goal, conjecture, ~has_legal_obligation(hwbc)).