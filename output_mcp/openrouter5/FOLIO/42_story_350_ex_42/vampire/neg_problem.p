% Negative version: negated conclusion as conjecture
% Negated conclusion: There exists a design by Max that is neither evocative nor dreamy.

% Predicates:
% design_by_max(D) - D is a design by Max
% adores_max(D) - Max adores D (design)
% adores_style(S) - Max adores style S
% zaha_style(S) - S is Zaha Hadid's design style
% kelly_style(S) - S is Kelly Wearstler's design style
% interesting_geometries(D) - D has interesting geometries
% brutalist(D) - D is a brutalist building
% evocative(D) - D is evocative
% dreamy(D) - D is dreamy
% style_of(D, S) - D is of style S

% Distinctness: Zaha styles and Kelly styles are disjoint
fof(distinct_styles, axiom, ! [S] : (zaha_style(S) => ~ kelly_style(S))).

% Premise 1: All of Zaha Hadid's design styles that Max adores have interesting geometries.
fof(premise_1, axiom, ! [D, S] : ((style_of(D, S) & zaha_style(S) & adores_style(S)) => interesting_geometries(D))).

% Premise 2: No brutalist buildings that Max adores have interesting geometries.
fof(premise_2, axiom, ! [D] : ((brutalist(D) & adores_max(D)) => ~ interesting_geometries(D))).

% Premise 3: Every style that Max adores is either Zaha Hadid's design style or Kelly Wearstler's design style.
fof(premise_3, axiom, ! [S] : (adores_style(S) => (zaha_style(S) | kelly_style(S)))).

% Premise 4: All of Kelly Wearstler's design styles that Max adores are evocative.
fof(premise_4, axiom, ! [D, S] : ((style_of(D, S) & kelly_style(S) & adores_style(S)) => evocative(D))).

% Premise 5: All of Kelly Wearstler's design styles that Max adores are dreamy.
fof(premise_5, axiom, ! [D, S] : ((style_of(D, S) & kelly_style(S) & adores_style(S)) => dreamy(D))).

% Premise 6: If a design by Max that he adores has interesting geometries, then the design is a brutalist building and evocative.
fof(premise_6, axiom, ! [D] : ((design_by_max(D) & adores_max(D) & interesting_geometries(D)) => (brutalist(D) & evocative(D)))).

% Negated conclusion: There exists a design by Max that is neither evocative nor dreamy.
fof(negated_conclusion, conjecture, ? [D] : (design_by_max(D) & ~ evocative(D) & ~ dreamy(D))).