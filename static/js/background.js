var canvas = document.getElementById("canvas");
var ctx = canvas.getContext("2d");

function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

// Canvasgröße an Fenstergröße anpassen
canvas.width = window.innerWidth;
canvas.height = window.innerHeight;

var balls = []; // Array, um die Kugeln zu speichern
var ballCount = 20; // Anzahl der Kugeln

// Farben für die Kugeln
var colors = ["red", "green", "blue", "orange", "purple", "yellow"];

// Kugel-Klasse
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

    // Kugel zurücksetzen, wenn sie den unteren Rand erreicht
    if (this.y > canvas.height) {
        this.y = -this.radius; // Zufällige Startposition oberhalb des Canvas setzen
        this.x = Math.random() * canvas.width; // Zufällige x-Position generieren
        this.color = colors[Math.floor(Math.random() * colors.length)]; // Zufällige Farbe auswählen
    }

    this.draw();
    }
}

// Kugeln erstellen und zum Array hinzufügen
for (var i = 0; i < ballCount; i++) {
    var x = Math.random() * canvas.width; // Zufällige x-Position generieren
    var y = Math.random() * canvas.height; // Zufällige y-Position generieren
    var radius = 20; // Größe der Kugeln
    var color = colors[Math.floor(Math.random() * colors.length)]; // Zufällige Farbe auswählen
    var dy = Math.random() * 2 + 1; // Zufällige Geschwindigkeit zwischen 1 und 3

    balls.push(new Ball(x, y, radius, color, dy));
}

// Animationsschleife
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    // Alle Kugeln aktualisieren und zeichnen
    for (var i = 0; i < balls.length; i++) {
    balls[i].update();
    }

    requestAnimationFrame(animate);
}

// Animation starten
animate();
