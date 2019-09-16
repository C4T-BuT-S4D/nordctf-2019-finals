function update() {
    var waitfor = new Date('Jan 1 31337');
    var current = new Date();
    var diff = new Date(waitfor - current);
    var result = [
        diff.getYear().toString(), 
        diff.getMonth().toString().padStart(2, "0"), 
        diff.getDay().toString().padStart(2, "0"), 
        diff.getMinutes().toString().padStart(2, "0"), 
        diff.getSeconds().toString().padStart(2, "0")
    ].join(":");
    document.getElementById("time").innerText = result;
}

window.onload = function() {
    update();
    setInterval(update, 1000);
}
