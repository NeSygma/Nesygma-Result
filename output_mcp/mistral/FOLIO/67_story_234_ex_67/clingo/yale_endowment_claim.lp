% --- Premises (facts) ---
university(yale).
is_private_ivy_league(yale).
moved_to_new_haven_in(yale, 1716).
endowment_value(yale, 42300000000).

residential_college(benjamin_franklin).
residential_college(berkeley).
residential_college(branford).
residential_college(davenport).
residential_college(ezra_stiles).
residential_college(grace_hopper).
residential_college(jonathan_edwards).
residential_college(morse).
residential_college(pauli_murray).
residential_college(pierson).
residential_college(saybrook).
residential_college(silliman).
residential_college(timothy_dwight).
residential_college(trumbull).

% --- Represent the claim and its negation ---
% We have no evidence to support or contradict the claim that Yale has the largest endowment
% Therefore, based strictly on these premises, the conclusion is uncertain

has_evidence_for_true :- false.  % No evidence supports the claim
has_evidence_for_false :- false. % No evidence contradicts the claim

% Derive conclusion predicates from evidence
conclusion_true :- has_evidence_for_true.
conclusion_false :- has_evidence_for_false.

% Answer mapping following theorem proving pattern
answer(true) :- conclusion_true.
answer(false) :- conclusion_false.
answer(uncertain) :- not conclusion_true, not conclusion_false.
answer(inconsistent) :- conclusion_true, conclusion_false.

#show answer/1.