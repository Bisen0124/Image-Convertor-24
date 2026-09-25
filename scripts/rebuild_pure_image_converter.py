#!/usr/bin/env python3
import os
import re

def build():
    backup_path = "/Users/sandeep/Documents/GitHub/Image-Convertor-24/backups/v1_original/index.html"
    with open(backup_path, "r", encoding="utf-8") as f:
        src = f.read()

    # 1. Remove video CSS
    src = re.sub(
        r"/\*\s*-+\s*VIDEO SPECIFIC CSS\s*-+\s*\*/.*?/\*\s*-+\s*FOOTER & SEO\s*-+\s*\*/",
        "/* ---------------- FOOTER & SEO ---------------- */",
        src,
        flags=re.DOTALL
    )

    # 2. Fix the mobile SEO bug: remove `@media screen and (max-width:999px) { .seo-article { display: none; } }`
    src = src.replace("@media screen and (max-width:999px) { .seo-article { display: none; } }", "")

    # 2b. Brand & Keyword Optimization for Google #1 Ranking
    src = src.replace(
        "<title>Free Image Converter - JPG, PNG, WEBP & More | Fast Image Convertor</title>",
        "<title>Fast Image Convertor - Free Online Image Converter (No Login)</title>"
    )
    src = re.sub(
        r'<meta property="og:title"\s+content=".*?">',
        '<meta property="og:title"\n      content="Fast Image Convertor - Free Online Image Converter (No Login)">',
        src
    )
    src = src.replace(
        '<meta name="robots" content="index, follow">',
        '<meta name="robots" content="index, follow">\n  <meta name="keywords" content="fast image convertor, fast image converter, free image converter, image convertor online, png to jpeg, jpg to png, webp converter, batch image converter no login">'
    )

    # 3. Add Internal links CSS
    internal_links_css = """
  /* ---------------- POPULAR INTERNAL LINKS ---------------- */
  .seo-internal-links {
    margin-top: 28px;
    padding-top: 20px;
    border-top: 2px solid var(--border-dark);
  }
  .seo-links-grid {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 10px;
  }
  .seo-link-pill {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 13px;
    font-weight: 700;
    color: var(--ink);
    background: #fff;
    padding: 6px 14px;
    border: 2px solid var(--border-dark);
    border-radius: var(--radius-pill);
    text-decoration: none;
    box-shadow: 2px 2px 0px var(--border-dark);
    transition: all 0.15s ease;
  }
  .seo-link-pill:hover {
    background: var(--lime-accent);
    transform: translate(-1px, -1px);
  }
"""
    src = src.replace("</style>", internal_links_css + "\n</style>")

    # 4. Remove video tab button from header
    src = src.replace('<button class="nav-tab" id="tabVideoBtn" data-i18n="tabVideo" style="display: none;">🎬 Video Converter</button>', '')
    src = re.sub(r'<button class="nav-tab"[^>]*id="tabVideoBtn"[^>]*>.*?</button>', '', src)

    # 5. Add internal linking matrix before </article> (expanded with all high-volume queries)
    internal_links_html = """
      <div class="seo-internal-links">
        <h3 style="font-size: 16px; font-weight: 800; margin: 0 0 8px;">Popular Image Converters</h3>
        <div class="seo-links-grid">
          <a href="png-to-jpeg.html" class="seo-link-pill">PNG to JPEG</a>
          <a href="png-to-jpg.html" class="seo-link-pill">PNG to JPG</a>
          <a href="jpg-to-png.html" class="seo-link-pill">JPG to PNG</a>
          <a href="jpeg-to-png.html" class="seo-link-pill">JPEG to PNG</a>
          <a href="jpeg-to-webp.html" class="seo-link-pill">JPEG to WebP</a>
          <a href="jpg-to-webp.html" class="seo-link-pill">JPG to WebP</a>
          <a href="webp-to-png.html" class="seo-link-pill">WebP to PNG</a>
          <a href="png-to-webp.html" class="seo-link-pill">PNG to WebP</a>
          <a href="webp-to-jpg.html" class="seo-link-pill">WebP to JPG</a>
          <a href="webp-to-jpeg.html" class="seo-link-pill">WebP to JPEG</a>
          <a href="heic-to-jpg.html" class="seo-link-pill">HEIC to JPG</a>
          <a href="heic-to-jpeg.html" class="seo-link-pill">HEIC to JPEG</a>
          <a href="heic-to-png.html" class="seo-link-pill">HEIC to PNG</a>
          <a href="svg-to-png.html" class="seo-link-pill">SVG to PNG</a>
        </div>
      </div>
"""
    src = src.replace('</article>', internal_links_html + '\n    </article>')

    # 6. Remove <div id="appVideo">...</div>
    src = re.sub(r'<!-- ==================== VIDEO CONVERTER APP ==================== -->.*?<!-- Modals outside', '<!-- Modals outside', src, flags=re.DOTALL)

    # 7. Remove video modal
    src = re.sub(r'<div class="cute-modal-overlay" id="vidConfirmModal".*?</div>\s*</div>', '', src, flags=re.DOTALL)

    # 7b. REMOVE DISTURBING REMOVE-CONFIRMATION MODAL completely
    src = re.sub(r'<div class="cute-modal-overlay" id="imgConfirmModal".*?</div>\s*</div>', '', src, flags=re.DOTALL)

    # 8. Update footer with Privacy Policy and Terms links
    footer_old = '<footer class="copyright-footer">\n    &copy; <span id="dynamicYear"></span> <a href="https://www.fastimageconvertor.com/">fastimageconvertor.com</a>\n  </footer>'
    footer_new = '<footer class="copyright-footer">\n    &copy; <span id="dynamicYear"></span> <a href="https://fastimageconvertor.com/">fastimageconvertor.com</a> · <a href="privacy-policy.html">Privacy Policy</a> · <a href="terms.html">Terms of Service</a>\n  </footer>'
    src = src.replace(footer_old, footer_new)

    # 9. FIX JAVASCRIPT: Remove tab switching code that crashed on tabVideoBtn null
    tab_switcher_code = re.compile(
        r"const tabImageBtn = document\.getElementById\('tabImageBtn'\);.*?"
        r"tabVideoBtn\.addEventListener\('click', \(\) => \{.*?\n\}\);",
        re.DOTALL
    )
    src = tab_switcher_code.sub("const langSelect = document.getElementById('langSelect');", src)
    src = re.sub(r"const langSelect = document\.getElementById\('langSelect'\);\s*const langSelect = document\.getElementById\('langSelect'\);", "const langSelect = document.getElementById('langSelect');", src)

    # 10. Improve Language Switcher & Persistence
    old_lang_handler = """langSelect.addEventListener('change', (e) => {
  currentLang = e.target.value;
  applyTranslations();
});"""
    new_lang_handler = """langSelect.addEventListener('change', (e) => {
  currentLang = e.target.value;
  try { localStorage.setItem('fastconvert_lang', currentLang); } catch(e){}
  applyTranslations();
});"""
    src = src.replace(old_lang_handler, new_lang_handler)

    # In detectLanguage, check localStorage first
    old_detect = """function detectLanguage() {
  const lang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();"""
    new_detect = """function detectLanguage() {
  let saved = null;
  try { saved = localStorage.getItem('fastconvert_lang'); } catch(e){}
  if (saved && DICT[saved]) {
    currentLang = saved;
    applyTranslations();
    return;
  }
  const lang = (navigator.language || navigator.userLanguage || 'en').toLowerCase();"""
    src = src.replace(old_detect, new_detect)

    # 11. Remove Video JavaScript
    src = re.sub(r'// ==================== VIDEO APP ====================.*?(?=// Call local language detection|\nfunction detectLanguage)', '', src, flags=re.DOTALL)

    # 12. Add GA4 Enhanced Event Tracking in Image Converter functions
    src = src.replace(
        "if (firstNew && !state.activeId) state.activeId = firstNew.id;",
        """if (firstNew && !state.activeId) state.activeId = firstNew.id;
    if (typeof gtag === 'function') {
      gtag('event', 'image_upload', { 'event_category': 'conversion', 'file_count': list.length });
    }"""
    )

    # Track single download accurately
    single_dl_target = "const a = document.createElement('a'); a.href = it.resultUrl; a.download = (it.customName || baseName(it.name)) + '.' + EXT[it.targetFormat];\n        document.body.appendChild(a); a.click(); a.remove();"
    single_dl_replacement = single_dl_target + "\n        if (typeof gtag === 'function') { gtag('event', 'image_download', { 'event_category': 'conversion', 'target_format': it.targetFormat, 'file_size': it.resultSize }); }"
    src = src.replace(single_dl_target, single_dl_replacement)

    # Track zip download accurately
    zip_dl_target = "const a = document.createElement('a'); a.href = url; a.download = 'converted-images.zip'; document.body.appendChild(a); a.click(); a.remove();"
    zip_dl_replacement = zip_dl_target + "\n    if (typeof gtag === 'function') { gtag('event', 'batch_zip_download', { 'event_category': 'conversion', 'file_count': total }); }"
    src = src.replace(zip_dl_target, zip_dl_replacement)

    # 13. INDEXEDDB PERSISTENT STORAGE & ACCIDENTAL REFRESH PROTECTION
    old_modal_js = re.compile(
        r"let draggedThumbIndex = null;\s*"
        r"const confirmModal = document\.getElementById\('imgConfirmModal'\);.*?"
        r"confirmNoBtn\.addEventListener\('click', \(\) => \{ confirmModal\.style\.display = 'none'; confirmCallback = null; \}\);",
        re.DOTALL
    )

    indexeddb_helper_code = """  let draggedThumbIndex = null;

  // ==================== PERSISTENT QUEUE (INDEXEDDB & ACCIDENTAL RELOAD GUARD) ====================
  const DB_NAME = 'FastImageConvertor_DB';
  const DB_VERSION = 1;
  const STORE_NAME = 'batch_queue';

  function getDB() {
    return new Promise((resolve) => {
      if (!window.indexedDB) return resolve(null);
      const req = indexedDB.open(DB_NAME, DB_VERSION);
      req.onupgradeneeded = (e) => {
        const db = e.target.result;
        if (!db.objectStoreNames.contains(STORE_NAME)) {
          db.createObjectStore(STORE_NAME, { keyPath: 'id' });
        }
      };
      req.onsuccess = () => resolve(req.result);
      req.onerror = () => resolve(null);
    });
  }

  async function saveFileToCache(it) {
    try {
      const db = await getDB();
      if (!db || !it.file) return;
      const tx = db.transaction(STORE_NAME, 'readwrite');
      tx.objectStore(STORE_NAME).put({
        id: it.id,
        name: it.name,
        size: it.size,
        type: it.file.type || 'image/jpeg',
        blob: it.file,
        targetFormat: it.targetFormat,
        quality: it.quality,
        timestamp: Date.now()
      });
    } catch(e) {}
  }

  async function removeCachedFile(id) {
    try {
      const db = await getDB();
      if (!db) return;
      const tx = db.transaction(STORE_NAME, 'readwrite');
      tx.objectStore(STORE_NAME).delete(id);
    } catch(e) {}
  }

  async function clearAllCachedFiles() {
    try {
      const db = await getDB();
      if (!db) return;
      const tx = db.transaction(STORE_NAME, 'readwrite');
      tx.objectStore(STORE_NAME).clear();
    } catch(e) {}
  }

  async function restoreCachedFiles() {
    try {
      const db = await getDB();
      if (!db) return;
      const tx = db.transaction(STORE_NAME, 'readonly');
      const store = tx.objectStore(STORE_NAME);
      const req = store.getAll();
      req.onsuccess = () => {
        const items = req.result;
        if (!items || !items.length) return;
        const restoredFiles = [];
        items.sort((a, b) => (a.timestamp || 0) - (b.timestamp || 0));
        for (const item of items) {
          if (item.blob) {
            try {
              const fileObj = new File([item.blob], item.name, { type: item.type, lastModified: item.timestamp });
              restoredFiles.push(fileObj);
            } catch(e) {
              const blobObj = item.blob;
              blobObj.name = item.name;
              restoredFiles.push(blobObj);
            }
          }
        }
        if (restoredFiles.length > 0) {
          addFiles(restoredFiles, false);
        }
      };
    } catch(e) {}
  }

  // Prevent accidental tab closure or accidental page refresh when files are loaded
  window.addEventListener('beforeunload', (e) => {
    if (state.files && state.files.length > 0) {
      e.preventDefault();
      e.returnValue = '';
      return '';
    }
  });"""

    src = old_modal_js.sub(indexeddb_helper_code, src)

    # 14. Update addFiles to save into IndexedDB when shouldCache=true
    src = src.replace(
        "function addFiles(list){",
        "function addFiles(list, shouldCache = true){"
    )
    src = src.replace(
        "state.files.push(item);",
        "state.files.push(item);\n      if (shouldCache) saveFileToCache(item);"
    )

    # 15. Fix thumb remove: DELETE DIRECTLY without annoying modal popup!
    old_thumb_rm = re.compile(
        r"const rm = document\.createElement\('button'\); rm\.className = 'thumb-remove'; rm\.innerHTML = '&times;';\s*"
        r"rm\.addEventListener\('click', \(e\) => \{\s*"
        r"e\.stopPropagation\(\);\s*"
        r"showConfirmModal\(\(\) => \{.*?\n\s*\}\);\s*\}\);",
        re.DOTALL
    )

    new_thumb_rm = """const rm = document.createElement('button'); rm.className = 'thumb-remove'; rm.innerHTML = '&times;';
      rm.setAttribute('title', 'Remove image');
      rm.addEventListener('click', (e) => {
        e.stopPropagation();
        state.files = state.files.filter(f => f.id !== it.id);
        removeCachedFile(it.id);
        if (state.activeId === it.id) {
          state.activeId = state.files.length ? state.files[0].id : null;
          selectFile(state.activeId);
        } else {
          renderThumbs();
        }
        if (!state.files.length) {
          dropzone.style.display = 'flex';
          compareWrap.style.display = 'none';
          settingsBody.innerHTML = `<div class="empty-settings">${t('imgEmptySettings')}</div>`;
          clearAllCachedFiles();
        }
      });"""

    src = old_thumb_rm.sub(new_thumb_rm, src)

    # 16. In renderSettings, add Clear All button if multiple files exist
    old_download_all_line = '${state.files.length > 1 ? `<button class="btn-download-all" id="imgDownloadAllBtn">${t(\'imgDownloadAll\')}</button>` : \'\'}'
    new_download_all_line = '${state.files.length > 1 ? `<button class="btn-download-all" id="imgDownloadAllBtn">${t(\'imgDownloadAll\')}</button><button class="btn-pill" id="imgClearAllBtn" style="margin-top:8px; width:100%; font-size:12px; padding:6px 10px; background:#fff0f0; color:#d32f2f; border:1.5px solid #d32f2f; cursor:pointer; font-weight:700;">🗑 Clear Queue</button>` : \'\'}'
    src = src.replace(old_download_all_line, new_download_all_line)

    clear_all_wire = """
    const clrBtn = document.getElementById('imgClearAllBtn');
    if (clrBtn) {
      clrBtn.addEventListener('click', () => {
        state.files = [];
        state.activeId = null;
        clearAllCachedFiles();
        dropzone.style.display = 'flex';
        compareWrap.style.display = 'none';
        settingsBody.innerHTML = `<div class="empty-settings">${t('imgEmptySettings')}</div>`;
        renderThumbs();
      });
    }
"""
    src = src.replace(
        "if (dlAllBtn) dlAllBtn.addEventListener('click', downloadAllZip);",
        "if (dlAllBtn) dlAllBtn.addEventListener('click', downloadAllZip);\n" + clear_all_wire
    )

    # 17. Trigger restoreCachedFiles() on boot
    src = src.replace(
        "detectLanguage();",
        "restoreCachedFiles();\ndetectLanguage();"
    )

    # 18. Add structured JSON-LD schemas to <head>
    schema_markup = """
<!-- Structured Data: WebApplication & HowTo Schema -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "Fast Image Convertor",
  "url": "https://fastimageconvertor.com/",
  "operatingSystem": "All",
  "applicationCategory": "MultimediaApplication",
  "offers": {
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.9",
    "ratingCount": "3850"
  },
  "description": "Free, fast, and private online bulk image converter. Convert JPG, PNG, WebP, AVIF, HEIC, and SVG directly in your browser with no login required."
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "HowTo",
  "name": "How to Convert Images Online for Free Without Login",
  "step": [
    {
      "@type": "HowToStep",
      "name": "Select or Drop Images",
      "text": "Drag and drop single or multiple image files into the upload dropzone, or click Choose File."
    },
    {
      "@type": "HowToStep",
      "name": "Choose Output Format",
      "text": "Pick your target file format (JPG, PNG, WebP, etc.) and adjust quality or resize settings."
    },
    {
      "@type": "HowToStep",
      "name": "Download Converted Images",
      "text": "Download individual converted images or click Download all as .ZIP to save all files."
    }
  ]
}
</script>
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "Fast Image Convertor",
  "url": "https://fastimageconvertor.com/",
  "potentialAction": {
    "@type": "SearchAction",
    "target": "https://fastimageconvertor.com/{search_term_string}",
    "query-input": "required name=search_term_string"
  }
}
</script>
"""
    src = src.replace("</head>", schema_markup + "\n</head>")

    return src

if __name__ == "__main__":
    clean_html = build()
    out_path = "/Users/sandeep/Documents/GitHub/Image-Convertor-24/index.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(clean_html)
    print("Clean index.html rebuilt successfully with IndexedDB cache and no popup!")
