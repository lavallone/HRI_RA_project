// log display function
function append(text) {
  // document.getElementById("websocket_events").insertAdjacentHTML('beforeend', "<li>" + text + ";</li>");
  console.log(text);
} 

// websocket global variable
var websocket = null;

function wsrobot_connected() {
  var connected = false;
  if (websocket!=null)
    console.log("websocket.readyState: "+websocket.readyState)
  if (websocket!=null && websocket.readyState==1) {
    connected = true;
  }
  console.log("connected: "+connected)
  return connected;
}

function wsrobot_init(port) {
    var ip = document.getElementById("IP").value;
    var url = "ws://"+ip+":"+port+"/websocketserver";
    console.log(url);
    websocket = new WebSocket(url);

    websocket.onmessage = function(event){
      append("message received: "+event.data);
      document.getElementById("status").innerHTML = event.data;
    } 

    websocket.onopen = function(){
      append("connection received");
    } 

    websocket.onclose = function(){
      append("connection closed");
    }

    websocket.onerror = function(){
      append("!!!connection error!!!");
    }

}
 
function wsrobot_quit() {
    websocket.close();
    websocket = null;
}

function wsrobot_send(data) {
  if (websocket!=null)
    websocket.send(data);
}


function button_fn(data) {
  // console.log('websocket button...')
  wsrobot_send(data);
}


