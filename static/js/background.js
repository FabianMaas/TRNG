var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var balls = []; 
var ballCount = 20; 

var colors = ["red", "green", "blue", "orange", "purple", "yellow"];

function Ball(x, y, radius, color, dy) {
    this.x = x;
    this.y = y;
    this.radius = radius;
    this.color = color;
    this.dy = dy;

    this.draw = function() {
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
    ctx.fillStyle = this.color;
    ctx.fill();
    ctx.closePath();
    }

    this.update = function() {
    this.y += this.dy;

    if (this.y > canvas.height) {
        this.y = -this.radius; 
        this.x = Math.random() * canvas.width; 
        this.color = colors[Math.floor(Math.random() * colors.length)]; 
    }

    this.draw();
    }
}

// Create Balls
for (var i = 0; i < ballCount; i++) {
    var x = Math.random() * canvas.width; 
    var y = Math.random() * canvas.height; 
    var radius = 20; // Größe der Kugeln
    var color = colors[Math.floor(Math.random() * colors.length)]; 
    var dy = Math.random() * 2 + 1; 

    balls.push(new Ball(x, y, radius, color, dy));
}

// Animation Loop
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Update and draw balls
    for (var i = 0; i < balls.length; i++) {
    balls[i].update();
    }

    requestAnimationFrame(animate);
}

// Start animation
animate();