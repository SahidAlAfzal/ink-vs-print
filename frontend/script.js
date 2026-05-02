function checkSimilarity() {
    // Mock OCR extraction
    document.getElementById("text1").value = "The quick brown fox jumps over the lazy dog.";
    document.getElementById("text2").value = "A quick brown fox jumped over a lazy dog.";

    // Generating dummy similarity scores
    let edit = (Math.random() * 0.3 + 0.6).toFixed(2); 
    let tfidf = (Math.random() * 0.2 + 0.7).toFixed(2);
    let embed = (Math.random() * 0.1 + 0.85).toFixed(2);

    let finalValue = ((+edit + +tfidf + +embed) / 3);
    let finalDisplay = (finalValue * 100).toFixed(1) + "%";

    // Update UI with a slight delay for "processing" feel
    setTimeout(() => {
        document.getElementById("editScore").innerText = edit;
        document.getElementById("tfidfScore").innerText = tfidf;
        document.getElementById("embedScore").innerText = embed;
        document.getElementById("finalScore").innerText = finalDisplay;
    }, 300);
}

/* --- ENHANCED INTERACTIVE BACKGROUND SCRIPT --- */
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let particles = [];
let mouse = { x: null, y: null, radius: 150 };

function initCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
}

class Particle {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.size = Math.random() * 3 + 1;
        this.baseX = this.x;
        this.baseY = this.y;
        this.density = (Math.random() * 30) + 1;
        this.speedX = Math.random() * 0.6 - 0.3;
        this.speedY = Math.random() * 0.6 - 0.3;
    }
    
    update() {
        // Mouse interaction
        let dx = mouse.x - this.x;
        let dy = mouse.y - this.y;
        let distance = Math.sqrt(dx * dx + dy * dy);
        let forceDirectionX = dx / distance;
        let forceDirectionY = dy / distance;
        let maxDistance = mouse.radius;
        let force = (maxDistance - distance) / maxDistance;
        let directionX = forceDirectionX * force * this.density;
        let directionY = forceDirectionY * force * this.density;

        if (distance < mouse.radius) {
            this.x -= directionX;
            this.y -= directionY;
        } else {
            // Return to base position
            if (this.x !== this.baseX) {
                let dx = this.x - this.baseX;
                this.x -= dx / 10;
            }
            if (this.y !== this.baseY) {
                let dy = this.y - this.baseY;
                this.y -= dy / 10;
            }
        }

        // Continuous drift
        this.baseX += this.speedX;
        this.baseY += this.speedY;

        // Wrap around screen
        if (this.baseX > canvas.width) this.baseX = 0;
        if (this.baseX < 0) this.baseX = canvas.width;
        if (this.baseY > canvas.height) this.baseY = 0;
        if (this.baseY < 0) this.baseY = canvas.height;
    }
    
    draw() {
        ctx.fillStyle = 'rgba(99, 102, 241, 0.6)';
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
        ctx.fill();
    }
}

function createParticles() {
    particles = [];
    let numberOfParticles = (canvas.width * canvas.height) / 9000;
    for (let i = 0; i < numberOfParticles; i++) {
        particles.push(new Particle());
    }
}

function connectParticles() {
    for (let a = 0; a < particles.length; a++) {
        for (let b = a; b < particles.length; b++) {
            let dx = particles[a].x - particles[b].x;
            let dy = particles[a].y - particles[b].y;
            let distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 120) {
                let opacity = 1 - (distance / 120);
                ctx.strokeStyle = `rgba(99, 102, 241, ${opacity * 0.3})`;
                ctx.lineWidth = 1;
                ctx.beginPath();
                ctx.moveTo(particles[a].x, particles[a].y);
                ctx.lineTo(particles[b].x, particles[b].y);
                ctx.stroke();
            }
        }
    }
}

function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    
    particles.forEach(p => {
        p.update();
        p.draw();
    });
    
    connectParticles();
    requestAnimationFrame(animate);
}

// Mouse move event
window.addEventListener('mousemove', (e) => {
    mouse.x = e.x;
    mouse.y = e.y;
});

// Mouse leave event
window.addEventListener('mouseleave', () => {
    mouse.x = null;
    mouse.y = null;
});

// Touch support for mobile
window.addEventListener('touchmove', (e) => {
    e.preventDefault();
    mouse.x = e.touches[0].clientX;
    mouse.y = e.touches[0].clientY;
}, { passive: false });

window.addEventListener('touchend', () => {
    mouse.x = null;
    mouse.y = null;
});

// Resize handler
let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => {
        initCanvas();
        createParticles();
    }, 100);
});

// Initialize
initCanvas();
createParticles();
animate();