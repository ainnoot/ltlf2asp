rules = {
	'state': {
		'product': """
state_empty(T) :- time(T), not trace(T,_).
state_cnt(T,P) :- time(T), P=#count{T,A: trace(T,A)}.
state_idx(T,0..P-1) :- state_cnt(T,P).
lex_min(T,0,A) :- time(T), A=#min{A: trace(T,A)}.
state_sort(T,0,A) :- lex_min(T,0,A).
state_sort(T,P,B) :- state_idx(T,P), state_sort(T,P-1,A), trace(T,B), B > A, #count{C: trace(T,C), C > A, C < B} = 0.
state_weight_acc(T,0,W) :- lex_min(T,0,A), weight(A,W).
state_weight_acc(T,P,W) :- state_weight_acc(T,P-1,V), state_sort(T,P,A), weight(A,X), W=V*X.
state_weight(T,W) :- state_cnt(T,P), state_weight_acc(T,P-1,W).
:~ trace_weight(W). [W@1,W]
		""",

		'sum': """
state_empty(T) :- time(T), not trace(T,_).
state_weight(T, 0) :- state_empty(T).
state_weight(T, W) :- time(T), not state_empty(T), W = #sum{W,A: trace(T,A), weight(A,W)}.
:~ trace_weight(W). [W@1,W]
		""",

		'max': """
state_empty(T) :- time(T), not trace(T,_).
state_weight(T, 0) :- state_empty(T).
state_weight(T, W) :- time(T), not state_empty(T), W = #max{W,A: trace(T,A), weight(A,W)}.
:~ trace_weight(W). [W@1,W]
		""",
	},
	'trace': {
		'product': """
trace_weight(0) :- trace_empty.
trace_empty :- not trace(_,_).
trace_cnt(P-1) :- last_instant(P), not trace_empty.
trace_weight_acc(0,W) :- state_weight(0,W), not trace_empty.
trace_weight_acc(T,W) :- time(T), trace_weight_acc(T-1,V), trace_weight(T,X), W=V*X, not trace_empty.
trace_weight(W) :- trace_weight_acc(T,W), last_instant(T), not trace_empty.
:~ trace_weight(W). [W@1,W]
		""",

		'sum': """
trace_empty :- not trace(_,_).
trace_weight(0) :- trace_empty.
trace_weight(W) :- time(T), W=#sum{W,T: state_weight(T,W)}.
:~ trace_weight(W). [W@1,W]
		""",

		'max': """
trace_empty :- not trace(_,_).
trace_weight(0) :- trace_empty.
trace_weight(W) :- time(T), W=#max{W,T: state_weight(T,W)}.
:~ trace_weight(W). [W@1,W]
		""",
	}
}



%%% MAX %%%


%%% PROD %%%


%%% Trace Weights %%%
%%% SUM %%%


%%% MAX %%%


%%% PROD %%%



