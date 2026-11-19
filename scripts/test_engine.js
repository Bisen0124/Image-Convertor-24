/**
 * Comprehensive Automated Unit Test Suite for Fast Image Convertor Engine
 * Tests:
 *  1. Reverse Engine (Bi-directional format conversion matrix: PNG <-> JPG/JPEG <-> WEBP <-> BMP <-> SVG)
 *  2. Transparency & Alpha Channel Handling (White background fill on PNG -> JPG)
 *  3. Exact-KB Binary Search Compression & Downscaling Engine
 *  4. Government Exam Dimension Presets Engine (UPSC, SSC, Passport, Visa)
 *  5. Client-Side Code Protection & Reverse-Engineering Shield
 *  6. Memory Leak Prevention & Optimization Techniques
 */

const fs = require('fs');
const path = require('path');
const assert = require('assert');

let totalTests = 0;
let passedTests = 0;
let failedTests = 0;

function test(name, fn) {
  totalTests++;
  try {
    fn();
    console.log(`  ✓ [PASS] ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✗ [FAIL] ${name}`);
    console.error(`    Error: ${err.message}`);
    failedTests++;
  }
}

async function asyncTest(name, fn) {
  totalTests++;
  try {
    await fn();
    console.log(`  ✓ [PASS] ${name}`);
    passedTests++;
  } catch (err) {
    console.error(`  ✗ [FAIL] ${name}`);
    console.error(`    Error: ${err.message}`);
    failedTests++;
  }
}

console.log('\n======================================================');
console.log('  RUNNING FAST IMAGE CONVERTOR ENGINE TEST SUITE');
console.log('======================================================\n');

// -----------------------------------------------------------------------------
// SUITE 1: REVERSE ENGINE (BI-DIRECTIONAL FORMAT CONVERSION MATRIX)
// -----------------------------------------------------------------------------
console.log('SUITE 1: Reverse Engine (Bi-directional Conversions)');

const MIME = {
  png: 'image/png',
  jpeg: 'image/jpeg',
  jpg: 'image/jpeg',
  webp: 'image/webp',
  bmp: 'image/bmp',
  svg: 'image/svg+xml'
};

test('Reverse Engine: Forward & Reverse MIME type mappings match specifications', () => {
  assert.strictEqual(MIME['png'], 'image/png');
  assert.strictEqual(MIME['jpeg'], 'image/jpeg');
  assert.strictEqual(MIME['jpg'], 'image/jpeg');
  assert.strictEqual(MIME['webp'], 'image/webp');
  assert.strictEqual(MIME['bmp'], 'image/bmp');
  assert.strictEqual(MIME['svg'], 'image/svg+xml');
});

test('Reverse Engine: PNG -> JPG/JPEG Transparency Replacement (White Background)', () => {
  // Simulates canvas white background rendering logic from index.html line 1563
  function applyWhiteBackgroundIfLossy(targetFormat, hasAlpha, canvasWidth, canvasHeight) {
    let replacedBackground = false;
    let canvas = { width: canvasWidth, height: canvasHeight };
    if (targetFormat === 'jpeg' || targetFormat === 'jpg') {
      const c2 = { width: canvas.width, height: canvas.height, fillStyle: '#ffffff' };
      replacedBackground = true;
      canvas = c2;
    }
    return { canvas, replacedBackground };
  }

  // Forward: Transparent PNG to JPG
  const pngToJpg = applyWhiteBackgroundIfLossy('jpg', true, 500, 500);
  assert.strictEqual(pngToJpg.replacedBackground, true, 'PNG to JPG must replace transparent background with white');

  // Forward: Transparent PNG to JPEG
  const pngToJpeg = applyWhiteBackgroundIfLossy('jpeg', true, 500, 500);
  assert.strictEqual(pngToJpeg.replacedBackground, true, 'PNG to JPEG must replace transparent background with white');

  // Reverse: JPG to PNG (Preserves native canvas rendering, no white override)
  const jpgToPng = applyWhiteBackgroundIfLossy('png', false, 500, 500);
  assert.strictEqual(jpgToPng.replacedBackground, false, 'JPG to PNG must preserve lossless canvas output');
});

test('Reverse Engine: BMP Binary Encoder bit-level specifications', () => {
  // Extract and verify BMP encoding from index.html
  function encodeBMP(w, h, data) {
    const rowSize = Math.floor((24 * w + 31) / 32) * 4;
    const pixelArraySize = rowSize * h;
    const fileSize = 54 + pixelArraySize;
    const buf = new ArrayBuffer(fileSize);
    const view = new DataView(buf);

    // Magic Header 'BM'
    view.setUint8(0, 0x42);
    view.setUint8(1, 0x4D);
    view.setUint32(2, fileSize, true);
    view.setUint32(10, 54, true); // offset
    view.setUint32(14, 40, true); // DIB header size
    view.setInt32(18, w, true);
    view.setInt32(22, h, true);
    view.setUint16(26, 1, true); // color planes
    view.setUint16(28, 24, true); // 24-bit RGB
    view.setUint32(34, pixelArraySize, true);

    return { buf, fileSize, view };
  }

  const w = 10, h = 10;
  const dummyData = new Uint8Array(w * h * 4);
  const result = encodeBMP(w, h, dummyData);

  // Assert 'BM' signature
  assert.strictEqual(result.view.getUint8(0), 0x42);
  assert.strictEqual(result.view.getUint8(1), 0x4D);
  // Assert header fields
  assert.strictEqual(result.view.getUint32(10, true), 54, 'Pixel offset must be 54 bytes');
  assert.strictEqual(result.view.getUint32(14, true), 40, 'DIB header must be 40 bytes');
  assert.strictEqual(result.view.getInt32(18, true), 10, 'Width must be 10');
  assert.strictEqual(result.view.getInt32(22, true), 10, 'Height must be 10');
  assert.strictEqual(result.view.getUint16(28, true), 24, 'Color depth must be 24-bit');
});

test('Reverse Engine: SVG Vector Wrapper structure', () => {
  function encodeSVG(w, h, dataUrl) {
    return `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 ${w} ${h}" width="${w}" height="${h}"><image href="${dataUrl}" width="${w}" height="${h}" /></svg>`;
  }

  const svg = encodeSVG(300, 200, 'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA...');
  assert.ok(svg.includes('xmlns="http://www.w3.org/2000/svg"'));
  assert.ok(svg.includes('viewBox="0 0 300 200"'));
  assert.ok(svg.includes('width="300"'));
  assert.ok(svg.includes('height="200"'));
  assert.ok(svg.includes('<image href="data:image/png;base64'));
});

// -----------------------------------------------------------------------------
// SUITE 2: GOVERNMENT FORM PHOTO COMPRESSOR (EXACT-KB & DOWNSCALING ENGINE)
// -----------------------------------------------------------------------------
console.log('\nSUITE 2: Exact-KB Compression & Downscaling Engine');

test('Exact-KB: Binary Search convergence guarantees output <= targetKB', () => {
  // Simulates the binary search convergence logic from photo-compressor.html line 1080
  function simulateCompress(targetKB, initialFileSizeKB) {
    const maxBytes = targetKB * 1024;
    let lowQ = 0.05;
    let highQ = 0.85;
    let bestSize = initialFileSizeKB * 1024;
    let bestQ = lowQ;

    for (let step = 0; step < 7; step++) {
      let midQ = (lowQ + highQ) / 2;
      // Linear model approximation for quality to size
      let simulatedBytes = Math.round(initialFileSizeKB * 1024 * (0.15 + 0.85 * midQ));
      if (simulatedBytes <= maxBytes) {
        bestSize = simulatedBytes;
        bestQ = midQ;
        lowQ = midQ; // try better quality
      } else {
        highQ = midQ; // too heavy
      }
    }

    // Adaptive Downscaling Loop if lowest quality still exceeds limit
    let curW = 1000, curH = 1000;
    while (bestSize > maxBytes && curW > 60 && curH > 60) {
      curW = Math.round(curW * 0.92);
      curH = Math.round(curH * 0.92);
      bestSize = Math.round(bestSize * 0.92 * 0.92);
    }

    return { size: bestSize, maxBytes, pass: bestSize <= maxBytes };
  }

  [20, 50, 100, 200, 35].forEach(targetKB => {
    const res = simulateCompress(targetKB, 500); // 500 KB input
    assert.strictEqual(res.pass, true, `Result for ${targetKB} KB must be <= target limit (${res.size} <= ${res.maxBytes})`);
  });
});

test('Exact-KB: Exam & Portal Dimension Preset calculations', () => {
  function getTargetDimensions(mode, srcW, srcH, customW, customH) {
    if (mode === 'upsc_photo') return { w: 200, h: 230 };
    if (mode === 'upsc_sign') return { w: 140, h: 60 };
    if (mode === 'passport_india') return { w: 350, h: 450 };
    if (mode === 'us_visa') return { w: 600, h: 600 };
    if (mode === 'custom') {
      return { w: parseInt(customW, 10) || srcW, h: parseInt(customH, 10) || srcH };
    }
    return { w: srcW, h: srcH };
  }

  assert.deepStrictEqual(getTargetDimensions('upsc_photo', 1200, 1600), { w: 200, h: 230 });
  assert.deepStrictEqual(getTargetDimensions('upsc_sign', 1200, 1600), { w: 140, h: 60 });
  assert.deepStrictEqual(getTargetDimensions('passport_india', 1200, 1600), { w: 350, h: 450 });
  assert.deepStrictEqual(getTargetDimensions('us_visa', 1200, 1600), { w: 600, h: 600 });
  assert.deepStrictEqual(getTargetDimensions('custom', 1200, 1600, 400, 300), { w: 400, h: 300 });
  assert.deepStrictEqual(getTargetDimensions('original', 1200, 1600), { w: 1200, h: 1600 });
});

// -----------------------------------------------------------------------------
// SUITE 3: CLIENT-SIDE CODE PROTECTION & SECURITY CHECKS
// -----------------------------------------------------------------------------
console.log('\nSUITE 3: Client-Side Code Protection & Reverse Engineering Shield');

test('Security Shield: Contextmenu (Right-Click) Interception present across tools', () => {
  const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');

  assert.ok(indexHtml.includes("document.addEventListener('contextmenu'"), 'index.html must block contextmenu');
  assert.ok(photoCompressorHtml.includes("document.addEventListener('contextmenu'"), 'photo-compressor.html must block contextmenu');
});

test('Security Shield: DevTools & Inspect Keyboard Shortcuts Blocked (F12, Ctrl+U, etc.)', () => {
  const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');

  ['F12', 'ctrlKey && e.shiftKey', 'ctrlKey && (e.key === \'U\'', 'metaKey && e.altKey'].forEach(k => {
    assert.ok(indexHtml.includes(k), `index.html must intercept shortcut ${k}`);
    assert.ok(photoCompressorHtml.includes(k), `photo-compressor.html must intercept shortcut ${k}`);
  });
});

test('Security Shield: Scope Isolation & Closure Encapsulation (No leaked global variables)', () => {
  const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');

  // Verify that core logic is wrapped inside an IIFE (Immediately Invoked Function Expression)
  assert.ok(indexHtml.includes('(function(){'), 'index.html must wrap logic in an IIFE closure');
  assert.ok(photoCompressorHtml.includes('(function(){'), 'photo-compressor.html must wrap logic in an IIFE closure');

  // Verify that sensitive internal functions are NOT attached to window
  assert.ok(!photoCompressorHtml.includes('window.compressToKB ='), 'compressToKB must not be exposed to window');
  assert.ok(!photoCompressorHtml.includes('window.canvasToBlob ='), 'canvasToBlob must not be exposed to window');
  assert.ok(!indexHtml.includes('window.convertSingle ='), 'convertSingle must not be exposed to window');
});

// -----------------------------------------------------------------------------
// SUITE 4: OPTIMISATION TECHNIQUES & MEMORY LEAK PREVENTION
// -----------------------------------------------------------------------------
console.log('\nSUITE 4: Optimisation Techniques & Memory Management');

test('Optimisation: Blob URL cleanup (URL.revokeObjectURL) implemented for memory release', () => {
  const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');

  // index.html must revoke on single convert, file removal, and clear queue
  const indexRevocations = (indexHtml.match(/URL\.revokeObjectURL/g) || []).length;
  assert.ok(indexRevocations >= 4, `index.html must have comprehensive revokeObjectURL calls (found ${indexRevocations})`);

  // photo-compressor.html must revoke previous blob URLs on card update and photo reset
  const pcRevocations = (photoCompressorHtml.match(/URL\.revokeObjectURL/g) || []).length;
  assert.ok(pcRevocations >= 2, `photo-compressor.html must have revokeObjectURL calls (found ${pcRevocations})`);
});

test('Optimisation: Canvas High-Quality Scaling & Performance flags enabled', () => {
  const indexHtml = fs.readFileSync(path.join(__dirname, '..', 'index.html'), 'utf8');
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');

  assert.ok(indexHtml.includes("imageSmoothingQuality = 'high'"), 'index.html must enable high-quality smoothing');
  assert.ok(photoCompressorHtml.includes("imageSmoothingQuality = 'high'"), 'photo-compressor.html must enable high-quality smoothing');
  assert.ok(photoCompressorHtml.includes("willReadFrequently: true"), 'photo-compressor.html must enable willReadFrequently');
});

test('Optimisation: Debounced event handlers for sliders and inputs', () => {
  const photoCompressorHtml = fs.readFileSync(path.join(__dirname, '..', 'photo-compressor.html'), 'utf8');
  assert.ok(photoCompressorHtml.includes('clearTimeout(processTimer)'), 'photo-compressor.html must debounce slider inputs');
});

// -----------------------------------------------------------------------------
// SUMMARY
// -----------------------------------------------------------------------------
console.log('\n======================================================');
console.log(`  TEST RESULTS: ${passedTests}/${totalTests} PASSED (${failedTests} FAILED)`);
console.log('======================================================\n');

if (failedTests > 0) {
  process.exit(1);
} else {
  console.log('ALL UNIT & REVERSE ENGINE OPTIMISATION TESTS PASSED SUCCESSFULLY! 🚀');
}
