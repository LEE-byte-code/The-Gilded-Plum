const sharp = require('sharp');
const fs = require('fs');
const path = require('path');
const os = require('os');

const imagesDir = path.join(__dirname, 'images');
const files = fs.readdirSync(imagesDir);

const imageFiles = files.filter(f => /\.(jpg|jpeg|png)$/i.test(f));

console.log(`Found ${imageFiles.length} images to process...\n`);

(async () => {
    for (const file of imageFiles) {
        const inputPath = path.join(imagesDir, file);
        const baseName = path.parse(file).name;
        const ext = path.extname(file);

        // Never resize up, only down. Hero gets larger threshold.
        const maxWidth = baseName.includes('hero') ? 1920 : 1200;

        const originalSize = fs.statSync(inputPath).size;

        // --- WebP output ---
        const webpPath = path.join(imagesDir, `${baseName}.webp`);
        try {
            const metadata = await sharp(inputPath).metadata();
            const resizeWidth = metadata.width > maxWidth ? maxWidth : null;

            const pipeline = sharp(inputPath);
            if (resizeWidth) {
                pipeline.resize(resizeWidth, null, { fit: 'inside', withoutEnlargement: true });
            }
            pipeline.webp({ quality: 80 });
            await pipeline.toFile(webpPath);

            const webpSize = fs.statSync(webpPath).size;
            const webpSavings = ((1 - webpSize / originalSize) * 100).toFixed(1);
            const dims = resizeWidth ? `${resizeWidth}w` : `${metadata.width}w`;
            console.log(`✓ ${baseName}.webp  ${dims}  ${(originalSize / 1024).toFixed(0)}KB → ${(webpSize / 1024).toFixed(0)}KB  -${webpSavings}%`);
        } catch (err) {
            console.error(`✗ ${baseName}.webp: ${err.message}`);
        }

        // --- Recompressed JPEG output (skip PNG) ---
        if (ext !== '.png') {
            const tmpPath = path.join(os.tmpdir(), `${baseName}-tmp${ext}`);
            const jpegPath = path.join(imagesDir, `${baseName}${ext}`);

            try {
                const metadata = await sharp(inputPath).metadata();
                const resizeWidth = metadata.width > maxWidth ? maxWidth : null;

                const pipeline = sharp(inputPath);
                if (resizeWidth) {
                    pipeline.resize(resizeWidth, null, { fit: 'inside', withoutEnlargement: true });
                }
                pipeline.jpeg({ quality: 82, mozjpeg: true });
                await pipeline.toFile(tmpPath);

                // Swap temp file with original
                fs.unlinkSync(inputPath);
                fs.renameSync(tmpPath, jpegPath);

                const newSize = fs.statSync(jpegPath).size;
                const savings = ((1 - newSize / originalSize) * 100).toFixed(1);
                const dims = resizeWidth ? `${resizeWidth}w` : `${metadata.width}w`;
                console.log(`✓ ${baseName}${ext}  ${dims}  ${(originalSize / 1024).toFixed(0)}KB → ${(newSize / 1024).toFixed(0)}KB  -${savings}%  (recompressed)`);
            } catch (err) {
                console.error(`✗ ${baseName}${ext}: ${err.message}`);
                // Clean up temp file if it exists
                try { fs.unlinkSync(tmpPath); } catch (_) {}
            }
        }
    }

    console.log('\nDone! All images optimized.');
})();
