%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Atomic Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
last_instant(T) :- time(T), not time(T+1).
holds(T, X) :- atomic(X, A), time(T), trace(T, A).
holds(T, X) :- last(X), last_instant(T).
holds(T, X) :- true(X), time(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%% Propositional Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(T, X) :- conjunction(X,_), time(T), holds(T,F): conjunction(X,F).
holds(T, X) :- disjunction(X, F), holds(T, F).
holds(T, X) :- negate(X, F), not holds(T, F), time(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Temporal Formula %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
holds(T, X) :- next(X, F), holds(T+1, F), time(T), time(T+1).
holds(T, X) :- until(X, LHS, RHS), holds(T, RHS).
holds(T, X) :- until(X, LHS, RHS), holds(T, LHS), holds(T+1, X).
holds(T, X) :- release(X, LHS, RHS), holds(T,RHS), holds(T,LHS).
holds(T, X) :- release(X, LHS, RHS), holds(T,RHS), holds(T+1, X).
holds(T, X) :- release(X, LHS, RHS), holds(T,RHS), last_instant(T).

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%% Output projection %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#show.
#show trace/2.


#defined true/1.
#defined false/1.
#defined last/1.
#defined negate/2.
#defined conjunction/2.
#defined atomic/2.
#defined disjunction/2.
#defined trace/2.
#defined next/2.
#defined until/3.
#defined release/3.
