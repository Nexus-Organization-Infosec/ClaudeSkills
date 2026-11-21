/* PixelRelief: ein Foto als feines Pixel-Relief (WebGL), das beim Laden aus der Tiefe zusammenfliegt,
   sich zur Maus neigt und Pixel in der Nähe des Mauszeigers anhebt.

   Verwendung (Reihenfolge der Skripte): zuerst die Quelle aus foto_zu_pixel.py (setzt window.PIXEL_QUELLE),
   dann diese Datei, dann
     PixelRelief.mount(document.querySelector('.hero'), { source: window.PIXEL_QUELLE });
   Das Element (.hero) braucht position:relative; Text darüber z-index 1 oder höher.

   Die Quelle sollte eine Daten-URL sein (foto_zu_pixel.py): Bilder aus Dateien dürfen im Canvas nicht ausgelesen
   werden, wenn die Seite per Doppelklick (file://) geöffnet wird. Ohne WebGL bleibt das Element unverändert und
   bekommt die Klasse "pixel-relief-fallback"; ein darunterliegendes Foto bleibt dann sichtbar. */
(function () {
  const DEFAULTS = {
    source: null,            // Daten-URL oder Bild-URL derselben Herkunft
    background: '#212326',   // Hintergrund zwischen den Pixeln, passend zur Seite wählen
    size: 0.86,              // Pixelgröße im Raster (1 = lückenlos)
    depth: 0.045,            // Relieftiefe relativ zur Breite; helle Pixel stehen vor
    tiltX: 0.42,             // maximale Neigung zur Maus, horizontal (Radiant, gesamt)
    tiltY: 0.24,             // maximale Neigung zur Maus, vertikal
    lift: 1.5,               // Anheben der Pixel am Mauszeiger (Vielfaches von depth), 0 = aus
    liftRadius: 0.2,         // Radius des Anhebens relativ zur Höhe
    drift: 0.05,             // leichtes Schwenken ohne Maus (Radiant), 0 = aus
    intro: 2200,             // Dauer des Zusammenfliegens in ms, 0 = aus
    startAfter: null,        // Promise: Intro erst danach starten (z. B. nach einem Ladebildschirm)
    fit: 'cover',            // 'cover' füllt die Fläche, 'contain' zeigt das ganze Bild
    portraitZoom: 1.9,       // Hochformat: Bildbreite × Faktor (nur bei fit 'cover')
    brightness: 1.12,        // gleicht die Lücken zwischen den Pixeln aus
    minLuminance: 0.03,      // fast schwarze Pixel weglassen
    maxDpr: 2,
  };

  const VERTEX = `
    attribute vec2 a_grid; attribute vec3 a_color; attribute vec2 a_extra;
    uniform vec2 u_view; uniform vec2 u_offset; uniform float u_cell; uniform vec2 u_rot; uniform vec2 u_mouse;
    uniform float u_hover; uniform float u_intro; uniform float u_depth; uniform float u_size; uniform float u_lift; uniform float u_radius;
    varying vec3 v_color; varying float v_mix;
    void main() {
      vec2 base = u_offset + (a_grid + 0.5) * u_cell;
      vec2 c = u_view * 0.5;
      vec3 p = vec3(base - c, a_extra.x * u_depth);
      vec2 dm = base - u_mouse;
      float r = u_view.y * u_radius;
      p.z += u_depth * u_lift * u_hover * exp(-dot(dm, dm) / (r * r));
      float t = clamp((u_intro - a_extra.y * 0.45) / 0.55, 0.0, 1.0);
      t = 1.0 - pow(1.0 - t, 3.0);
      p.z -= (1.0 - t) * (0.35 + a_extra.y) * u_view.x;
      float cy = cos(u_rot.y), sy = sin(u_rot.y);
      p = vec3(p.x * cy + p.z * sy, p.y, -p.x * sy + p.z * cy);
      float cx = cos(u_rot.x), sx = sin(u_rot.x);
      p = vec3(p.x, p.y * cx - p.z * sx, p.y * sx + p.z * cx);
      float focal = u_view.x * 1.2;
      float s = focal / max(focal - p.z, 1.0);
      vec2 clip = (c + p.xy * s) / u_view * 2.0 - 1.0;
      gl_Position = vec4(clip.x, -clip.y, clamp(-p.z / (focal * 2.0), -1.0, 1.0), 1.0);
      gl_PointSize = max(1.0, u_cell * s * u_size);
      v_color = a_color;
      v_mix = t;
    }`;
  const FRAGMENT = `
    precision mediump float;
    uniform vec3 u_bg; uniform float u_bright; varying vec3 v_color; varying float v_mix;
    void main() { gl_FragColor = vec4(mix(u_bg, min(v_color * u_bright, 1.0), v_mix), 1.0); }`;

  const hexToRgb = hex => {
    const v = parseInt(hex.replace('#', ''), 16);
    return [(v >> 16 & 255) / 255, (v >> 8 & 255) / 255, (v & 255) / 255];
  };

  function mount(container, userOptions) {
    const o = Object.assign({}, DEFAULTS, userOptions || {});
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const canvas = document.createElement('canvas');
    canvas.className = 'pixel-relief';
    canvas.setAttribute('aria-hidden', 'true');
    Object.assign(canvas.style, { position: 'absolute', inset: '0', width: '100%', height: '100%', display: 'block', pointerEvents: 'none', zIndex: '0' });
    const gl = o.source && canvas.getContext('webgl', { antialias: false, alpha: false });
    if (!gl) {
      container.classList.add('pixel-relief-fallback');
      return { destroy() {} };
    }
    container.insertBefore(canvas, container.firstChild);
    container.classList.add('pixel-relief-active');

    const compile = (type, code) => {
      const shader = gl.createShader(type);
      gl.shaderSource(shader, code);
      gl.compileShader(shader);
      if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(shader));
      return shader;
    };
    const program = gl.createProgram();
    gl.attachShader(program, compile(gl.VERTEX_SHADER, VERTEX));
    gl.attachShader(program, compile(gl.FRAGMENT_SHADER, FRAGMENT));
    gl.linkProgram(program);
    gl.useProgram(program);
    const uni = {};
    ['u_view', 'u_offset', 'u_cell', 'u_rot', 'u_mouse', 'u_hover', 'u_intro', 'u_depth', 'u_size', 'u_bg', 'u_bright', 'u_lift', 'u_radius']
      .forEach(n => { uni[n] = gl.getUniformLocation(program, n); });
    const bg = hexToRgb(o.background);
    gl.uniform3f(uni.u_bg, bg[0], bg[1], bg[2]);
    gl.uniform1f(uni.u_bright, o.brightness);
    gl.uniform1f(uni.u_lift, o.lift);
    gl.uniform1f(uni.u_radius, o.liftRadius);
    gl.uniform1f(uni.u_size, o.size);
    gl.enable(gl.DEPTH_TEST);
    gl.depthFunc(gl.LEQUAL);
    gl.clearColor(bg[0], bg[1], bg[2], 1);

    let cols = 0, rows = 0, count = 0, width = 0, height = 0, dpr = 1;
    let visible = true, running = false, destroyed = false, introStart = null;
    let pointer = { x: 0.5, y: 0.5, inside: false };
    let mouse = { x: -1e5, y: -1e5 };
    let hover = 0, rotX = 0, rotY = 0;

    const image = new Image();
    image.src = o.source;

    const upload = () => {
      cols = image.naturalWidth;
      rows = image.naturalHeight;
      const off = document.createElement('canvas');
      off.width = cols;
      off.height = rows;
      const ctx = off.getContext('2d', { willReadFrequently: true });
      ctx.drawImage(image, 0, 0);
      const px = ctx.getImageData(0, 0, cols, rows).data;
      const data = [];
      for (let y = 0; y < rows; y++) {
        for (let x = 0; x < cols; x++) {
          const i = (y * cols + x) * 4;
          const r = px[i] / 255, g = px[i + 1] / 255, b = px[i + 2] / 255;
          const lum = 0.2126 * r + 0.7152 * g + 0.0722 * b;
          if (lum < o.minLuminance || px[i + 3] < 128) continue;
          data.push(x, y, r, g, b, lum, Math.random());
        }
      }
      count = data.length / 7;
      gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
      gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
      [['a_grid', 2, 0], ['a_color', 3, 8], ['a_extra', 2, 20]].forEach(([name, size, offset]) => {
        const loc = gl.getAttribLocation(program, name);
        gl.enableVertexAttribArray(loc);
        gl.vertexAttribPointer(loc, size, gl.FLOAT, false, 28, offset);
      });
    };

    const resize = () => {
      dpr = Math.min(o.maxDpr, devicePixelRatio || 1);
      width = container.clientWidth;
      height = container.clientHeight;
      canvas.width = Math.round(width * dpr);
      canvas.height = Math.round(height * dpr);
      gl.viewport(0, 0, canvas.width, canvas.height);
    };

    const cellSize = () => {
      if (o.fit === 'contain') return Math.min(width / cols, height / rows);
      if (width < height) return (width / cols) * o.portraitZoom;
      return Math.max(width / cols, height / rows) * 1.06;
    };

    const frame = now => {
      if (destroyed || !visible) { running = false; return; }
      const drift = reduced ? 0 : Math.sin(now / 3800) * o.drift;
      rotY += ((pointer.x - 0.5) * o.tiltX + drift - rotY) * 0.06;
      rotX += ((pointer.y - 0.5) * -o.tiltY - rotX) * 0.06;
      hover += ((pointer.inside ? 1 : 0) - hover) * 0.08;
      let intro = 1;
      if (!reduced && o.intro > 0) intro = introStart === null ? 0 : Math.min(1, (now - introStart) / o.intro);
      const cell = cellSize();
      gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);
      gl.uniform2f(uni.u_view, canvas.width, canvas.height);
      gl.uniform2f(uni.u_offset, (width - cols * cell) / 2 * dpr, (height - rows * cell) / 2 * dpr);
      gl.uniform1f(uni.u_cell, cell * dpr);
      gl.uniform2f(uni.u_rot, rotX, rotY);
      gl.uniform2f(uni.u_mouse, mouse.x * dpr, mouse.y * dpr);
      gl.uniform1f(uni.u_hover, hover);
      gl.uniform1f(uni.u_intro, intro);
      gl.uniform1f(uni.u_depth, width * o.depth * dpr);
      gl.drawArrays(gl.POINTS, 0, count);
      requestAnimationFrame(frame);
    };
    const run = () => {
      if (running || !count || destroyed) return;
      running = true;
      requestAnimationFrame(frame);
    };

    const onMove = event => {
      const rect = container.getBoundingClientRect();
      pointer = { x: (event.clientX - rect.left) / rect.width, y: (event.clientY - rect.top) / rect.height, inside: true };
      mouse = { x: event.clientX - rect.left, y: event.clientY - rect.top };
    };
    const onLeave = () => { pointer = { x: 0.5, y: 0.5, inside: false }; };
    container.addEventListener('pointermove', onMove);
    container.addEventListener('pointerleave', onLeave);
    addEventListener('resize', resize);
    const observer = new IntersectionObserver(([entry]) => { visible = entry.isIntersecting; if (visible) run(); });
    observer.observe(container);

    const ready = image.complete && image.naturalWidth ? Promise.resolve() : new Promise((resolve, reject) => {
      image.addEventListener('load', resolve, { once: true });
      image.addEventListener('error', reject, { once: true });
    });
    ready.then(() => { upload(); resize(); run(); }).catch(() => {
      canvas.remove();
      container.classList.remove('pixel-relief-active');
      container.classList.add('pixel-relief-fallback');
    });
    Promise.resolve(o.startAfter).then(() => { introStart = performance.now(); });

    return {
      destroy() {
        destroyed = true;
        observer.disconnect();
        container.removeEventListener('pointermove', onMove);
        container.removeEventListener('pointerleave', onLeave);
        removeEventListener('resize', resize);
        canvas.remove();
      },
    };
  }

  window.PixelRelief = { mount, defaults: DEFAULTS };
})();
