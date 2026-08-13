import { Config } from '@remotion/cli/config';
import fs from 'node:fs';

// ---------------------------------------------------------------------------
// This sandbox cannot download a browser (only npm + GitHub + PyPI are
// reachable). We therefore render with the headless Chromium binary bundled
// in the `@sparticuz/chromium` npm package — see scripts/prepare-chromium.mjs,
// which unpacks it to /tmp along with the NSS libraries it needs.
// ---------------------------------------------------------------------------

const browserExecutable = process.env.REMOTION_BROWSER_EXECUTABLE ?? '/tmp/chromium';

const libDir = process.env.CHROMIUM_LIB_DIR ?? '/tmp/al2023/lib';
if (fs.existsSync(libDir)) {
  process.env.LD_LIBRARY_PATH = [libDir, process.env.LD_LIBRARY_PATH]
    .filter(Boolean)
    .join(':');
}

if (fs.existsSync(browserExecutable)) {
  Config.setBrowserExecutable(browserExecutable);
} else {
  console.warn(
    `[jobready] Browser not found at ${browserExecutable}. ` +
      'Run `node scripts/prepare-chromium.mjs` first.',
  );
}

Config.setVideoImageFormat('jpeg');
Config.setJpegQuality(90);
Config.setConcurrency(1);
Config.setOverwriteOutput(true);
