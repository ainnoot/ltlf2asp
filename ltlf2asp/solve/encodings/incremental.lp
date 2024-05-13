#program base.

#program formula.
symbol(X) :- atomic(_,X).
node(X) :- atomic(X,_).
node(X) :- weak_next(X,_).
node(X) :- next(X,_).
node(X) :- true(X).
node(X) :- false(X).
node(X) :- last(X).
node(X) :- always(X,_).
node(X) :- eventually(X,_).
node(X) :- equivalent(X,_,_).
node(X) :- until(X,_,_).
node(X) :- negate(X,_).
node(X) :- conjunction(X,_).
node(X) :- disjunction(X,_).
node(X) :- implies(X,_,_).

#program search(a, b).
#external search(a, b).
{ last_state(T): T=a..b-1 } = 1 :- search(a, b).
time(a..b-1) :- not search(a, b).
time(a..T) :- last_state(T), search(a, b).
{ trace(T,A): symbol(A) } :- T=a..b-1.
:- last_state(L), trace(K,_), K > L.
:- root(X), not holds(0,X), search(a,b).

#program semantics(t).
#external holds(t+1,X): node(X).
#external time(t).
#external time(t+1).
holds(t,X) :- atomic(X,A), trace(t,A).
holds(t,X) :- last(X), last_state(t), time(t).
holds(t,X) :- weak_next(X,F), holds(t+1, F).
holds(t,X) :- weak_next(X,F), last_state(t).
holds(t,X) :- next(X,F), holds(t+1,F).
holds(t,X) :- true(X).
holds(t,X) :- always(X,F), holds(t,F), last_state(t).
holds(t,X) :- always(X,F), holds(t,F), holds(t+1,X).
holds(t,X) :- eventually(X,F), holds(t,F).
holds(t,X) :- eventually(X,F), holds(t+1,X).
holds(t,X) :- equivalent(X, LHS, RHS), holds(t, LHS), holds(t, RHS).
holds(t,X) :- equivalent(X, LHS, RHS), time(t), not holds(t, LHS), not holds(t, RHS).
holds(t,X) :- until(X,LHS,RHS), holds(t,RHS).
holds(t,X) :- until(X,LHS,RHS), holds(t,LHS), holds(t+1,X).
% holds(t,X) :- weak_until(X,LHS,RHS), holds(t,RHS).
% holds(t,X) :- weak_until(X,LHS,RHS), holds(t,LHS), last_state(t).
% holds(t,X) :- weak_until(X,LHS,RHS), holds(t,LHS), holds(t+1,X).

holds(t,X) :- negate(X,F), not holds(t,F), time(t).
holds(t,X) :- conjunction(X,_), time(t), holds(t,F): conjunction(X,F).
holds(t,X) :- disjunction(X,F), holds(t,F).
holds(t,X) :- implies(X,LHS,RHS), not holds(t,LHS), time(t).
holds(t,X) :- implies(X,LHS,RHS), holds(t,RHS).

% WAS: :- root(X), not holds(0,X).
% It must be on top w/ external atoms... it was too good to be true!

#show.
#show trace/2.
%#show (T,A,1): trace(T,A).
%#show (T,A,0): not trace(T,A), time(T), atomic(_,A).

#defined atomic/2.
#defined true/1.
#defined trace/2.
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
