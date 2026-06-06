fof(categorization, axiom, 
    ! [X] : (ml_algorithm(X) => 
        (supervised(X) | unsupervised(X) | reinforcement_learning(X)))).

fof(disjoint_categories, axiom, 
    ! [X] : ~(supervised(X) & unsupervised(X)) &
    ! [X] : ~(supervised(X) & reinforcement_learning(X)) &
    ! [X] : ~(unsupervised(X) & reinforcement_learning(X))).

fof(unsupervised_no_labels, axiom, 
    ! [X] : (unsupervised(X) => ~requires_labeled_data(X))).

fof(state_of_the_art_model_exists, axiom, 
    state_of_the_art_summarization_model(sum_model)).

fof(trained_with_ml, axiom, 
    trained_with(sum_model, ml_algorithm_for_sum)).

fof(rl_not_used, axiom, 
    ~reinforcement_learning(ml_algorithm_for_sum)).

fof(sum_requires_labels, axiom, 
    requires_labeled_data(ml_algorithm_for_sum)).

fof(not_supervised_used, conjecture, 
    ~supervised(ml_algorithm_for_sum)).