% holds(T, X) :- release(X, LHS, RHS), ... .
% holds(T, X) :- release(X, LHS, RHS), ... .
% holds(T, X) :- weak_until(X, LHS, RHS), ... .
% holds(T, X) :- weak_until(X, LHS, RHS), ... .
% holds(T, X) :- strong_release(X, LHS, RHS), ... .
% holds(T, X) :- strong_release(X, LHS, RHS), ... .

%nel parser delle tracce
%time(T) :- trace(T,_).
%time(T) :- -trace(T,_).
%last_instant(T) :- time(T), not time(T+1).

:- root(X), not holds(0, X).
:- root(X), always(X,F), not holds(_,F).
:- root(X), conjunction(X,F), not holds(0,F).

holds(T, X) :- atomic(X, A), trace(T, A).
holds(T, X) :- weak_next(X, A), last_instant(T).
holds(T, X) :- weak_next(X, A), holds(T+1, A), time(T), time(T+1).
holds(T, X) :- next(X, F), holds(T+1, F), time(T), time(T+1).
holds(T, X) :- last(X), last_instant(T).
holds(T, X) :- true(X), time(T).
holds(T, X) :- always(X, F), holds(T, F), last_instant(T).
holds(T, X) :- always(X, F), holds(T+1,X), holds(T, F).
holds(T, X) :- eventually(X, F), holds(T, F).
holds(T, X) :- eventually(X, F), holds(T+1, X), time(T+1).
holds(T,X) :- equivalent(X, LHS, RHS), holds(T, LHS), holds(T, RHS).
holds(T,X) :- equivalent(X, LHS, RHS), time(T), not holds(T, LHS), not holds(T, RHS).
holds(T, X) :- until(X, LHS, RHS), holds(T, RHS).
holds(T, X) :- until(X, LHS, RHS), holds(T, LHS), holds(T+1, X).
holds(T, X) :- negate(X, F), not holds(T, F), time(T).
holds(T, X) :- conjunction(X,_), time(T), holds(T,F): conjunction(X,F).
holds(T, X) :- disjunction(X, F), holds(T, F).
holds(T, X) :- implies(X, LHS, RHS), holds(T, LHS), holds(T, RHS).
holds(T, X) :- implies(X, LHS, RHS), time(T), not holds(T, LHS).


#defined nogood_root/1.
#defined atomic/2.
#defined true/1.
#defined false/1.
#defined last/1.
#defined next/2.
#defined weak_next/2.
#defined eventually/2.
#defined always/2.
#defined negate/2.
#defined conjunction/2.
#defined disjunction/2.
#defined until/3.
#defined weak_until/3.
#defined release/3.
#defined strong_release/3.
#defined implies/3.
#defined equivalent/3.
