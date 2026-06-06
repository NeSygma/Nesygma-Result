% Genes
gene(g1; g2; g3; g4; g5).

% Choice rule: Each gene can be active or inactive
{ is_active(G) } :- gene(G).

% Regulatory rules defining the required state (rule_result)
rule_result(g1) :- not is_active(g2).
rule_result(g2) :- not is_active(g1).
rule_result(g3) :- is_active(g4), is_active(g5).
rule_result(g4).
rule_result(g5).

% Constraint: The actual state must match the rule result
:- is_active(G), not rule_result(G).
:- not is_active(G), rule_result(G).

% Output formatting
#show is_active/1.