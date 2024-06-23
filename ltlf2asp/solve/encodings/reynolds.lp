#const depth=8.
state_id(0..depth-1).

% Initial formula is the root of the tableaux
clumsy_node(F,next(G)) :- next(F,G).
clumsy_node(F,weak_next(G)) :- weak_next(F,G).
state(0, R) :- root(R), not clumsy_node(R,_).
state(0, F) :- root(R), clumsy_node(R,F).

% Assuming negation normal form, we need only rules for U, R, &&, ||
expandable(F) :- conjunction(F,_).
expandable(F) :- disjunction(F,_).
expandable(F) :- until(F,_,_).
expandable(F) :- release(F,_,_).

% Pruning rule "Empty": the node does not contain any X(...) sequent
% so we found an accepting branch.
% WX in the state does not yield -empty/1 because WX is vacuously true in the last instant
-empty(T) :- state(T, next(F)).
-empty(T) :- state(T, F), expandable(F).

% EMPTY pruning rule triggers if there's no reason to expand further the current node
empty(T) :- reached_depth(T), not -empty(T), not conflict(T).


% CONFLICT pruning rule triggers if opposite literals are in the same node
% or if we insert a bottom in the node
conflict(T) :- state(T,F), state(T,G), atomic(F,L), atomic(G,-L).
conflict(T) :- state(T,false).
conflict(T) :- state(T,-true).

% LOOP pruning rule triggers if a there's a back-edge in the tableaux tree-branch
% !!!!!!!! In Nicola paper this rule is called PRUNE, LOOP is a pruning rule for
% LTL (no finite traces)
diff(T,T') :- T < T', state(T',_), state(T,F), not state(T',F).
diff(T,T') :- T < T', state(T,_), state(T',F), not state(T,F).
loop(T') :- T < T', not diff(T,T'), reached_depth(T), reached_depth(T').

% A branch is closed iff it triggers a pruning rule
close_branch(T) :- empty(T).
close_branch(T) :- conflict(T).
close_branch(T) :- loop(T).
open_branch(T) :- reached_depth(T), not close_branch(T).

% If a state contains an expandable formula, it must be expanded.
% If a state can't be expanded, but contains X/WX formulae, we might progress it
expand(T) :- state(T,F), expandable(F).
progress(T) :- state(T,next(F)), not expand(T), not close_branch(T).
progress(T) :- state(T,weak_next(F)), not expand(T), not close_branch(T).

% Big choice rule to model which expansion rules are available in a given state
{
  expand_until_left(T,F): state(T,F), until(F,_,_);
  expand_until_right(T,F): state(T,F), until(F,_,_);
  expand_conjunction(T,F): state(T,F), conjunction(F,_);
  expand_disjunction(T,F): state(T,F), disjunction(F,_);
  expand_release_left(T,F): state(T,F), release(F,_,_);
  expand_release_right(T,F): state(T,F), release(F,_,_)
} = 1 :- expand(T), open_branch(T).

% Project over subformulae affected by expansion rules (we need it for inertia (*))
affected(T,G) :- expand_until_left(T,G).
affected(T,G) :- expand_until_right(T,G).
affected(T,G) :- expand_conjunction(T,G).
affected(T,G) :- expand_disjunction(T,G).
affected(T,G) :- expand_release_right(T,G).
affected(T,G) :- expand_release_left(T,G).

% Program is satisfiable if we have enough depth to close a tableaux branch. When unsatisfiable,
% double up horizon and re-run.
reached_depth(T) :- state(T,_), state_id(T).
:- reached_depth(T), not reached_depth(T+1), open_branch(T).

% (*) Inertia law for unaffected sequents in a tableaux node
pre_state(T+1,F) :- state(T,F), not affected(T,F), expand(T), state_id(T+1).

% a U b \equiv b | X(a U b)
%%% UNTIL
pre_state(T+1,LHS) :- expand_until_left(T,F), until(F,LHS,RHS).
pre_state(T+1,next(F)) :- expand_until_left(T,F), until(F,LHS,RHS).
pre_state(T+1,RHS) :- expand_until_right(T,F), until(F,LHS,RHS).

% a R b \equiv (a & b) | b & WX(a U b)
%%% RELEASE
pre_state(T+1, LHS) :- expand_release_left(T,F), release(F,LHS,RHS).
pre_state(T+1, RHS) :- expand_release_left(T,F), release(F,LHS,RHS).
pre_state(T+1, weak_next(F)) :- expand_release_right(T,F), release(F,LHS,RHS).
pre_state(T+1, RHS) :- expand_release_right(T,F), release(F,LHS,RHS).

%%% CONJUNCTION, DISJUNCTION
pre_state(T+1,G) :- expand_conjunction(T,F), conjunction(F,G).
1 { pre_state(T+1,G): disjunction(F,G) } :- expand_disjunction(T,F).

% progress(t) is in the answer set if expand(t) is not;
% if progress(t) is in the model, there are no affected sequents in state(t);
% all sequents are discarded
% we re-insert in state(t+1) all sequents scoped in X,WX
pre_state(T+1,F) :- progress(T), state(T,next(F)).
pre_state(T+1,F) :- progress(T), state(T,weak_next(F)).

state(T+1,F) :- pre_state(T+1,F), not clumsy_node(F,_).
state(T+1,F) :- pre_state(T+1,G), clumsy_node(G,F).

% We can decode a satisfying trace if we applied the EMPTY rule
result(sat) :-   close_branch(T), empty(T).

% If we find a loop or a conflict, the current branch is not an accepting branch
result(unsat) :- close_branch(T), conflict(T).
result(unsat) :- close_branch(T), loop(T).

#show state/2.
#show loop/1.
#show expand/1.
#show conflict/1.
#show progress/1.
#show open_branch/1.
#show close_branch/1.
#show empty/1.
#defined state/2.
#defined loop/1.
#defined expand/1.
#defined conflict/1.
#defined progress/1.
#defined open_branch/1.
#defined close_branch/1.
#defined result/1.
#defined empty/1.
#defined until/3.
#defined release/3.
#defined conjunction/2.
#defined disjunction/2.
#defined next/2.
#defined weak_next/2.
#defined atomic/2.

% Answer sets of the program are closed branches, either accepting or unaccepting
% If an accepting branch exists, it will have optimal cost.
:~ result(unsat). [1@1]

% Given P \cup [\phi], if it is:
% unsatisfiable --> depth is not big enough to find a model/prove unsatisfiability
% satisfiable
%   -> optimal model contains result(sat)   --> we found a model
%   -> optimal model contains result(unsat) --> formula is unsatisfiable

% finds the shortest branch
%:~ state(T,_). [1@1,T]
