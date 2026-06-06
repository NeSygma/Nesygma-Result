% Negative file: negated claim as conjecture
% Premises about design styles and designs by Max

% Predicates:
% zaha(X)       - X is a Zaha Hadid design style
% kelly(X)      - X is a Kelly Wearstler design style
% brutalist(X)  - X is a brutalist building
% adores(X)     - Max adores X
% interesting_geometries(X) - X has interesting geometries
% evocative(X)  - X is evocative
% dreamy(X)     - X is dreamy
% design_by_max(X) - X is a design by Max

% Premise 1: All of Zaha Hadid's design styles that Max adores have interesting geometries.
fof(premise_1, axiom, ! [X] : ((zaha(X) & adores(X)) => interesting_geometries(X))).

% Premise 2: No brutalist buildings that Max adores have interesting geometries.
fof(premise_2, axiom, ! [X] : ((brutalist(X) & adores(X)) => ~interesting_geometries(X))).

% Premise 3: Every style that Max adores is either Zaha Hadid's design style or Kelly Wearstler's design style.
fof(premise_3, axiom, ! [X] : (adores(X) => (zaha(X) | kelly(X)))).

% Premise 4: All of Kelly Wearstler's design styles that Max adores are evocative.
fof(premise_4, axiom, ! [X] : ((kelly(X) & adores(X)) => evocative(X))).

% Premise 5: All of Kelly Wearstler's design styles that Max adores are dreamy.
fof(premise_5, axiom, ! [X] : ((kelly(X) & adores(X)) => dreamy(X))).

% Premise 6: If a design by Max that he adores has interesting geometries, then the design is a brutalist building and evocative.
fof(premise_6, axiom, ! [X] : ((design_by_max(X) & adores(X) & interesting_geometries(X)) => (brutalist(X) & evocative(X)))).

% Negated conclusion: There is NO design by Max that is both evocative and dreamy.
fof(negated_conclusion, conjecture, ~ ? [X] : (design_by_max(X) & evocative(X) & dreamy(X))).