fof(club_member, axiom, ClubMember(bonnie)).
fof(premise_1, axiom, ! [X] : (ClubMember(X) & PerformOften(X) => AttendEngaged(X))).
fof(premise_2, axiom, ! [X] : (ClubMember(X) => (PerformOften(X) | InactiveDisinterested(X)))).
fof(premise_3, axiom, ! [X] : (ClubMember(X) & ChaperoneDances(X) => ~StudentAttendSchool(X))).
fof(premise_4, axiom, ! [X] : (ClubMember(X) & InactiveDisinterested(X) => ChaperoneDances(X))).
fof(premise_5, axiom, ! [X] : (ClubMember(X) & YoungChildTeenagerWishAcademic(X) => StudentAttendSchool(X))).
fof(premise_6, axiom, ClubMember(bonnie) & (AttendEngaged(bonnie) <=> StudentAttendSchool(bonnie))).
fof(conclusion, conjecture, (ChaperoneDances(bonnie) | PerformOften(bonnie)) => (YoungChildTeenagerWishAcademic(bonnie) & InactiveDisinterested(bonnie))).