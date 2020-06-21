(define (problem probPlanetary) (:domain planetary) (:objects
 robot1 robot2 - robot
 LOCATION0 LOCATION1 LOCATION2 LOCATION3 LOCATION4 LOCATION5 LOCATION6 LOCATION7 - location
 SLOW FAST - speedType
 drill photo wave - taskType
)
(:init (= (totalTime) 0) (= (totalBattery) 0) (= (totalDistance) 0) (= (recharges) 0)
 (at robot1 LOCATION0)
(= (speed robot1 FAST) 40)(= (moveBurn robot1 FAST) 1)
 (= (speed robot1 SLOW) 20)(= (moveBurn robot1 SLOW) 0.2)
(= (battery robot1) 400) (= (maxBattery robot1) 400) (= (rechargeRate robot1) 1)
(= (taskDuration robot1 drill) 20) (= (taskBurn robot1 drill) 1)
 (= (taskDuration robot1 photo) 1) (= (taskBurn robot1 photo) 1)

 (at robot2 LOCATION1)
(= (speed robot2 FAST) 50)(= (moveBurn robot2 FAST) 1)
 (= (speed robot2 SLOW) 25)(= (moveBurn robot2 SLOW) 0.4)
(= (battery robot2) 500) (= (maxBattery robot2) 500) (= (rechargeRate robot2) 1)
(= (taskDuration robot2 drill) 15) (= (taskBurn robot2 drill) 1)
 (= (taskDuration robot2 wave) 1) (= (taskBurn robot2 wave) 2)


 (= (tasks LOCATION0 drill) 0)(= (tasks LOCATION1 drill) 0)(= (tasks LOCATION2 drill) 0)(= (tasks LOCATION3 drill) 0)(= (tasks LOCATION4 drill) 0)(= (tasks LOCATION5 drill) 0)(= (tasks LOCATION6 drill) 0)(= (tasks LOCATION7 drill) 0)(= (tasks LOCATION0 photo) 0)(= (tasks LOCATION1 photo) 0)(= (tasks LOCATION2 photo) 0)(= (tasks LOCATION3 photo) 0)(= (tasks LOCATION4 photo) 0)(= (tasks LOCATION5 photo) 0)(= (tasks LOCATION6 photo) 0)(= (tasks LOCATION7 photo) 0)(= (tasks LOCATION0 wave) 0)(= (tasks LOCATION1 wave) 0)(= (tasks LOCATION2 wave) 0)(= (tasks LOCATION3 wave) 0)(= (tasks LOCATION4 wave) 0)(= (tasks LOCATION5 wave) 0)(= (tasks LOCATION6 wave) 0)(= (tasks LOCATION7 wave) 0)

   (= (distance LOCATION0 LOCATION2) 282) (= (distance LOCATION0 LOCATION3) 100) (= (distance LOCATION0 LOCATION4) 94) (= (distance LOCATION0 LOCATION5) 344) (= (distance LOCATION0 LOCATION6) 367) (= (distance LOCATION0 LOCATION7) 212)   (= (distance LOCATION1 LOCATION2) 447) (= (distance LOCATION1 LOCATION3) 272) (= (distance LOCATION1 LOCATION4) 259) (= (distance LOCATION1 LOCATION5) 191) (= (distance LOCATION1 LOCATION6) 251) (= (distance LOCATION1 LOCATION7) 166) (= (distance LOCATION2 LOCATION0) 282) (= (distance LOCATION2 LOCATION1) 447)  (= (distance LOCATION2 LOCATION3) 240) (= (distance LOCATION2 LOCATION4) 275) (= (distance LOCATION2 LOCATION5) 306) (= (distance LOCATION2 LOCATION6) 278) (= (distance LOCATION2 LOCATION7) 287) (= (distance LOCATION3 LOCATION0) 100) (= (distance LOCATION3 LOCATION1) 272) (= (distance LOCATION3 LOCATION2) 240)  (= (distance LOCATION3 LOCATION4) 35) (= (distance LOCATION3 LOCATION5) 243) (= (distance LOCATION3 LOCATION6) 267) (= (distance LOCATION3 LOCATION7) 117) (= (distance LOCATION4 LOCATION0) 94) (= (distance LOCATION4 LOCATION1) 259) (= (distance LOCATION4 LOCATION2) 275) (= (distance LOCATION4 LOCATION3) 35)  (= (distance LOCATION4 LOCATION5) 256) (= (distance LOCATION4 LOCATION6) 286) (= (distance LOCATION4 LOCATION7) 119) (= (distance LOCATION5 LOCATION0) 344) (= (distance LOCATION5 LOCATION1) 191) (= (distance LOCATION5 LOCATION2) 306) (= (distance LOCATION5 LOCATION3) 243) (= (distance LOCATION5 LOCATION4) 256)  (= (distance LOCATION5 LOCATION6) 60) (= (distance LOCATION5 LOCATION7) 143) (= (distance LOCATION6 LOCATION0) 367) (= (distance LOCATION6 LOCATION1) 251) (= (distance LOCATION6 LOCATION2) 278) (= (distance LOCATION6 LOCATION3) 267) (= (distance LOCATION6 LOCATION4) 286) (= (distance LOCATION6 LOCATION5) 60)  (= (distance LOCATION6 LOCATION7) 184) (= (distance LOCATION7 LOCATION0) 212) (= (distance LOCATION7 LOCATION1) 166) (= (distance LOCATION7 LOCATION2) 287) (= (distance LOCATION7 LOCATION3) 117) (= (distance LOCATION7 LOCATION4) 119) (= (distance LOCATION7 LOCATION5) 143) (= (distance LOCATION7 LOCATION6) 184) 

 (connected LOCATION2 LOCATION0) (connected LOCATION4 LOCATION1) (connected LOCATION5 LOCATION0) (connected LOCATION0 LOCATION2) (connected LOCATION1 LOCATION5) (connected LOCATION6 LOCATION0) (connected LOCATION3 LOCATION6) (connected LOCATION1 LOCATION3) (connected LOCATION0 LOCATION5) (connected LOCATION5 LOCATION1) (connected LOCATION6 LOCATION1) (connected LOCATION4 LOCATION6) (connected LOCATION2 LOCATION6) (connected LOCATION0 LOCATION3) (connected LOCATION2 LOCATION1) (connected LOCATION3 LOCATION7) (connected LOCATION7 LOCATION4) (connected LOCATION5 LOCATION6) (connected LOCATION4 LOCATION7) (connected LOCATION5 LOCATION7) (connected LOCATION6 LOCATION7) (connected LOCATION7 LOCATION5) (connected LOCATION7 LOCATION2) (connected LOCATION2 LOCATION7) (connected LOCATION7 LOCATION3) (connected LOCATION3 LOCATION4) (connected LOCATION6 LOCATION4) (connected LOCATION2 LOCATION4) (connected LOCATION3 LOCATION2) (connected LOCATION5 LOCATION4) (connected LOCATION3 LOCATION5) (connected LOCATION4 LOCATION5) (connected LOCATION4 LOCATION2) (connected LOCATION5 LOCATION2) (connected LOCATION6 LOCATION2) (connected LOCATION2 LOCATION5) (connected LOCATION6 LOCATION5) (connected LOCATION1 LOCATION6) (connected LOCATION4 LOCATION3) (connected LOCATION5 LOCATION3) (connected LOCATION6 LOCATION3) (connected LOCATION0 LOCATION6) (connected LOCATION2 LOCATION3) (connected LOCATION1 LOCATION7) (connected LOCATION0 LOCATION7) (connected LOCATION7 LOCATION0) (connected LOCATION7 LOCATION6) (connected LOCATION7 LOCATION1) (connected LOCATION1 LOCATION4) (connected LOCATION3 LOCATION0) (connected LOCATION0 LOCATION4) (connected LOCATION4 LOCATION0) (connected LOCATION1 LOCATION2) (connected LOCATION3 LOCATION1)

)(:goal (and
 (= (tasks LOCATION7 drill) 3)
 (= (tasks LOCATION6 drill) 2)
 (= (tasks LOCATION4 drill) 3)
 (= (tasks LOCATION2 drill) 4)
 (= (tasks LOCATION5 photo) 1)
 (= (tasks LOCATION3 wave) 5)
))
 (:metric minimize (totalTime))
)
