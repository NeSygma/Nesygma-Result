% Bidders: bidder(Name, Budget, SynergyBonus).
bidder(a,150,20).
bidder(b,200,10).
bidder(c,180,25).
bidder(d,100,5).

% Items and categories.
item(item1, electronics).
item(item2, electronics).
item(item5, electronics).
item(item3, furniture).
item(item4, furniture).
item(item6, furniture).
item(lic_E, license_e).
item(lic_F, license_f).

% Bids: bid(Id, Bidder, Price). Bid items.
bid(1,a,70). bid_item(1,item1). bid_item(1,item2).
bid(2,a,40). bid_item(2,lic_E).
bid(3,b,90). bid_item(3,item3). bid_item(3,item4).
bid(4,b,50). bid_item(4,lic_F).
bid(5,b,60). bid_item(5,item5).
bid(6,c,100). bid_item(6,item1). bid_item(6,item5).
bid(7,c,60). bid_item(7,lic_E).
bid(8,c,80). bid_item(8,item3). bid_item(8,item6).
bid(9,d,25). bid_item(9,lic_F).
bid(10,d,70). bid_item(10,item4).

% Choice of winning bids.
{win(B)} :- bid(B,_,_).

% 1. Item exclusivity.
:- win(B1), win(B2), B1 != B2, bid_item(B1,I), bid_item(B2,I).

% 2. Budget compliance.
price_sum(Bidder, Sum) :- bidder(Bidder,_,_), Sum = #sum {Price,B : win(B), bid(B,Bidder,Price)}.
:- price_sum(Bidder, Sum), bidder(Bidder,Budget,_), Sum > Budget.

% 3. Synergy bonus condition.
win_count(Bidder, Cnt) :- bidder(Bidder,_,_), Cnt = #count {B : win(B), bid(B,Bidder,_)}.
synergy_applied(Bidder) :- win_count(Bidder, Cnt), Cnt >= 2.

% 4. Licensing requirement.
% Electronics items require lic_E, furniture items require lic_F.
:- win(B), bid(B,Bidder,_), bid_item(B,I), item(I, electronics), not win(L) : bid(L,Bidder,_), bid_item(L,lic_E).
:- win(B), bid(B,Bidder,_), bid_item(B,I), item(I, furniture), not win(L) : bid(L,Bidder,_), bid_item(L,lic_F).

% 5. Fairness: max 3 items per bidder.
item_count(Bidder, Cnt) :- bidder(Bidder,_,_), Cnt = #count {I : win(B), bid(B,Bidder,_), bid_item(B,I)}.
:- item_count(Bidder, Cnt), Cnt > 3.

% Total revenue calculation.
rev_price(R) :- R = #sum {Price,B : win(B), bid(B,_,Price)}.
rev_synergy(S) :- S = #sum {Bonus,Bidder : synergy_applied(Bidder), bidder(Bidder,_,Bonus)}.
total_rev(T) :- rev_price(R), rev_synergy(S), T = R + S.

% Optimization: maximize total revenue.
#maximize {Price,B : win(B), bid(B,_,Price)}.
#maximize {Bonus,Bidder : synergy_applied(Bidder), bidder(Bidder,_,Bonus)}.

#show win/1.
#show total_rev/1.
#show synergy_applied/1.