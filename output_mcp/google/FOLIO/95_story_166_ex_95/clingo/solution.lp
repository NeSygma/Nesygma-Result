% --- Premises ---
managed_building(olive_garden).
monthly_rent(olive_garden, 2000).

% Premise: The security deposit can be either equal to the monthly rent at a managed building or more.
% This implies for any managed building B with rent R, the deposit D >= R.
% We represent this as a property of the building.
security_deposit_ge_rent(B, R) :- managed_building(B), monthly_rent(B, R).

% --- Conclusion ---
% The security deposit at the Olive Garden is either $2000 or more.
conclusion_true :- security_deposit_ge_rent(olive_garden, 2000).

% --- Logic for True/False/Uncertain ---
% Since the conclusion is derived directly from the premises, it is true.
% We must define conclusion_false independently to satisfy the theorem proving pattern.
% There is no premise that contradicts the conclusion.
conclusion_false :- false. 

answer(true)      :- conclusion_true.
answer(false)     :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.

#show answer/1.