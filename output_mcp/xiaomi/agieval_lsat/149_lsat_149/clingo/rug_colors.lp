% Define the 6 colors
color(forest). color(olive). color(peach). color(turquoise). color(white). color(yellow).

% Define the 3 rugs
rug(1). rug(2). rug(3).

% Define the answer choices as potential assignments
% Each choice assigns colors to rugs

% Choice A: forest only; turquoise only; olive, peach, and white
assign_a(1, forest).
assign_a(2, turquoise).
assign_a(3, olive). assign_a(3, peach). assign_a(3, white).

% Choice B: forest only; turquoise only; olive, peach, and yellow
assign_b(1, forest).
assign_b(2, turquoise).
assign_b(3, olive). assign_b(3, peach). assign_b(3, yellow).

% Choice C: peach only; turquoise only; forest, olive, and white
assign_c(1, peach).
assign_c(2, turquoise).
assign_c(3, forest). assign_c(3, olive). assign_c(3, white).

% Choice D: yellow only; forest and turquoise; olive and peach
assign_d(1, yellow).
assign_d(2, forest). assign_d(2, turquoise).
assign_d(3, olive). assign_d(3, peach).

% Choice E: yellow only; olive and peach; turquoise and white
assign_e(1, yellow).
assign_e(2, olive). assign_e(2, peach).
assign_e(3, turquoise). assign_e(3, white).

% Check constraints for each choice
% Constraint 1: Exactly 5 colors used (one color not used)
used_a(C) :- assign_a(_, C).
used_b(C) :- assign_b(_, C).
used_c(C) :- assign_c(_, C).
used_d(C) :- assign_d(_, C).
used_e(C) :- assign_e(_, C).

count_a(N) :- N = #count{C : used_a(C)}.
count_b(N) :- N = #count{C : used_b(C)}.
count_c(N) :- N = #count{C : used_c(C)}.
count_d(N) :- N = #count{C : used_d(C)}.
count_e(N) :- N = #count{C : used_e(C)}.

% Constraint 2: Each used color appears in exactly one rug
unique_a :- assign_a(R1, C), assign_a(R2, C), R1 != R2.
unique_b :- assign_b(R1, C), assign_b(R2, C), R1 != R2.
unique_c :- assign_c(R1, C), assign_c(R2, C), R1 != R2.
unique_d :- assign_d(R1, C), assign_d(R2, C), R1 != R2.
unique_e :- assign_e(R1, C), assign_e(R2, C), R1 != R2.

% Constraint 3: If white is used in a rug, that rug has exactly 3 colors
white_rule_a :- assign_a(R, white), not 3 = #count{C : assign_a(R, C)}.
white_rule_b :- assign_b(R, white), not 3 = #count{C : assign_b(R, C)}.
white_rule_c :- assign_c(R, white), not 3 = #count{C : assign_c(R, C)}.
white_rule_d :- assign_d(R, white), not 3 = #count{C : assign_d(R, C)}.
white_rule_e :- assign_e(R, white), not 3 = #count{C : assign_e(R, C)}.

% Constraint 4: If olive is used in a rug, peach must also be used in that rug
olive_rule_a :- assign_a(R, olive), not assign_a(R, peach).
olive_rule_b :- assign_b(R, olive), not assign_b(R, peach).
olive_rule_c :- assign_c(R, olive), not assign_c(R, peach).
olive_rule_d :- assign_d(R, olive), not assign_d(R, peach).
olive_rule_e :- assign_e(R, olive), not assign_e(R, peach).

% Constraint 5: Forest and turquoise cannot be in the same rug
ft_rule_a :- assign_a(R, forest), assign_a(R, turquoise).
ft_rule_b :- assign_b(R, forest), assign_b(R, turquoise).
ft_rule_c :- assign_c(R, forest), assign_c(R, turquoise).
ft_rule_d :- assign_d(R, forest), assign_d(R, turquoise).
ft_rule_e :- assign_e(R, forest), assign_e(R, turquoise).

% Constraint 6: Peach and turquoise cannot be in the same rug
pt_rule_a :- assign_a(R, peach), assign_a(R, turquoise).
pt_rule_b :- assign_b(R, peach), assign_b(R, turquoise).
pt_rule_c :- assign_c(R, peach), assign_c(R, turquoise).
pt_rule_d :- assign_d(R, peach), assign_d(R, turquoise).
pt_rule_e :- assign_e(R, peach), assign_e(R, turquoise).

% Constraint 7: Peach and yellow cannot be in the same rug
py_rule_a :- assign_a(R, peach), assign_a(R, yellow).
py_rule_b :- assign_b(R, peach), assign_b(R, yellow).
py_rule_c :- assign_c(R, peach), assign_c(R, yellow).
py_rule_d :- assign_d(R, peach), assign_d(R, yellow).
py_rule_e :- assign_e(R, peach), assign_e(R, yellow).

% A choice is valid if it satisfies all constraints
valid_a :- count_a(5), not unique_a, not white_rule_a, not olive_rule_a, 
           not ft_rule_a, not pt_rule_a, not py_rule_a.
valid_b :- count_b(5), not unique_b, not white_rule_b, not olive_rule_b, 
           not ft_rule_b, not pt_rule_b, not py_rule_b.
valid_c :- count_c(5), not unique_c, not white_rule_c, not olive_rule_c, 
           not ft_rule_c, not pt_rule_c, not py_rule_c.
valid_d :- count_d(5), not unique_d, not white_rule_d, not olive_rule_d, 
           not ft_rule_d, not pt_rule_d, not py_rule_d.
valid_e :- count_e(5), not unique_e, not white_rule_e, not olive_rule_e, 
           not ft_rule_e, not pt_rule_e, not py_rule_e.

% Map to options
option(a) :- valid_a.
option(b) :- valid_b.
option(c) :- valid_c.
option(d) :- valid_d.
option(e) :- valid_e.

#show option/1.