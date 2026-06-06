tff(managed_building_type, type, managed_building: $tType).
tff(olive_garden_decl, type, olive_garden: managed_building).
tff(monthly_rent_decl, type, monthly_rent: (managed_building * $int) > $o).
tff(security_deposit_decl, type, security_deposit: (managed_building * $int) > $o).
tff(fact_1, axiom, monthly_rent(olive_garden, 2000)).
tff(fact_2, axiom, ! [X: managed_building, D: $int] : (security_deposit(X, D) => ? [R: $int] : (monthly_rent(X, R) & (D = R | $greater(D, R))))).
tff(goal, conjecture, ~ ! [D: $int] : (security_deposit(olive_garden, D) => (D = 2000 | $greater(D, 2000)))).