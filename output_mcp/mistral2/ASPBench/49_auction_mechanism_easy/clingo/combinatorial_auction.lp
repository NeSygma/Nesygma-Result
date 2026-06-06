% --- Domain Declarations ---
bidder(a; b; c; d).
item(item1; item2; item3; item4; item5).

% --- Bid Data ---
% bid(Bidder, BidId, Price)
bid(a, bid1, 100). bid_items(bid1, item1). bid_items(bid1, item2).
bid(a, bid2, 50).  bid_items(bid2, item3).
bid(b, bid3, 120). bid_items(bid3, item2). bid_items(bid3, item3).
bid(b, bid4, 80).  bid_items(bid4, item4). bid_items(bid4, item5).
bid(c, bid5, 150). bid_items(bid5, item1). bid_items(bid5, item3). bid_items(bid5, item5).
bid(d, bid6, 40).  bid_items(bid6, item4).

% --- Choice Rule for Winning Bids ---
{winning_bid(BidId) : bid(_, BidId, _)}.

% --- Allocation of Items ---
% An item can be allocated to a bidder only if the bidder has a winning bid that includes the item.
allocated(Item, Bidder) :-
    winning_bid(BidId),
    bid(Bidder, BidId, _),
    bid_items(BidId, Item).

% --- No Conflicts: Each item can be allocated to at most one bidder ---
:- allocated(Item, Bidder1), allocated(Item, Bidder2), Bidder1 != Bidder2.

% --- Bundle Integrity: All items in a winning bid must be allocated ---
:- winning_bid(BidId), bid(Bidder, BidId, _), bid_items(BidId, Item), not allocated(Item, Bidder).

% --- Objective: Maximize Total Revenue ---
#maximize { Price : winning_bid(BidId), bid(_, BidId, Price) }.

% --- Show Winning Bids and Allocations ---
#show winning_bid/1.
#show allocated/2.