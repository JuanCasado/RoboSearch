
let map = null
let popup = null
let selected = null
let clicked = null
let plan = {}

const image = {
  height: 467,
  width: 477,
  imageUrl: './map.png',
}

const grid = {
  vSize: 40,
  hSize: 40,
  height: ()=>image.height/grid.vSize,
  width:  ()=>image.width /grid.hSize,
}

const waitTime = 600

const state = {
  states: ['Set Image', 'Get robot names', 'Get tasks names', 'Select where robots start', 'Select where tasks happen', 'Configure robots', 'Configure path planning', 'Set metric', 'Set name', 'Hit Create Plan button'],
  index: -1,
  current: ()=>{return state.states[state.index]},
  start: ()=>{state.index=-1;state.next()},
  next: ()=>{
    state.index=(state.index+1)%state.states.length
    document.getElementById('action').innerHTML=`<h1>${state.current()}</h1>`
    switch(state.index){
      case 0:{ //Set Image
        const imageName = window.prompt('Enter the name of the map image')
        grid.vSize=Number(window.prompt('Enter the vertical grid size'))
        grid.hSize=Number(window.prompt('Enter the horizontal grid size'))
        configureImage(imageName)
        plan.image=imageName
        plan.pathPlan={}
        plan.pathPlan.grid_size=[grid.hSize,grid.vSize]
        updatePlan()
      }break
      case 1:{ //Get robot name
        const robots = Number(window.prompt('Enter the number of robots'))
        let currentRobot = 0
        plan.robots=[]
        updatePlan()
        const getRobotName = ()=>{
          const robotName = window.prompt(`Enter the name of robot #${currentRobot+1}`)
          plan.robots.push({name: robotName})
          updatePlan()
          if (++currentRobot < robots) setTimeout(getRobotName, waitTime)
          else setTimeout(state.next, waitTime)
        }
        setTimeout(getRobotName, waitTime)
      }break
      case 2:{ // Get tasks names
        const tasks = Number(window.prompt('Enter the number of tasks'))
        let currentTask = 0
        plan.tasks=[]
        updatePlan()
        const getTaskName = ()=>{
          const taskName = window.prompt(`Enter the name of task #${currentTask+1}`)
          plan.tasks.push({name: taskName})
          updatePlan()
          if (++currentTask < tasks) setTimeout(getTaskName, waitTime)
          else setTimeout(state.next, waitTime)
        }
        setTimeout(getTaskName, waitTime)
      }break
      case 5: { // Configure robots
        let currentTask = 0
        let currentRobot = 0
        let currentSpeed = 0
        let robotStep = 0
        let taskStep = 0
        let speedStep = 0
        const configureRobotTask = () => {
          switch (taskStep){
            case 0: {
              const taskName = window.prompt(`Enter the name of a task that ${plan.robots[currentRobot].name} can perform`)
              if (!plan.robots[currentRobot].tasks)plan.robots[currentRobot].tasks=[]
              plan.robots[currentRobot].tasks.push({})
              plan.robots[currentRobot].tasks[currentTask].name = taskName
            }break
            case 1: {
              const duration = Number(window.prompt(`Enter the duration of task ${plan.robots[currentRobot].tasks[currentTask].name} of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].tasks[currentTask].duration = duration
            }break
            case 2: {
              const consume = Number(window.prompt(`Enter the consume of task ${plan.robots[currentRobot].tasks[currentTask].name} of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].tasks[currentTask].consume = consume
            }break
            case 3: {
              if (window.prompt(`Create another task for ${plan.robots[currentRobot].name} (YES to create)`)!=='YES'){
                robotStep=(robotStep+1)%6
              }
              ++currentTask
            }break
          }
          taskStep=(taskStep+1)%4
          setTimeout(configureRobot, waitTime)
        }
        const configureRobotSpeed = () => {
          switch (speedStep){
            case 0: {
              const speedName = window.prompt(`Enter the name of a speed that ${plan.robots[currentRobot].name} go at`)
              if (!plan.robots[currentRobot].speeds)plan.robots[currentRobot].speeds=[]
              plan.robots[currentRobot].speeds.push({})
              plan.robots[currentRobot].speeds[currentSpeed].name = speedName
            }break
            case 1: {
              const speed = Number(window.prompt(`Enter the value of speed ${plan.robots[currentRobot].speeds[currentSpeed].name} of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].speeds[currentSpeed].speed = speed
            }break
            case 2: {
              const consume = Number(window.prompt(`Enter the consume of speed ${plan.robots[currentRobot].speeds[currentSpeed].name} of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].speeds[currentSpeed].consume = consume
            }break
            case 3: {
              if (window.prompt(`Create another speed for ${plan.robots[currentRobot].name} (YES to create)`)!=='YES'){
                robotStep=(robotStep+1)%6
              }
              ++currentSpeed
            }break
          }
          speedStep=(speedStep+1)%4
          setTimeout(configureRobot, waitTime)
        }
        const configureRobot = ()=>{
          switch (robotStep) {
            case 0: {
              const battery = Number(window.prompt(`Enter battery of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].battery=battery
              robotStep=(robotStep+1)%6
              setTimeout(configureRobot, waitTime)
            }break
            case 1: {
              const maxBattery = Number(window.prompt(`Enter max battery of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].maxBattery=maxBattery
              robotStep=(robotStep+1)%6
              setTimeout(configureRobot, waitTime)
            }break
            case 2: {
              const rechargeRate = Number(window.prompt(`Enter recharge rate of ${plan.robots[currentRobot].name}`))
              plan.robots[currentRobot].rechargeRate=rechargeRate
              robotStep=(robotStep+1)%6
              setTimeout(configureRobot, waitTime)
            }break
            case 3: {
              configureRobotTask()
            }break
            case 4: {
              configureRobotSpeed()
            }break
            case 5: {
              if (++currentRobot < plan.robots.length) setTimeout(configureRobot, waitTime)
              else setTimeout(state.next, waitTime)
              robotStep=(robotStep+1)%6
              currentTask=0
              currentSpeed=0
            }
          }
          updatePlan()
        }
        setTimeout(configureRobot, waitTime)
      }break
      case 6: { // Configure path planning
        let step = 0
        const configurePathPlan = () => {
          switch (step) {
            case 0: {
              const heuristic = window.prompt(`Enter heuristic (manhattan | naive | euclidean | octile | dijkstra | chebyshev)}`)
              if (!plan.pathPlan) plan.pathPlan={}
              plan.pathPlan.heuristic=heuristic
              setTimeout(configurePathPlan, waitTime)
            }break
            case 1: {
              const algorithm = window.prompt(`Enter algorithm (Dijkstra  | A* | theta)}`)
              plan.pathPlan.algorithm=algorithm
              setTimeout(configurePathPlan, waitTime)
            }break
            case 2: {
              const scale = Number(window.prompt(`Enter scale (Number recommended: 1.001)`))
              plan.pathPlan.scale=scale
              setTimeout(configurePathPlan, waitTime)
            }break
            default:{
              setTimeout(state.next, waitTime)
            }break
          }
          ++step
        }
        updatePlan()
        setTimeout(configurePathPlan, waitTime)
      }break
      case 7: { // Set metric
        const metric = window.prompt(`Enter the metric to minimice (totalTime | totalBattery | totalDistance | recharges)`)
        plan.metric = metric
        updatePlan()
        setTimeout(state.next, waitTime)
      }
      case 8: { // Set name
        const name = window.prompt(`Enter the name of the problem`)
        plan.name = name
        updatePlan()
        initPlan()
      }
    }
  }
}

const handleSet = () => {
  const clickedUnits = toUnits(toCenter(clicked))
  switch (state.index) {
    case 3: { // Select where robots start
      const robotName = window.prompt('Enter the name of the robot that starts here')
      let named = 0
      for (robot in plan.robots) {
        if (plan.robots[robot].name === robotName) {
          plan.robots[robot].init = [clickedUnits.width, clickedUnits.height]
        }
        if (plan.robots[robot].init) ++named
      }
      updatePlan()
      if (named>=plan.robots.length) setTimeout(state.next, waitTime)
    }break;
    case 4: { // Select where tasks happen
      if (!plan.goals) plan.goals=[]
      const taskName = window.prompt('Enter the name of the task that happens here')
      for (task in plan.tasks) {
        if (plan.tasks[task].name === taskName) {
          const times = Number(window.prompt('How many times does the task happen'))
          plan.goals.push({action: taskName, point: [clickedUnits.width, clickedUnits.height], times: times})
        }
      }
      updatePlan()
      if (window.prompt('enter another task (NO to stop adding tasks)')==='NO') setTimeout(state.next, waitTime)
    }break;
  }
}

const readProblem = (event)=>{
  if (event.target.files.length){
    const reader = new FileReader()
    reader.onload = ()=>{
      const text = reader.result
      plan=JSON.parse(text)
      configureImage(plan.image)
      grid.vSize=plan.pathPlan.grid_size[0]
      grid.hSize=plan.pathPlan.grid_size[1]
      updatePlan()
      initPlan()
      end()
      startMap()
    }
    reader.readAsText(event.target.files[event.target.files.length-1])
  }
}

const createPlan = () => {
  axios.post('http://localhost/plan', plan).then((response)=>{
    document.getElementById('out').innerHTML=response.data
    done()
  }).catch(()=>{
    alert('The problem has an error')
  })
}

const validate = (point) => {
  const validPoint = {...point}
  if (point.height < 0) {validPoint.height = 0}
  if (point.width < 0) {validPoint.width = 0}
  if (point.height > image.height-1) {validPoint.height = image.height-1}
  if (point.width > image.width-1) {validPoint.width = image.width-1}
  validPoint.height = Math.floor(Math.floor(validPoint.height / grid.height())*grid.height())
  validPoint.width = Math.floor(Math.floor(validPoint.width / grid.width())*grid.width())
  return validPoint
}

const toGrid = (latlng) => {
  return {
    height: Math.round(image.height - latlng.lat),
    width: Math.round(latlng.lng),
  }
}

const toCenter = (point) => {
  return {
    height: Math.floor(point.height + grid.height()/2),
    width: Math.floor(point.width + grid.width()/2),
  }
}

const toMap = (point) => {
  return {
    lat: (image.height - point.height)-grid.height()/2,
    lng: point.width+grid.width()/2,
  }
}

const toUnits = (point) => {
  return {
    height: Math.round(point.height/grid.height()),
    width: Math.round(point.width/grid.width()),
  }
}

const configureImage = (imageName) => {
  const img = new Image()
  img.onload = function() {image.width=this.width;image.height=this.height}
  image.imageUrl=imageName
  img.src = `http://localhost/map/${image.imageUrl}`
}

let isObstacle = (point) =>  true
let removeImage = () => {}
const setImage = () => {
  removeImage()
  map.setMaxBounds(new L.LatLngBounds([[0,image.width+image.width*0.2], [image.height+image.height*0.2,0]]))
  const data = L.imageOverlay(`/map/${image.imageUrl}`, [[0,image.width], [image.height,0]]).addTo(map)
  const canvas = document.createElement('canvas')
  canvas.width = image.width
  canvas.height = image.height
  isObstacle = (point) => {
    canvas.getContext('2d').drawImage(data._image, 0, 0)
    const imagePoint = canvas.getContext('2d').getImageData(point.width, point.height, 1, 1).data
    return !(imagePoint[0]||imagePoint[1]||imagePoint[2])
  }
  removeImage = ()=>{canvas.remove()}
}

const updatePlan = () => {
  document.getElementById('out').innerHTML=JSON.stringify(plan, undefined, 2)
}

const pointDescription = (pointClicked) => {
  let description = ''
  const content = document.getElementById('out').getElementsByTagName('p')
  if (content.length >= 1)
    for (let child of content) {
      if (child.innerHTML.includes(`(${pointClicked.width}, ${pointClicked.height})`))
        description+=`<p>${child.innerHTML}</p>`
    }
  else {
    for (let robot of plan.robots) {
      if (robot.init[0]==pointClicked.width && robot.init[1]==pointClicked.height) 
        description+=`<p>Robot ${robot.name} starts here</p>`
    }
    for (let goal of plan.goals) {
      if (goal.point[0]==pointClicked.width && goal.point[1]==pointClicked.height) 
        description+=`<p>Goal ${goal.action} happens here ${goal.times} times</p>`
    }
  }
  return description
}

const click = (e) => {
  clicked = validate(toGrid(e.latlng))
  const clickedUnits = toUnits(toCenter(clicked))
  popup.setLatLng(toMap(clicked)).setContent(`
    <div>
      <h3>(${clickedUnits.width}, ${clickedUnits.height}) is a ${isObstacle(toCenter(clicked))?'obstacle':'valid point'}</h3>
      ${(state.index===3||state.index==4)?isObstacle(toCenter(clicked))?'':`
      <div id="popup-content">
        <button id="set" onclick="handleSet()" type="button" class="btn btn-success">SET</button>
      </div>`:pointDescription(clickedUnits)}
    </div>
  `).openOn(map)
}

const mousemove = (e) => {
  const start = validate ({
    height: image.height - Math.round(image.height - e.latlng.lat),
    width: Math.round(e.latlng.lng),
  })
  const end = {
    height: start.height + grid.height(),
    width: start.width + grid.width(),
  }
  selected.setBounds([[start.height, start.width], [end.height, end.width]])
  selected.addTo(map)
}

const initProblem = () => {
  document.getElementById('action').innerHTML=`<h1>Create a problem</h1>`
}
const initPlan = () => {
  document.getElementById('action').innerHTML=`<h1>Create a plan</h1>`
}
const done = () => {
  document.getElementById('action').innerHTML=`<h1>Plan is ready</h1>`
}

const startMap = () => {
  popup = L.popup()
  selected = L.rectangle([[0,0],[0,0]], {color: '#ffff0055', weight: 2, fillColor:'#000000bb'})
  map = L.map('map', {
    crs: L.CRS.Simple,
    attributionControl: false,
    minZoom:0,
  }).setView([0, 0], 0)
  setImage()
  map.on('click', click)
  map.on('mousemove', mousemove)
}

const start = () => {
  plan={}
  state.start()
  updatePlan()
  end()
  startMap()
  setTimeout(state.next, waitTime)
}
const end = () => {
  removeImage()
  if (map!==null){
    map.off('click', click)
    map.off('mousemove', mousemove)
    map.closePopup(popup)
    map.removeLayer(selected)
    map.off()
    map.remove()
  }
}
const reset = () => {
  end()
  initProblem()
}

document.addEventListener("DOMContentLoaded", ()=>{
  document.getElementById('start').onclick=start
  document.getElementById('reset').onclick=reset
  document.getElementById('create').onclick=createPlan
  document.getElementById('loader').onclick=()=>{document.getElementById('loaded').click()}
  document.getElementById('loaded').addEventListener('change', readProblem)
  initProblem()
})

