/**
 * Flipbook.js 2.3 - High-DPI & CSS-Native Cover
 */
export class Flipbook {
  constructor(config) {
    this.canvas = document.querySelector(config.canvas);
    this.ctx = this.canvas.getContext('2d', { alpha: false });
    this.frameCount = config.frameCount || 0;
    this.pathTemplate = config.pathTemplate || '';
    this.images = [];
    this.onProgress = config.onProgress || (() => {});
    this.onComplete = config.onComplete || (() => {});
    
    this.currentFrame = 0;
    this.targetFrame = 0;
    this.isAnimating = false;
    this.lerpAmount = config.lerp || 0.1; 

    this._handleScroll = this.handleScroll.bind(this);
    this._handleResize = this.handleResize.bind(this);
  }

  async init() {
    this.handleResize();
    if (this.pathTemplate && this.images.length === 0) {
        await this.preloadImages();
    }
    
    this.renderFrame(0);
    window.addEventListener('scroll', this._handleScroll, { passive: true });
    window.addEventListener('resize', this._handleResize, { passive: true });
    this.onComplete();
  }

  setImages(newImages, newFrameCount) {
    this.images = newImages;
    this.frameCount = newFrameCount;
    this.renderFrame(Math.floor(this.currentFrame) % newFrameCount);
  }

  async preloadImages() {
    const promises = [];
    for (let i = 0; i < this.frameCount; i++) {
      const promise = new Promise((resolve) => {
        const img = new Image();
        const indexStr = String(i).padStart(4, '0');
        img.src = this.pathTemplate.replace('${index}', indexStr);
        img.onload = () => {
          const loaded = this.images.filter(x => x && x.complete).length;
          this.onProgress(Math.floor((loaded / this.frameCount) * 100));
          resolve(img);
        };
        img.onerror = () => resolve(null);
        this.images[i] = img;
      });
      promises.push(promise);
    }
    return Promise.all(promises);
  }

  handleScroll() {
    const y = window.scrollY || document.documentElement.scrollTop;
    const h = window.innerHeight;
    const docH = document.documentElement.scrollHeight;
    const maxScroll = docH - h;
    
    const progress = Math.max(0, Math.min(1, y / maxScroll));
    this.targetFrame = Math.floor(progress * (this.frameCount - 1));

    if (!this.isAnimating) {
        this.startAnimationLoop();
    }
  }

  startAnimationLoop() {
    if (this.isAnimating) return;
    this.isAnimating = true;
    const loop = () => {
        if (!this.isAnimating) return;
        const diff = this.targetFrame - this.currentFrame;
        if (Math.abs(diff) < 0.05) {
            this.currentFrame = this.targetFrame;
            this.isAnimating = false;
        } else {
            this.currentFrame += diff * this.lerpAmount;
            requestAnimationFrame(loop);
        }
        this.renderFrame(Math.floor(this.currentFrame));
    };
    requestAnimationFrame(loop);
  }

  handleResize() {
    const img = this.images[0];
    this.canvas.width = img ? img.naturalWidth : 1920;
    this.canvas.height = img ? img.naturalHeight : 1080;
    this.renderFrame(Math.floor(this.currentFrame));
  }

  renderFrame(index) {
    const img = this.images[index];
    if (!img || !img.complete) return;
    this.ctx.drawImage(img, 0, 0, this.canvas.width, this.canvas.height);
  }

  destroy() {
    window.removeEventListener('scroll', this._handleScroll);
    window.removeEventListener('resize', this._handleResize);
    this.isAnimating = false;
  }
}
