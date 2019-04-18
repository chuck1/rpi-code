
var socket = null;

function string_to_int_array_8(data) {
	var byteCharacters = atob(data);
	var byteNumbers = new Array(byteCharacters.length);
	for (var i = 0; i < byteCharacters.length; i++) {
		byteNumbers[i] = byteCharacters.charCodeAt(i);
	}
	var byteArray = new Uint8Array(byteNumbers);
	return byteArray;
}

var CHUNK = 256;


//var chunks_played = 0;
//var chunks_received = 0;
var position_play = 0;
var position_receive = 0;




function open_socket(ws_url, msg) {

	socket = new WebSocket(ws_url);

	socket.onclose = function (event) {
		console.log('closed', event);
	};

	socket.onerror = function (event) {
		console.log('error', event);
	};

	// Connection opened
	socket.onopen = function (event) {
		console.log('open. state=',socket.readyState);

		console.log('send', msg);

		socket.send(msg);
	};

	// Listen for messages
	socket.onmessage = function (evt) {
		console.log('Message from server', evt.data);
		var msg = JSON.parse(evt.data);

		else if(msg['type']=='text') {
			console.log(msg['data']);
		}
	};
}


function socket_send(msg) {
	console.log('websocket send. state=', socket.readyState);

	s = socket.readyState;

	if((s == WebSocket.CLOSED) || (s == WebSocket.CLOSING)) {
		console.log('websocket is closed or closing. reconnect.');
		open_socket(msg);
	}
	else
	{
		socket.send(msg);
	}
}

window.onload = function(){
	var split = window.location.href.split("/");

	var ws_url = "ws://" + split[2] + "/ws";
	//var ws_url = "http://" + split[2] + "/ws";
	//var ws_url = "ws://" + split[2].split(":")[0] + ":12002" + "/ws";

	console.log("ws_url", ws_url);

	open_socket(ws_url, JSON.stringify("hello"));

	var body = document.getElementById("body");

	var buttons = [
		"up",
		"down",
		];

	for(let s of buttons) {
		var button = document.createElement("button");
		body.appendChild(button);

		button.addEventListener("mousedown" () => {
			socket_send(JSON.stringify({
				event_type: "mousedown",
				element: s,
			}));
		});

		button.addEventListener("mouseup" () => {
			socket_send(JSON.stringify({
				event_type: "mouseup",
				element: s,
			}));
		});

		button.addEventListener("mouseleave" () => {
			socket_send(JSON.stringify({
				event_type: "mouseleave",
				element: s,
			}));
		});
	}

	for(let s of sliders) {
		var e = document.createElement("input");
		e.setAttribute("type", "range");

		var e1 = document.createElement("p");
		e1.innerHTML = s;

		var e2 = document.createElement("p");
		e2.innerHTML = e.value;

		body.appendChild(e1);
		body.appendChild(e);

		e.addEventListener("input", () => {
			socket_send(JSON.stringify({
				event_type: "range_input",
				element: s,
				value: e.value,
			}));
		});
	}


}




