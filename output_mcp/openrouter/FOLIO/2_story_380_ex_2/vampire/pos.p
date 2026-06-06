% Positive version
fof(ax1, axiom, ![X]: (perform_often(X) => attend_events(X))).
fof(ax2, axiom, ![X]: (perform_often(X) | inactive_disinterested(X))).
fof(ax3, axiom, ![X]: (chaperone_dances(X) => ~student_attends_school(X))).
fof(ax4, axiom, ![X]: (inactive_disinterested(X) => chaperone_dances(X))).
fof(ax5, axiom, ![X]: ((young_child_or_teenager(X) & wish_academic(X)) => student_attends_school(X))).
fof(ax6, axiom, (attend_events(bonnie) <=> student_attends_school(bonnie))).
fof(goal, conjecture, ( ( (young_child_or_teenager(bonnie) & wish_academic(bonnie) & chaperone_dances(bonnie)) | ~ (young_child_or_teenager(bonnie) & wish_academic(bonnie)) ) => (student_attends_school(bonnie) | inactive_disinterested(bonnie)) ) ).