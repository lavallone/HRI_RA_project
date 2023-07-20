(define (domain simple_grid)
    (:requirements :strips)
    (:predicates (agent ?x) (at ?x ?y) (door ?w) (adj ?x ?y))
    (:action move
        :parameters (?r ?from ?to)
        :effect (and (not(at ?r ?from)) (at ?r ?to))
        :precondition (and (agent ?r) (at ?r ?from) (adj ?from ?to) )
    )
    
)