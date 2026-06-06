% Positive file: original claim as conjecture
% Predicates:
% ml_algorithm(X) - X is a machine learning algorithm
% category(X, Y) - X is categorized as Y (Y is a category)
% requires_labeled_data(X) - algorithm X requires labeled data
% trained_with(M, A) - model M is trained with algorithm A
% state_of_the_art(M) - model M is state-of-the-art

fof(distinct_categories, axiom, (supervised != unsupervised & supervised != reinforcement & unsupervised != reinforcement)).

fof(categorization, axiom, ! [X] : 
    (ml_algorithm(X) => (category(X, supervised) | category(X, unsupervised) | category(X, reinforcement)))).

fof(unsupervised_no_labels, axiom, ! [X] : 
    (category(X, unsupervised) => ~requires_labeled_data(X))).

fof(sota_trained, axiom, ? [M, A] : (state_of_the_art(M) & ml_algorithm(A) & trained_with(M, A))).

fof(not_reinforcement, axiom, ! [M, A] : 
    ((state_of_the_art(M) & trained_with(M, A)) => ~category(A, reinforcement))).

fof(requires_labels, axiom, ! [M, A] : 
    ((state_of_the_art(M) & trained_with(M, A) & ml_algorithm(A)) => requires_labeled_data(A))).

fof(goal, conjecture, ? [M, A] : (state_of_the_art(M) & ml_algorithm(A) & trained_with(M, A) & category(A, supervised))).