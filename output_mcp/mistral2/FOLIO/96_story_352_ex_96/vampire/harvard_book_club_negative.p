fof(business_org_are_legal_entities, axiom,
    ! [X] : (is_a(X, business_organization) => is_a(X, legal_entity))).

fof(companies_are_business_orgs, axiom,
    ! [X] : (is_a(X, company) => is_a(X, business_organization))).

fof(private_companies_are_companies, axiom,
    ! [X] : (is_a(X, private_company) => is_a(X, company))).

fof(legal_entities_created_under_law, axiom,
    ! [X] : (is_a(X, legal_entity) => created_under_law(X))).

fof(legal_entities_have_obligations, axiom,
    ! [X] : (is_a(X, legal_entity) => has_legal_obligations(X))).

fof(harvard_club_law_condition, axiom,
    created_under_law(harvard_weekly_book_club) =>
    ~is_a(harvard_weekly_book_club, private_company)).

fof(distinct_constants, axiom,
    harvard_weekly_book_club != business_organization &
    harvard_weekly_book_club != legal_entity &
    harvard_weekly_book_club != company &
    harvard_weekly_book_club != private_company &
    business_organization != legal_entity &
    business_organization != company &
    business_organization != private_company &
    legal_entity != company &
    legal_entity != private_company &
    company != private_company).

fof(goal_negation, conjecture,
    ~has_legal_obligations(harvard_weekly_book_club)).