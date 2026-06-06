% Problem: Pierson College is a residential college at Yale
% Negative version: Negated claim as conjecture

% Constants
fof(constant_declaration, axiom, $true).

% Distinctness axioms for all residential colleges
fof(distinct_colleges, axiom,
    (benjamin_franklin_college != berkeley_college &
     benjamin_franklin_college != branford_college &
     benjamin_franklin_college != davenport_college &
     benjamin_franklin_college != ezra_stiles_college &
     benjamin_franklin_college != grace_hopper_college &
     benjamin_franklin_college != jonathan_edwards_college &
     benjamin_franklin_college != morse_college &
     benjamin_franklin_college != pauli_murray_college &
     benjamin_franklin_college != pierson_college &
     benjamin_franklin_college != saybrook_college &
     benjamin_franklin_college != silliman_college &
     benjamin_franklin_college != timothy_dwight_college &
     benjamin_franklin_college != trumbull_college &
     berkeley_college != branford_college &
     berkeley_college != davenport_college &
     berkeley_college != ezra_stiles_college &
     berkeley_college != grace_hopper_college &
     berkeley_college != jonathan_edwards_college &
     berkeley_college != morse_college &
     berkeley_college != pauli_murray_college &
     berkeley_college != pierson_college &
     berkeley_college != saybrook_college &
     berkeley_college != silliman_college &
     berkeley_college != timothy_dwight_college &
     berkeley_college != trumbull_college &
     branford_college != davenport_college &
     branford_college != ezra_stiles_college &
     branford_college != grace_hopper_college &
     branford_college != jonathan_edwards_college &
     branford_college != morse_college &
     branford_college != pauli_murray_college &
     branford_college != pierson_college &
     branford_college != saybrook_college &
     branford_college != silliman_college &
     branford_college != timothy_dwight_college &
     branford_college != trumbull_college &
     davenport_college != ezra_stiles_college &
     davenport_college != grace_hopper_college &
     davenport_college != jonathan_edwards_college &
     davenport_college != morse_college &
     davenport_college != pauli_murray_college &
     davenport_college != pierson_college &
     davenport_college != saybrook_college &
     davenport_college != silliman_college &
     davenport_college != timothy_dwight_college &
     davenport_college != trumbull_college &
     ezra_stiles_college != grace_hopper_college &
     ezra_stiles_college != jonathan_edwards_college &
     ezra_stiles_college != morse_college &
     ezra_stiles_college != pauli_murray_college &
     ezra_stiles_college != pierson_college &
     ezra_stiles_college != saybrook_college &
     ezra_stiles_college != silliman_college &
     ezra_stiles_college != timothy_dwight_college &
     ezra_stiles_college != trumbull_college &
     grace_hopper_college != jonathan_edwards_college &
     grace_hopper_college != morse_college &
     grace_hopper_college != pauli_murray_college &
     grace_hopper_college != pierson_college &
     grace_hopper_college != saybrook_college &
     grace_hopper_college != silliman_college &
     grace_hopper_college != timothy_dwight_college &
     grace_hopper_college != trumbull_college &
     jonathan_edwards_college != morse_college &
     jonathan_edwards_college != pauli_murray_college &
     jonathan_edwards_college != pierson_college &
     jonathan_edwards_college != saybrook_college &
     jonathan_edwards_college != silliman_college &
     jonathan_edwards_college != timothy_dwight_college &
     jonathan_edwards_college != trumbull_college &
     morse_college != pauli_murray_college &
     morse_college != pierson_college &
     morse_college != saybrook_college &
     morse_college != silliman_college &
     morse_college != timothy_dwight_college &
     morse_college != trumbull_college &
     pauli_murray_college != pierson_college &
     pauli_murray_college != saybrook_college &
     pauli_murray_college != silliman_college &
     pauli_murray_college != timothy_dwight_college &
     pauli_murray_college != trumbull_college &
     pierson_college != saybrook_college &
     pierson_college != silliman_college &
     pierson_college != timothy_dwight_college &
     pierson_college != trumbull_college &
     saybrook_college != silliman_college &
     saybrook_college != timothy_dwight_college &
     saybrook_college != trumbull_college &
     silliman_college != timothy_dwight_college &
     silliman_college != trumbull_college &
     timothy_dwight_college != trumbull_college)).

% Premise: All listed colleges are residential colleges at Yale
fof(residential_colleges_premise, axiom,
    (residential_college_at(benjamin_franklin_college, yale_university) &
     residential_college_at(berkeley_college, yale_university) &
     residential_college_at(branford_college, yale_university) &
     residential_college_at(davenport_college, yale_university) &
     residential_college_at(ezra_stiles_college, yale_university) &
     residential_college_at(grace_hopper_college, yale_university) &
     residential_college_at(jonathan_edwards_college, yale_university) &
     residential_college_at(morse_college, yale_university) &
     residential_college_at(pauli_murray_college, yale_university) &
     residential_college_at(pierson_college, yale_university) &
     residential_college_at(saybrook_college, yale_university) &
     residential_college_at(silliman_college, yale_university) &
     residential_college_at(timothy_dwight_college, yale_university) &
     residential_college_at(trumbull_college, yale_university))).

% Negated target claim: Pierson College is NOT a residential college at Yale
fof(goal, conjecture, ~residential_college_at(pierson_college, yale_university)).