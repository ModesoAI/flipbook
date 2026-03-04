/**
 * Flipbook.js 2.0
 * A high-performance, zero-dependency 3D scroll-to-canvas renderer.
 */
export class Flipbook {
  constructor(config) {
    this.canvas = document.querySelector(config.canvas);
    this.ctx = this.canvas.getContext('2d', { alpha: false });
    this.frameCount = config.frameCount || 0;
    this.pathTemplate = config.pathTemplate || '';
    this.images = config.images || [];
    this.isLoaded = false;
    this.onProgress = config.onProgress || (() => {});
    this.onComplete = config.onComplete || (() => {});
    
    this.currentFrame = 0;
    this.targetFrame = 0;
    this.isAnimating = false;
    this.lerpAmount = config.lerp || 1.0; 

    this._handleScroll = this.handleScroll.bind(this);
    this._handleResize = this.handleResize.bind(this);
  }

  async init() {
    this.setupEventListeners();
    this.handleResize();
    
    // Fix: Only run preload if we have a template and no images
    if (this.images.length === 0 && this.pathTemplate) {
      await this.preloadImages();
    }
    
    this.isLoaded = true;
    this.onComplete();
    this.renderFrame(0);
  }

  setImages(newImages, newFrameCount) {
    this.images = newImages;
    this.frameCount = newFrameCount;
    this.renderFrame(Math.floor(this.currentFrame) % newFrameCount);
  }

  async preloadImages() {
    if (!this.pathTemplate) return []; // Robustness fix

    const promises = [];
    let loadedCount = 0;

    for (let i = 0; i < this.frameCount; i++) {
      const promise = new Promise((resolve) => {
        const img = new Image();
        const indexStr = String(i).padStart(4, '0');
        img.src = this.pathTemplate.replace('${index}', indexStr);
        img.onload = () => {
          loadedCount++;
          this.onProgress(Math.floor((loadedCount / this.frameCount) * 100));
          resolve(img);
        };
        img.onerror = () => {
          console.warn(`Flipbook: Failed to load ${img.src}`);
          resolve(null);
        };
        this.images[i] = img;
      });
      promises.push(promise);
    }

    return Promise.all(promises);
  }

  setupEventListeners() {
    window.addEventListener('scroll', this._handleScroll, { passive: true });
    window.addEventListener('resize', this._handleResize, { passive: true });
  }

  destroy() {
    window.removeEventListener('scroll', this._handleScroll);
    window.removeEventListener('resize', this._handleResize);
    this.images = [];
    this.isAnimating = false;
  }

  handleScroll() {
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    const maxScrollTop = document.documentElement.scrollHeight - window.innerHeight;
    const scrollFraction = scrollTop / maxScrollTop;
    
    this.targetFrame = Math.min(
      this.frameCount - 1,
      Math.floor(scrollFraction * this.frameCount)
    );

    if (this.lerpAmount >= 1.0) {
        this.currentFrame = this.targetFrame;
        requestAnimationFrame(() => this.renderFrame(this.currentFrame));
    } else if (!this.isAnimating) {
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
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    this.renderFrame(Math.floor(this.currentFrame));
  }

  renderFrame(index) {
    if (index < 0 || index >= this.images.length) return;
    const img = this.images[index];
    if (!img || !img.complete || img.naturalWidth === 0) return;

    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    const canvasAspect = this.canvas.width / this.canvas.height;
    const imgAspect = img.naturalWidth / img.naturalHeight;

    let drawWidth, drawHeight, offsetX, offsetY;

    if (canvasAspect > imgAspect) {
      drawWidth = this.canvas.width;
      drawHeight = this.canvas.width / imgAspect;
      offsetX = 0;
      offsetY = -(drawHeight - this.canvas.height) / 2;
    } else {
      drawWidth = this.canvas.height * imgAspect;
      drawHeight = this.canvas.height;
      offsetX = -(drawWidth - this.canvas.width) / 2;
      offsetY = 0;
    }

    this.ctx.drawImage(img, offsetX, offsetY, drawWidth, drawHeight);
  }
}
