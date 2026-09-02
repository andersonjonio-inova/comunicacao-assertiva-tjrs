const slides = [...document.querySelectorAll('.slide')];
const previous = document.querySelector('#previous');
const next = document.querySelector('#next');
const play = document.querySelector('#play');
const counter = document.querySelector('#counter');
const fullscreen = document.querySelector('#fullscreen');
const audioFile = document.querySelector('#audio-file');
const soundtrack = document.querySelector('#soundtrack');
const interval = 7200;
let current = 0;
let timer = null;

function show(index) {
  current = Math.max(0, Math.min(index, slides.length - 1));
  slides.forEach((slide, position) => slide.classList.toggle('active', position === current));
  counter.textContent = `${current + 1} / ${slides.length}`;
  history.replaceState(null, '', `#${current + 1}`);
  if (current === slides.length - 1) stop();
}

function start() {
  if (current === slides.length - 1) show(0);
  clearInterval(timer);
  timer = setInterval(() => show(current + 1), interval);
  play.textContent = 'Pausar';
  play.setAttribute('aria-pressed', 'true');
  if (soundtrack.src) soundtrack.play().catch(() => {});
}

function stop() {
  clearInterval(timer);
  timer = null;
  play.textContent = 'Iniciar';
  play.setAttribute('aria-pressed', 'false');
  soundtrack.pause();
}

previous.addEventListener('click', () => show(current - 1));
next.addEventListener('click', () => show(current + 1));
play.addEventListener('click', () => timer ? stop() : start());
fullscreen.addEventListener('click', () => document.fullscreenElement ? document.exitFullscreen() : document.documentElement.requestFullscreen());
audioFile.addEventListener('change', () => {
  const [file] = audioFile.files;
  if (!file) return;
  soundtrack.src = URL.createObjectURL(file);
  soundtrack.loop = true;
  document.querySelector('.audio-button').textContent = 'Trilha carregada';
});

document.addEventListener('keydown', event => {
  if (event.target.matches('input, button')) return;
  if (['ArrowRight', 'PageDown', ' '].includes(event.key)) { event.preventDefault(); show(current + 1); }
  if (['ArrowLeft', 'PageUp', 'Backspace'].includes(event.key)) { event.preventDefault(); show(current - 1); }
  if (event.key.toLowerCase() === 'p') timer ? stop() : start();
  if (event.key.toLowerCase() === 'f') fullscreen.click();
});

let touchStart = null;
let touchStartY = null;
document.addEventListener('touchstart', event => {
  touchStart = event.changedTouches[0].clientX;
  touchStartY = event.changedTouches[0].clientY;
}, { passive: true });
document.addEventListener('touchend', event => {
  if (touchStart === null) return;
  const delta = event.changedTouches[0].clientX - touchStart;
  const deltaY = event.changedTouches[0].clientY - touchStartY;
  if (Math.abs(delta) > 55 && Math.abs(delta) > Math.abs(deltaY)) show(current + (delta < 0 ? 1 : -1));
  touchStart = null;
  touchStartY = null;
}, { passive: true });

const hashIndex = Number(location.hash.slice(1)) - 1;
show(Number.isInteger(hashIndex) && hashIndex >= 0 ? hashIndex : 0);
