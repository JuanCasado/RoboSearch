
(define (domain planetary)

  (:requirements 
    :strips 
    :fluents 
    :durative-actions 
    :timed-initial-literals 
    :typing 
    :conditional-effects 
    :negative-preconditions 
    :equality
    :constraints
    :preferences
  )

  (:types
    robot
    location
    speedType
    taskType
  )

  (:predicates
    (at ?robot - robot ?location - location)
    (connected ?from - location ?to - location)
  )

  ;(:constraints (and
  ;  (forall (?robot - robot) (always 
  ;    (> (battery ?robot) 0)
  ;  ))
  ;))

  (:functions
    (distance ?from - location ?to - location)
    (speed ?robot - robot ?speedType - speedType)
    (battery ?robot - robot)
    (moveBurn ?robot - robot ?speedType - speedType)
    (taskBurn ?robot - robot ?taskType - taskType)
    (maxBattery ?robot - robot)
    (rechargeRate ?robot - robot)
    (tasks ?location - location ?taskType - taskType)
    (taskDuration ?robot - robot ?taskType - taskType)
    (totalTime)
    (totalBattery)
    (totalDistance)
    (recharges)
  )

  (:durative-action move
    :parameters (
      ?robot - robot
      ?from - location
      ?to - location
      ?speedType - speedType
    )
    :duration (= ?duration (/(distance ?from ?to) (speed ?robot ?speedType)))
    :condition (and 
      (at start (at ?robot ?from))
      (over all (connected ?from ?to))
      (at end (> (battery ?robot) 0))
    )
    :effect (and 
      (at start (not (at ?robot ?from)))
      (at end (at ?robot ?to))
      (at end (decrease (battery ?robot) (* (distance ?from ?to) (moveBurn ?robot ?speedType))))
      (at end (increase (totalBattery) (* (distance ?from ?to) (moveBurn ?robot ?speedType))))
      (at end (increase (totalTime) (/ (distance ?from ?to) (speed ?robot ?speedType))))
      (at end (increase (totalDistance) (distance ?from ?to)))
    )
  )

  (:durative-action recharge
    :parameters (
      ?robot - robot
      ?location - location
    )
    :duration (= ?duration (* (- (maxBattery ?robot) (battery ?robot)) (rechargeRate ?robot)))
    :condition (and
      (over all (< (battery ?robot) (maxBattery ?robot)))
      (over all (at ?robot ?location))
    )
    :effect (and 
      (at end (assign (battery ?robot) (maxBattery ?robot)))
      (at end (increase (totalTime) (* (- (maxBattery ?robot) (battery ?robot)) (rechargeRate ?robot))))
      (at end (increase (recharges) 1))
    )
  )
  
  
  (:durative-action performTask
    :parameters (
      ?robot - robot
      ?location - location
      ?taskType - taskType
    )
    :duration (= ?duration (taskDuration ?robot ?taskType))
    :condition (and
      (over all (at ?robot ?location))
      (at start (> (battery ?robot) (*(taskBurn ?robot ?taskType) (taskDuration ?robot ?taskType))))
    )
    :effect (and 
      (at end (increase (tasks ?location ?taskType) 1))
      (at end (decrease (battery ?robot) (*(taskBurn ?robot ?taskType) (taskDuration ?robot ?taskType))))
      (at end (increase (totalBattery) (*(taskBurn ?robot ?taskType) (taskDuration ?robot ?taskType))))
      (at end (increase (totalTime) (taskDuration ?robot ?taskType)))
    )
  )

)