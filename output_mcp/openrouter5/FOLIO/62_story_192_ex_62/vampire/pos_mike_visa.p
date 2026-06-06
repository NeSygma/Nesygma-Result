% Positive file: original claim as conjecture
% Premises:
% 1. International students in the US have either an F1 visa or a J1 visa.
fof(premise_1, axiom, ! [X] : (international_student_us(X) => (f1_visa(X) | j1_visa(X)))).

% 2. An international student in the US with an F1 visa needs to apply for CPT or OPT if the student wants to work in the US.
fof(premise_2, axiom, ! [X] : ((international_student_us(X) & f1_visa(X) & wants_to_work_us(X)) => (apply_cpt(X) | apply_opt(X)))).

% 3. Mike is an international student.
fof(premise_3, axiom, international_student_us(mike)).

% 4. Mike needs to apply for CPT if he wants to work in the US.
fof(premise_4, axiom, (wants_to_work_us(mike) => apply_cpt(mike))).

% Conclusion: Mike has a J1 visa.
fof(conclusion, conjecture, j1_visa(mike)).