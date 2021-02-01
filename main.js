var admin = require("firebase-admin");
var serviceAccount = require("./robot-ent-firebase-adminsdk-6f9qm-1e07c7a9ab.json");

var {PythonShell} = require("python-shell",{pythonpath:'/usr/bin/python3'});

admin.initializeApp({
    credential: admin.credential.cert(serviceAccount),
    databaseURL: "https://robot-ent.firebaseio.com"
});

var db = admin.database();
var ref = db.ref("item");

const textEncoding = require("text-encoding");
const TextEncoder = textEncoding.TextEncoder;

var byteFormat = function(number,point,com){
    if(!point) point = 0;
    if(!com ) com = 1024;
    var bytes = Number(number),
	target = Math.floor(Math.log(bytes)/ Math.log(com));

    return (bytes / Math.pow(com,Math.floor(target))).toFixed(point);
}

ref.on("child_added",function(snapshot,prevChildKey){
    var newPost = snapshot.val();
    var pyshell = new PythonShell("./sock/get-data.py");
    var t = String(newPost.type);
    console.log("Get new data");
   
    if (t.indexOf('bright') > -1){
	var num = byteFormat(newPost.brightnessValue);
	let text = "bright" + num;
	pyshell.send(text);
    } else if (t.indexOf('bright_h') > -1){
	var num = byteFormat(newPost.brightnessValue);
	let text = "birght_h" + num;
	pyshell.send(text);
    } else if (t.indexOf('humi') > -1){
	var num = byteFormat(newPost.humiValue);
	let text = "humi" + num;
	pyshell.send(text);
    } else if (t.indexOf('temp') > -1){
	var num = byteFormat(newPost.tempValue);
	let text = "temp" + num;
	pyshell.send(text);
    } else if (t.indexOf('human') > -1){
	let text = "human";
	pyshell.send(text);
    }
	
    pyshell.end()
});

