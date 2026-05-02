async function checkSimilarity() {
    console.log("1. Button clicked! Grabbing files...");
    const doc1 = document.getElementById("doc1").files[0];
    const doc2 = document.getElementById("doc2").files[0];

    if (!doc1 || !doc2) {
        alert("Please upload both documents first!");
        return;
    }

    const btn = document.querySelector("button");
    btn.innerText = "Analyzing... (This takes a minute)";
    btn.disabled = true;

    const formData = new FormData();
    formData.append("doc1", doc1);
    formData.append("doc2", doc2);

    try {
        console.log("2. Sending files to Python API...");
        const response = await fetch("http://127.0.0.1:8000/analyze", {
            method: "POST",
            body: formData
        });

        console.log("3. Waiting for Python to finish...");
        const data = await response.json();
        console.log("4. Received data from Python:", data); 

        if (data.status === "success") {
            // Update Text Areas
            document.getElementById("text1").value = data.text1;
            document.getElementById("text2").value = data.text2;

            // Update Math Scores
            document.getElementById("editScore").innerText = data.scores.edit_similarity;
            document.getElementById("tfidfScore").innerText = data.scores.tfidf_similarity;
            document.getElementById("embedScore").innerText = data.scores.embedding_similarity;
            
            let finalPercent = (data.scores.final_normalized_score * 100).toFixed(1);
            document.getElementById("finalScore").innerText = finalPercent + "%";
            
            console.log("5. UI Updated Successfully!");
        }
    } catch (error) {
        console.error("CRITICAL ERROR:", error);
        alert("Something went wrong! Check the console.");
    } finally {
        btn.innerText = "⚡ Compare Documents";
        btn.disabled = false;
    }
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
            if (this.x !== this.baseX) {
                let dx = this.x - this.baseX;
                this.x -= dx / 10;
            }
            if (this.y !== this.baseY) {
                let dy = this.y - this.baseY;
                this.y -= dy / 10;
            }
        }

        this.baseX += this.speedX;
        this.baseY += this.speedY;

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
    particles.forEach(p => { p.update(); p.draw(); });
    connectParticles();
    requestAnimationFrame(animate);
}

window.addEventListener('mousemove', (e) => { mouse.x = e.x; mouse.y = e.y; });
window.addEventListener('mouseleave', () => { mouse.x = null; mouse.y = null; });
window.addEventListener('touchmove', (e) => {
    e.preventDefault();
    mouse.x = e.touches[0].clientX;
    mouse.y = e.touches[0].clientY;
}, { passive: false });
window.addEventListener('touchend', () => { mouse.x = null; mouse.y = null; });

let resizeTimeout;
window.addEventListener('resize', () => {
    clearTimeout(resizeTimeout);
    resizeTimeout = setTimeout(() => { initCanvas(); createParticles(); }, 100);
});

initCanvas();
createParticles();
animate();