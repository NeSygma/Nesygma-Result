fof(ax1, axiom, ! [X] : ((in_club(X) & ~inactive_disinterested(X)) => chaperones_high_school_dance(X))).
fof(ax2, axiom, ! [X] : (in_club(X) => (performs_in_talent_show_often(X) | inactive_disinterested(X)))).
fof(ax3, axiom, ! [X] : ((in_club(X) & chaperones_high_school_dance(X)) => ~student_attends_school(X))).
fof(ax4, axiom, ! [X] : ((in_club(X) & inactive_disinterested(X)) => chaperones_high_school_dance(X))).
fof(ax5, axiom, ! [X] : ((young_teen(X) & wishes_academic(X) & in_club(X)) => student_attends_school(X))).
fof(ax6, axiom, in_club(bonnie) & ((attends(bonnie) & engaged(bonnie) & student_attends_school(bonnie)) | ~(attends(bonnie) & engaged(bonnie) & ~student_attends_school(bonnie)))).
fof(goal, conjecture, (chaperones_high_school_dance(bonnie) | performs_in_talent_show_often(bonnie)) => (young_teen(bonnie) & wishes_academic(bonnie) & inactive_disinterested(bonnie))).