% Positive run: conjecture is the conjunction
fof(ax1, axiom, ! [X] : (business_org(X) => legal_entity(X))).
fof(ax2, axiom, ! [X] : (company(X) => business_org(X))).
fof(ax3, axiom, ! [X] : (private_company(X) => company(X))).
fof(ax4, axiom, ! [X] : (legal_entity(X) => created_under_law(X))).
fof(ax5, axiom, ! [X] : (legal_entity(X) => legal_obligation(X))).
fof(ax6, axiom, (created_under_law(harvard_weekly_book_club) => ~private_company(harvard_weekly_book_club))).
fof(goal, conjecture, (legal_obligation(harvard_weekly_book_club) & private_company(harvard_weekly_book_club))).