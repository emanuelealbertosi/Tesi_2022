#!/usr/local/bin/swipl -f -q
%:- set_prolog_flag(verbose, silent).
%:- initialization (secfaas2fog(ChainName, Placement),writeln(Placement),halt(1)).
:-style_check(-singleton).
:- use_module(library(lists)).
:- initialization (secfaas2fog(OrchId, Placement),writeln(Placement),halt(1)).
%DA VERIFICARE PER VELOCIZZARE
%:- initialization (once(secfaas2fog(OrchId, Placement),writeln(Placement),)).

%:- initialization (printOrch(Orchestration, Graph, Preamble),writeln(Graph),halt(1)).

%:- initialization forall(secfaas2fog(ChainName, Placement), writeln(Placement)).
:- consult('infrastructure').
:- consult('application').
:- consult('wellformedness').
:- consult('typing').
:- consult('blobify').
:- consult('padding').
:- consult('mapping').
:- consult('utils').
:- consult('print').

secfaas2fog(OrchId, Placement):-
	functionOrch(OrchId, (GeneratorId,TriggerTypes), Orchestration),
	wellFormed(Orchestration,WFOrchestration),
    typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration),
    padding(TypedOrchestration, PadOrchestration),
    placement(PadOrchestration, GeneratorId, Placement).


%%%%TEST predicates
%notDuplicate(OrchId):-
%	findall(P,secfaas2fog(OrchId, P), Ps),
%	list_to_set(Ps,S),
%	length(Ps, R1),
%	length(S, R2),
%	R1 =:= R2. 
%
%testTyping(OrchId, TypedOrchestration):-
%	functionOrch(OrchId, (_,TriggerTypes), Orchestration),
%	wellFormed(Orchestration,WFOrchestration),
%	typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration).
%
%testTypingBlob(OrchId, BlobedOrchestration):-
%	functionOrch(OrchId, (_,TriggerTypes), Orchestration),
%	wellFormed(Orchestration,WFOrchestration),
%	typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration),
%	blobify(TypedOrchestration, BlobedOrchestration).
%
%testPadFormat(OrchId, PadOrchestration):-
%    functionOrch(OrchId, (_,TriggerTypes), Orchestration),
%	wellFormed(Orchestration,WFOrchestration),
%    typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration),
%    padding(TypedOrchestration, PadOrchestration).
%
%testPad(OrchId, PadOrchestration):-
%    functionOrch(OrchId, (_,TriggerTypes), Orchestration),
%	wellFormed(Orchestration,WFOrchestration),
%    typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration),
%    padding(TypedOrchestration, PadOrchestration).
%
%testPadMap(OrchId, Placement):-
%    functionOrch(OrchId, (GeneratorId,TriggerTypes), Orchestration),
%	wellFormed(Orchestration,WFOrchestration),
%    typePropagation(TriggerTypes,WFOrchestration,TypedOrchestration),
%    padding(TypedOrchestration, PadOrchestration),
%    placement(PadOrchestration, GeneratorId, Placement).
%
%notDuplicatePad(OrchId):-
%	findall(P,testPadMap(OrchId, P), Ps),
%	sort(Ps,S),
%	length(Ps, R1),
%	length(S, R2),
%	R1 =:= R2,
%    dif(R1,0). 
%
%wellFormedTest(OrchId, NewOrchestration):- 
%	functionOrch(OrchId, _, Orchestration),
%	wellFormed(Orchestration, NewOrchestration).


%main :-
%  current_prolog_flag(argv, Argv),
%  format('Hello World, argv:~w\n', [Argv]]),
%  halt(0).