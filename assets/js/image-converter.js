/**
 * Fast Image Converter Engine
 * 100% Client-Side In-Browser Processing (Zero Server Uploads)
 * Supports JPG, PNG, WebP, AVIF, HEIC, BMP, SVG, TIFF, ICO
 */

(function() {
  const MIME = {
    jpeg: 'image/jpeg',
    png: 'image/png',
    webp: 'image/webp',
    bmp: 'image/bmp',
    svg: 'image/svg+xml'
  };

  const EXT = {
    jpeg: 'jpg',
    png: 'png',
    webp: 'webp',
    bmp: 'bmp',
    svg: 'svg'
  };

  // Allow pages to preset default target format (e.g. 'jpeg' on png-to-jpeg.html)
  const defaultTarget = window.DEFAULT_TARGET_FORMAT || 'jpeg';
  const defaultQuality = 0.92;

  let currentGlobalFormat = defaultTarget;
  let currentGlobalQuality = defaultQuality;
  let webpSupport = null;
  let uid = 0;
  let convertTimer = null;

  const state = {
    files: [],
    activeId: null
  };

  // DOM Elements
  const dropzone = document.getElementById('imgDropzone');
  const fileInput = document.getElementById('imgFileInput');
  const compareWrap = document.getElementById('compareWrap');
  const compare = document.getElementById('compare');
  const imgOriginal = document.getElementById('imgOriginal');
  const imgAfter = document.getElementById('imgAfter');
  const afterWrap = document.getElementById('afterWrap');
  const divider = document.getElementById('divider');
  const handle = document.getElementById('handle');
  const tagLeft = document.getElementById('tagLeft');
  const tagRight = document.getElementById('tagRight');
  const thumbStrip = document.getElementById('imgThumbStrip');
  const settingsBody = document.getElementById('imgSettingsBody');
  const renameInput = document.getElementById('imgFileNameLabel');
  const addMoreBtn = document.getElementById('imgAddMoreBtn');
  const sortAscBtn = document.getElementById('imgSortAscBtn');
  const sortDescBtn = document.getElementById('imgSortDescBtn');
  const confirmModal = document.getElementById('imgConfirmModal');
  const confirmYesBtn = document.getElementById('imgConfirmYesBtn');
  const confirmNoBtn = document.getElementById('imgConfirmNoBtn');

  function activeFile() {
    return state.files.find(f => f.id === state.activeId) || null;
  }

  function fmtBytes(b) {
    if (b == null || isNaN(b)) return '—';
    if (b < 1024) return b + ' B';
    if (b < 1024 * 1024) return (b / 1024).toFixed(1) + ' KB';
    return (b / 1024 / 1024).toFixed(2) + ' MB';
  }

  function baseName(name) {
    const i = name.lastIndexOf('.');
    return i > 0 ? name.slice(0, i) : name;
  }

  function checkWebpSupport() {
    if (webpSupport !== null) return webpSupport;
    const c = document.createElement('canvas');
    c.width = 2; c.height = 2;
    webpSupport = c.toDataURL('image/webp').indexOf('data:image/webp') === 0;
    return webpSupport;
  }

  // File Handling
  function addFiles(list) {
    let firstNew = null;
    const promises = [];

    [...list].forEach(file => {
      if (!file.type.startsWith('image/') && !file.name.match(/\.(heic|heif|avif|bmp|tiff?|ico|svg)$/i)) {
        return;
      }

      const immediateUrl = URL.createObjectURL(file);
      const item = {
        id: 'f' + (++uid),
        file: file,
        name: file.name,
        size: file.size,
        targetFormat: currentGlobalFormat,
        quality: currentGlobalQuality,
        originalUrl: immediateUrl,
        resultBlob: null,
        resultUrl: null,
        resultSize: null,
        naturalW: null,
        naturalH: null,
        status: 'idle',
        error: ''
      };

      state.files.push(item);
      if (!firstNew) firstNew = item;
      promises.push(loadPreviewSource(item));
    });

    if (firstNew && !state.activeId) {
      state.activeId = firstNew.id;
    }

    renderThumbs();

    Promise.all(promises).then(() => {
      renderThumbs();
      renderSettings();
      const active = activeFile();
      if (active) renderCompare(active);
      scheduleConvert(0);
    });
  }

  async function loadPreviewSource(it) {
    try {
      // Check for HEIC/HEIF
      if (it.name.match(/\.(heic|heif)$/i) && typeof heic2any !== 'undefined') {
        try {
          const blob = await heic2any({ blob: it.file, toType: 'image/jpeg', quality: 0.85 });
          const singleBlob = Array.isArray(blob) ? blob[0] : blob;
          it.originalUrl = URL.createObjectURL(singleBlob);
          it.heicConvertedBlob = singleBlob;
        } catch (e) {
          console.warn('heic2any failed:', e);
        }
      }

      if (!it.originalUrl) it.originalUrl = URL.createObjectURL(it.file);

      try {
        const bmp = await createImageBitmap(it.file);
        it.naturalW = bmp.width;
        it.naturalH = bmp.height;
        if (bmp.close) bmp.close();
      } catch (e) {
        const img = new Image();
        await new Promise((res, rej) => {
          img.onload = res;
          img.onerror = rej;
          img.src = it.originalUrl;
        });
        it.naturalW = img.naturalWidth || 800;
        it.naturalH = img.naturalHeight || 800;
      }
    } catch (e) {
      console.warn('Preview fallback:', it.name, e);
    }
  }

  function selectFile(id) {
    state.activeId = id;
    renderThumbs();
    renderSettings();
    const active = activeFile();
    if (active) {
      renderCompare(active);
      if (active.status === 'done') {
        syncAfterImgWidth();
      } else {
        scheduleConvert(0);
      }
    }
  }

  function showConfirmModal(callback) {
    if (!confirmModal) {
      if (confirm('Remove image from batch?')) callback();
      return;
    }
    confirmModal.style.display = 'flex';
    confirmYesBtn.onclick = () => {
      confirmModal.style.display = 'none';
      callback();
    };
    confirmNoBtn.onclick = () => {
      confirmModal.style.display = 'none';
    };
  }

  function renderThumbs() {
    if (!thumbStrip) return;
    thumbStrip.innerHTML = '';

    if (state.files.length === 0) {
      if (dropzone) dropzone.style.display = 'flex';
      if (compareWrap) compareWrap.style.display = 'none';
      return;
    }

    if (dropzone) dropzone.style.display = 'none';
    if (compareWrap) compareWrap.style.display = 'block';

    state.files.forEach(it => {
      const wrap = document.createElement('div');
      wrap.className = 'thumb-wrap';

      const el = document.createElement('div');
      el.className = 'thumb' + (it.id === state.activeId ? ' active' : '');

      if (it.originalUrl) {
        const img = document.createElement('img');
        img.src = it.originalUrl;
        img.alt = it.name;
        el.appendChild(img);
      } else {
        el.innerHTML = '<span style="font-size:20px;">🖼️</span>';
      }

      if (it.status === 'done') {
        const badge = document.createElement('span');
        badge.className = 'thumb-badge';
        badge.textContent = '✓';
        el.appendChild(badge);
      }

      el.onclick = () => selectFile(it.id);

      const rm = document.createElement('div');
      rm.className = 'thumb-remove';
      rm.innerHTML = '&times;';
      rm.onclick = (e) => {
        e.stopPropagation();
        showConfirmModal(() => {
          if (it.originalUrl) URL.revokeObjectURL(it.originalUrl);
          if (it.resultUrl) URL.revokeObjectURL(it.resultUrl);
          state.files = state.files.filter(f => f.id !== it.id);
          state.activeId = state.files.length ? state.files[0].id : null;
          renderThumbs();
          renderSettings();
          const next = activeFile();
          if (next) renderCompare(next);
        });
      };

      wrap.appendChild(el);
      wrap.appendChild(rm);
      thumbStrip.appendChild(wrap);
    });

    // Add more button in thumb strip
    const addBtn = document.createElement('button');
    addBtn.className = 'thumb-add';
    addBtn.title = 'Add more images';
    addBtn.setAttribute('aria-label', 'Add more images');
    addBtn.innerHTML = '<svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>';
    addBtn.onclick = () => fileInput && fileInput.click();
    thumbStrip.appendChild(addBtn);
  }

  // Compare Slider Dragging
  let isDragging = false;
  function setDividerPct(pct) {
    pct = Math.max(0, Math.min(100, pct));
    if (divider) divider.style.left = pct + '%';
    if (handle) handle.style.left = pct + '%';
    if (afterWrap) afterWrap.style.clipPath = `polygon(${pct}% 0, 100% 0, 100% 100%, ${pct}% 100%)`;
  }

  function syncAfterImgWidth() {
    if (!compare || !imgAfter) return;
    imgAfter.style.width = compare.clientWidth + 'px';
    imgAfter.style.height = compare.clientHeight + 'px';
  }

  function updateDrag(e) {
    if (!isDragging || !compare) return;
    const rect = compare.getBoundingClientRect();
    const clientX = e.touches ? e.touches[0].clientX : e.clientX;
    const pct = ((clientX - rect.left) / rect.width) * 100;
    setDividerPct(pct);
  }

  if (handle) {
    handle.addEventListener('mousedown', () => { isDragging = true; });
    handle.addEventListener('touchstart', () => { isDragging = true; }, { passive: true });
  }
  window.addEventListener('mouseup', () => { isDragging = false; });
  window.addEventListener('touchend', () => { isDragging = false; });
  window.addEventListener('mousemove', updateDrag);
  window.addEventListener('touchmove', updateDrag, { passive: true });
  window.addEventListener('resize', syncAfterImgWidth);

  function renderCompare(it) {
    if (!it) return;
    if (imgOriginal) {
      imgOriginal.src = it.originalUrl || '';
      imgOriginal.onload = syncAfterImgWidth;
    }
    if (imgAfter) {
      imgAfter.src = it.resultUrl || it.originalUrl || '';
    }
    if (tagLeft) {
      tagLeft.textContent = 'Original · ' + fmtBytes(it.size);
    }
    if (tagRight) {
      tagRight.textContent = it.status === 'done' ? ('Converted · ' + fmtBytes(it.resultSize)) : 'Ready';
    }
    if (renameInput) {
      renameInput.value = baseName(it.name);
    }
    setDividerPct(50);
    syncAfterImgWidth();
  }

  // Settings Panel
  function renderSettings() {
    if (!settingsBody) return;
    const it = activeFile();
    if (!it) {
      settingsBody.innerHTML = '<div class="empty-settings">Choose or drop an image to see conversion settings.</div>';
      return;
    }

    const fmt = it.targetFormat;
    const isQualityAllowed = (fmt === 'jpeg' || fmt === 'webp');

    settingsBody.innerHTML = `
      <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 16px;">
        <h3 style="margin: 0;">Output Settings</h3>
        <span class="trust-badge" style="padding: 4px 10px; font-size: 11px; background: #eaf8ff;">⚡ 0s Wait</span>
      </div>

      <div class="size-preview-row">
        <div class="size-item">
          <span class="lbl">Original Size</span>
          <span class="val">${fmtBytes(it.size)}</span>
        </div>
        <div style="font-size: 16px; font-weight: 800;">→</div>
        <div class="size-item">
          <span class="lbl">Target Format</span>
          <span class="val" id="targetFmtLabel">${fmt.toUpperCase()}</span>
        </div>
        <div class="size-item">
          <span class="lbl">Converted Size</span>
          <span class="val" id="convertedSizeLabel" style="color: #008822;">${it.resultSize ? fmtBytes(it.resultSize) : 'Pending'}</span>
        </div>
      </div>

      <div class="field">
        <label for="formatSelect">Target Format</label>
        <select id="formatSelect" aria-label="Target Format">
          <option value="jpeg" ${fmt === 'jpeg' ? 'selected' : ''}>JPEG (.jpg)</option>
          <option value="png" ${fmt === 'png' ? 'selected' : ''}>PNG (.png)</option>
          <option value="webp" ${fmt === 'webp' ? 'selected' : ''}>WebP (.webp)</option>
          <option value="bmp" ${fmt === 'bmp' ? 'selected' : ''}>BMP (.bmp)</option>
          <option value="svg" ${fmt === 'svg' ? 'selected' : ''}>SVG (.svg)</option>
        </select>
      </div>

      ${isQualityAllowed ? `
        <div class="field">
          <div style="display: flex; justify-content: space-between; margin-bottom: 6px;">
            <label for="qualitySlider" style="margin: 0;">Quality: <span id="qualityVal">${Math.round(it.quality * 100)}%</span></label>
          </div>
          <input type="range" id="qualitySlider" min="0.1" max="1" step="0.05" value="${it.quality}" style="width: 100%; cursor: pointer;">
          <div style="display: flex; justify-content: space-between; font-size: 11px; font-weight: 700; color: var(--ink-dim); margin-top: 4px;">
            <span>Smaller File</span>
            <span>Balanced</span>
            <span>Highest Quality</span>
          </div>
        </div>
      ` : ''}

      <button class="btn-download" id="downloadBtn" ${it.status !== 'done' ? 'disabled' : ''}>
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 3v12m0 0-4-4m4 4 4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg>
        <span>Download ${EXT[it.targetFormat].toUpperCase()}</span>
      </button>

      <button class="btn-download-all" id="downloadAllBtn" style="${state.files.length > 1 ? 'display:block;' : 'display:none;'}">
        Download All as .ZIP (${state.files.length} files)
      </button>
    `;

    bindSettingsEvents(it);
  }

  function bindSettingsEvents(it) {
    const formatSelect = document.getElementById('formatSelect');
    if (formatSelect) {
      formatSelect.addEventListener('change', (e) => {
        const val = e.target.value;
        currentGlobalFormat = val;
        // Update all files in batch to target format
        state.files.forEach(f => {
          f.targetFormat = val;
          f.status = 'idle';
        });
        renderSettings();
        scheduleConvert(0);
      });
    }

    const qualitySlider = document.getElementById('qualitySlider');
    if (qualitySlider) {
      qualitySlider.addEventListener('input', (e) => {
        const q = parseFloat(e.target.value);
        currentGlobalQuality = q;
        it.quality = q;
        const qLabel = document.getElementById('qualityVal');
        if (qLabel) qLabel.textContent = Math.round(q * 100) + '%';
        scheduleConvert(200);
      });
    }

    const downloadBtn = document.getElementById('downloadBtn');
    if (downloadBtn) {
      downloadBtn.addEventListener('click', () => {
        if (!it.resultBlob) return;
        const ext = EXT[it.targetFormat] || 'jpg';
        const name = (renameInput && renameInput.value.trim()) ? renameInput.value.trim() : baseName(it.name);
        const filename = `${name}.${ext}`;
        const a = document.createElement('a');
        a.href = it.resultUrl;
        a.download = filename;
        document.body.appendChild(a);
        a.click();
        a.remove();
      });
    }

    const downloadAllBtn = document.getElementById('downloadAllBtn');
    if (downloadAllBtn) {
      downloadAllBtn.addEventListener('click', downloadAllZip);
    }
  }

  // BMP encoder
  function encodeBMP(canvas) {
    const ctx = canvas.getContext('2d');
    const w = canvas.width, h = canvas.height;
    const imgData = ctx.getImageData(0, 0, w, h);
    const data = imgData.data;
    const rowSize = Math.floor((24 * w + 31) / 32) * 4;
    const pixelArraySize = rowSize * h;
    const fileSize = 54 + pixelArraySize;
    const buffer = new ArrayBuffer(fileSize);
    const view = new DataView(buffer);

    // Bitmap File Header
    view.setUint16(0, 0x4D42, true); // "BM"
    view.setUint32(2, fileSize, true);
    view.setUint32(10, 54, true);

    // DIB Header (BITMAPINFOHEADER)
    view.setUint32(14, 40, true);
    view.setInt32(18, w, true);
    view.setInt32(22, h, true);
    view.setUint16(26, 1, true);
    view.setUint16(28, 24, true); // 24-bit RGB
    view.setUint32(34, pixelArraySize, true);

    let offset = 54;
    for (let y = h - 1; y >= 0; y--) {
      for (let x = 0; x < w; x++) {
        const i = (y * w + x) * 4;
        view.setUint8(offset++, data[i + 2]); // B
        view.setUint8(offset++, data[i + 1]); // G
        view.setUint8(offset++, data[i]);     // R
      }
      for (let p = 0; p < (rowSize - w * 3); p++) {
        view.setUint8(offset++, 0);
      }
    }
    return new Blob([buffer], { type: 'image/bmp' });
  }

  // SVG encoder (Vector encapsulation)
  function encodeSVG(canvas) {
    const pngDataUrl = canvas.toDataURL('image/png');
    const w = canvas.width, h = canvas.height;
    const svgStr = `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="${w}" height="${h}" viewBox="0 0 ${w} ${h}">
  <image width="${w}" height="${h}" xlink:href="${pngDataUrl}"/>
</svg>`;
    return new Blob([svgStr], { type: 'image/svg+xml' });
  }

  async function getImageSource(it) {
    if (it.heicConvertedBlob) {
      const img = new Image();
      const url = URL.createObjectURL(it.heicConvertedBlob);
      await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = url; });
      return img;
    }
    const img = new Image();
    await new Promise((res, rej) => { img.onload = res; img.onerror = rej; img.src = it.originalUrl; });
    return img;
  }

  async function convertSingle(it) {
    if (!it) return;
    it.status = 'working';

    try {
      const source = await getImageSource(it);
      const sw = source.naturalWidth || source.width || it.naturalW || 800;
      const sh = source.naturalHeight || source.height || it.naturalH || 800;

      const canvas = document.createElement('canvas');
      canvas.width = sw;
      canvas.height = sh;
      const ctx = canvas.getContext('2d');

      // Transparent PNG to JPEG: fill white background to avoid black background artifacts
      if (it.targetFormat === 'jpeg') {
        ctx.fillStyle = '#ffffff';
        ctx.fillRect(0, 0, sw, sh);
      }

      ctx.drawImage(source, 0, 0, sw, sh);

      let blob;
      if (it.targetFormat === 'bmp') {
        blob = encodeBMP(canvas);
      } else if (it.targetFormat === 'svg') {
        blob = encodeSVG(canvas);
      } else {
        if (it.targetFormat === 'webp' && !checkWebpSupport()) {
          throw new Error("This browser does not support WEBP encoding.");
        }
        const mime = MIME[it.targetFormat] || 'image/jpeg';
        const q = it.targetFormat === 'png' ? undefined : it.quality;
        blob = await new Promise((resolve, reject) => {
          canvas.toBlob(b => b ? resolve(b) : reject(new Error('Canvas conversion failed.')), mime, q);
        });
      }

      if (it.resultUrl) URL.revokeObjectURL(it.resultUrl);
      it.resultBlob = blob;
      it.resultUrl = URL.createObjectURL(blob);
      it.resultSize = blob.size;
      it.status = 'done';
      it.error = '';

      if (it.id === state.activeId) {
        if (tagRight) tagRight.textContent = 'Converted · ' + fmtBytes(it.resultSize);
        const convertedSizeLabel = document.getElementById('convertedSizeLabel');
        if (convertedSizeLabel) convertedSizeLabel.textContent = fmtBytes(it.resultSize);

        const dlBtn = document.getElementById('downloadBtn');
        if (dlBtn) {
          dlBtn.disabled = false;
          dlBtn.innerHTML = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 3v12m0 0-4-4m4 4 4-4"/><path d="M4 17v2a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2v-2"/></svg> <span>Download ${EXT[it.targetFormat].toUpperCase()}</span>`;
        }

        if (imgAfter) imgAfter.src = it.resultUrl;
      }
    } catch (err) {
      console.error(err);
      it.status = 'error';
      it.error = err.message || String(err);
      if (it.id === state.activeId && tagRight) {
        tagRight.textContent = 'Conversion Failed';
      }
    }
  }

  function scheduleConvert(delay) {
    clearTimeout(convertTimer);
    convertTimer = setTimeout(async () => {
      const active = activeFile();
      if (active) {
        await convertSingle(active);
        renderThumbs();
      }
      // Convert other files in batch sequentially in background
      for (const f of state.files) {
        if (f.id !== state.activeId && f.status !== 'done') {
          await convertSingle(f);
          renderThumbs();
        }
      }
    }, delay);
  }

  async function downloadAllZip() {
    if (typeof JSZip === 'undefined') {
      alert("ZIP library is loading, please try again in a moment.");
      return;
    }
    const dlAllBtn = document.getElementById('downloadAllBtn');
    const origText = dlAllBtn ? dlAllBtn.textContent : '';
    if (dlAllBtn) dlAllBtn.textContent = 'Creating ZIP...';

    const zip = new JSZip();
    for (const f of state.files) {
      if (!f.resultBlob) {
        await convertSingle(f);
      }
      const ext = EXT[f.targetFormat] || 'jpg';
      zip.file(`${baseName(f.name)}.${ext}`, f.resultBlob);
    }

    const content = await zip.generateAsync({ type: 'blob' });
    const url = URL.createObjectURL(content);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'converted-images.zip';
    document.body.appendChild(a);
    a.click();
    a.remove();
    if (dlAllBtn) dlAllBtn.textContent = origText;
    setTimeout(() => URL.revokeObjectURL(url), 4000);
  }

  // Event Listeners
  if (dropzone) {
    dropzone.onclick = () => fileInput && fileInput.click();
    dropzone.ondragover = (e) => { e.preventDefault(); dropzone.classList.add('drag'); };
    dropzone.ondragleave = () => dropzone.classList.remove('drag');
    dropzone.ondrop = (e) => {
      e.preventDefault();
      dropzone.classList.remove('drag');
      if (e.dataTransfer && e.dataTransfer.files) addFiles(e.dataTransfer.files);
    };
  }

  if (fileInput) {
    fileInput.onchange = (e) => {
      if (e.target.files) addFiles(e.target.files);
    };
  }

  // Clipboard Paste Support (Ctrl+V / Cmd+V)
  window.addEventListener('paste', (e) => {
    const items = (e.clipboardData || e.originalEvent.clipboardData).items;
    const files = [];
    for (const item of items) {
      if (item.kind === 'file' && item.type.startsWith('image/')) {
        files.push(item.getAsFile());
      }
    }
    if (files.length > 0) {
      addFiles(files);
    }
  });

  if (addMoreBtn) {
    addMoreBtn.onclick = () => fileInput && fileInput.click();
  }

  if (sortAscBtn) {
    sortAscBtn.onclick = () => {
      state.files.sort((a, b) => a.name.localeCompare(b.name));
      renderThumbs();
    };
  }

  if (sortDescBtn) {
    sortDescBtn.onclick = () => {
      state.files.sort((a, b) => b.name.localeCompare(a.name));
      renderThumbs();
    };
  }

  if (renameInput) {
    renameInput.addEventListener('input', (e) => {
      const active = activeFile();
      if (active) active.name = e.target.value.trim() + '.' + (EXT[active.targetFormat] || 'jpg');
    });
  }

  // Setup FAQ accordions
  document.querySelectorAll('.faq-question').forEach(q => {
    q.addEventListener('click', () => {
      const item = q.parentElement;
      const ans = item.querySelector('.faq-answer');
      if (ans) {
        ans.style.display = (ans.style.display === 'none' || !ans.style.display) ? 'block' : 'none';
      }
    });
  });

  // Dynamic Year
  const yearEl = document.getElementById('currentYear');
  if (yearEl) yearEl.textContent = new Date().getFullYear();

})();
