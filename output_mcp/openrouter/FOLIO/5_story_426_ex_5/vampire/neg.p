% Negative version
fof(ax1, axiom, ![X] : (employee(X) & schedule_meeting(X) => go_building(X))).
fof(ax2, axiom, ![X] : (lunch_building(X) => schedule_meeting(X))).
fof(ax3, axiom, ![X] : (employee(X) => (lunch_building(X) | lunch_home(X)))).
fof(ax4, axiom, ![X] : (employee(X) & lunch_home(X) => working_remote(X))).
fof(ax5, axiom, ![X] : (employee(X) & in_other_country(X) => working_remote(X))).
fof(ax6, axiom, ![X] : (manager(X) => ~working_remote(X))).
fof(ax7a, axiom, go_building(james) => manager(james)).
fof(ax7b, axiom, manager(james) => go_building(james)).
fof(ax8, axiom, employee(james)).
fof(conj, conjecture, lunch_building(james)).