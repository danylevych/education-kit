const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');
window.addEventListener('resize', () => {
    // existing code here
});

canvas.width = window.innerWidth;
canvas.height = window.innerHeight;
let pointsArray = [];
const maxDistance = 150;
const numPoints = 125;
let mousePoint = { x: null, y: null };
// Змінні для зірок
const starsArray = [];
const numStars = 200; // Кількість зірок
const shootingStarsArray = [];
const shootingStarChance = 0.005; // Ймовірність появи комети
const shootingStarSpeed = 8; // Швидкість комети
class Point {
    constructor(x, y) {
        this.x = x || Math.random() * canvas.width;
        this.y = y || Math.random() * canvas.height;
        this.vx = (Math.random() - 0.5) * 2;
        this.vy = (Math.random() - 0.5) * 2;
        this.radius = 2;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        if (this.x < 0 || this.x > canvas.width) this.vx *= -1;
        if (this.y < 0 || this.y > canvas.height) this.vy *= -1;
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = '#fff';
        ctx.fill();
        ctx.closePath();
    }
}
class Star {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height;
        this.radius = Math.random() * 1.5; // Розмір зірки
        this.opacity = Math.random(); // Прозорість зірки
        this.twinkleSpeed = Math.random() * 0.005 + 0.002; // Повільніша швидкість мерехтіння
    }
    update() {
        this.opacity += this.twinkleSpeed;
        if (this.opacity > 1 || this.opacity < 0) {
            this.twinkleSpeed *= -1; // Інверсія напрямку мерехтіння
        }
    }
    draw() {
        ctx.beginPath();
        ctx.arc(this.x, this.y, this.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(255, 255, 255, ${this.opacity})`;
        ctx.fill();
        ctx.closePath();
    }
}
class ShootingStar {
    constructor() {
        this.x = Math.random() * canvas.width;
        this.y = Math.random() * canvas.height / 2; // Початково десь на верхній половині екрана
        this.vx = Math.random() * shootingStarSpeed + 4; // Горизонтальна швидкість
        this.vy = Math.random() * shootingStarSpeed / 2 + 1; // Вертикальна швидкість
        this.length = Math.random() * 80 + 50; // Довжина комети
        this.opacity = 1;
    }
    update() {
        this.x += this.vx;
        this.y += this.vy;
        this.opacity -= 0.015; // Комета зникає поступово
        if (this.opacity <= 0) {
            // Видалення комети, коли вона зникає
            const index = shootingStarsArray.indexOf(this);
            if (index > -1) {
                shootingStarsArray.splice(index, 1);
            }
        }
    }
    draw() {
        ctx.beginPath();
        ctx.moveTo(this.x, this.y);
        ctx.lineTo(this.x - this.length, this.y - this.length / 2);
        ctx.strokeStyle = `rgba(255, 255, 255, ${this.opacity})`;
        ctx.lineWidth = 2;
        ctx.stroke();
        ctx.closePath();
    }
}
function createPoints() {
    for (let i = 0; i < numPoints; i++) {
        pointsArray.push(new Point());
    }
}
function createStars() {
    for (let i = 0; i < numStars; i++) {
        starsArray.push(new Star());
    }
}
function drawStars() {
    starsArray.forEach(star => {
        star.update();
        star.draw();
    });
}
function connectPoints() {
    ctx.lineWidth = 1; // Повертаємо стандартну товщину ліній для зв'язків
    for (let i = 0; i < pointsArray.length; i++) {
        for (let j = i + 1; j < pointsArray.length; j++) {
            const dx = pointsArray[i].x - pointsArray[j].x;
            const dy = pointsArray[i].y - pointsArray[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < maxDistance) {
                ctx.beginPath();
                ctx.moveTo(pointsArray[i].x, pointsArray[i].y);
                ctx.lineTo(pointsArray[j].x, pointsArray[j].y);
                ctx.strokeStyle = `rgba(255, 255, 255, ${1 - distance / maxDistance})`;
                ctx.stroke();
                ctx.closePath();
            }
        }
        // Додаємо зв'язок точок з точкою миші
        if (mousePoint.x && mousePoint.y) {
            const dx = pointsArray[i].x - mousePoint.x;
            const dy = pointsArray[i].y - mousePoint.y;
            const distance = Math.sqrt(dx * dx + dy * dy);
            if (distance < maxDistance) {
                ctx.beginPath();
                ctx.moveTo(pointsArray[i].x, pointsArray[i].y);
                ctx.lineTo(mousePoint.x, mousePoint.y);
                ctx.strokeStyle = `rgba(255, 255, 255, ${1 - distance / maxDistance})`;
                ctx.stroke();
                ctx.closePath();
            }
        }
    }
}
function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // Малюємо зірки
    drawStars();
    // Додаємо комету з певною ймовірністю
    if (Math.random() < shootingStarChance) {
        shootingStarsArray.push(new ShootingStar());
    }
    // Малюємо і оновлюємо комети
    shootingStarsArray.forEach(star => {
        star.update();
        star.draw();
    });
    pointsArray.forEach(point => {
        point.update();
        point.draw();
    });
    connectPoints();
    requestAnimationFrame(animate);
}
createPoints();
createStars();
animate();
// Відстеження руху миші
window.addEventListener('mousemove', (event) => {
    mousePoint.x = event.clientX;
    mousePoint.y = event.clientY;
});
window.addEventListener('resize', () => {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
});

function showAlert(message, where, type = 'warning') {
    const alertPlaceholder = document.getElementById(where);
    if (!alertPlaceholder) {
        console.error(`Element with ID ${where} not found.`);
        return;
    }

    // Видалення всіх існуючих сповіщень, залишаючи тільки одне
    const existingAlerts = alertPlaceholder.querySelectorAll('.alert');
    if (existingAlerts.length > 0) {
        existingAlerts[0].classList.add('fade-out');
        setTimeout(() => existingAlerts[0].remove(), 500); // Затримка на анімацію зникнення
    }

    // Створення нового сповіщення
    const wrapper = document.createElement('div');
    wrapper.innerHTML = `
        <div class="alert ${type}" role="alert">
            <div>${message}</div>
        </div>
    `;
    alertPlaceholder.append(wrapper);

    // Автоматичне приховування сповіщення через 7 секунд
    setTimeout(() => {
        wrapper.querySelector('.alert').classList.add('fade-out');
        setTimeout(() => wrapper.remove(), 500); // Затримка на анімацію зникнення
    }, 3000);
}


document.addEventListener('DOMContentLoaded', function () {
    // Функція для автоматичного зникнення сповіщення
    function autoDismissAlert() {
        const alertElement = document.querySelector('.alert');
        if (alertElement) {
            // Через 3 секунди додаємо клас для зникнення
            setTimeout(function () {
                alertElement.classList.add('fade-out');
                // Після завершення анімації видаляємо елемент з DOM
                setTimeout(function () {
                    alertElement.remove();
                }, 500); // Тривалість анімації (має відповідати часу анімації CSS)
            }, 3000); // 3 секунди перед зникненням
        }
    }

    // Викликаємо функцію
    autoDismissAlert();
});

function updateClock() {
    const now = new Date();
    const hours = String(now.getHours()).padStart(2, '0');
    const minutes = String(now.getMinutes()).padStart(2, '0');
    document.querySelector('.clock').textContent = `${hours}:${minutes}`;
}

setInterval(updateClock, 1000); // Оновлювати годинник кожну секунду
updateClock(); // Оновлюємо годинник відразу при завантаженні сторінки
