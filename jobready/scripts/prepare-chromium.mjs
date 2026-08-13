// Unpacks the headless Chromium bundled in `@sparticuz/chromium` so Remotion
// can render without downloading a browser. Idempotent — skips work if the
// files already exist in /tmp.
//
// Extracts:
//   chromium.br    -> /tmp/chromium          (the browser binary)
//   fonts.tar.br   -> /tmp/fonts             (Open Sans + fonts.conf)
//   al2023.tar.br  -> /tmp/al2023/lib        (libnss3, libnspr4, … the libs Chromium links)
//
// SwiftShader (swiftshader.tar.br) is intentionally skipped: this composition
// is pure CSS, so no WebGL is needed.
import { inflate } from '@sparticuz/chromium';
import { execFileSync } from 'node:child_process';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const binDir = join(here, '..', 'node_modules', '@sparticuz', 'chromium', 'bin');

const chromiumBin = await inflate(join(binDir, 'chromium.br'));
await inflate(join(binDir, 'fonts.tar.br'));
await inflate(join(binDir, 'al2023.tar.br'));

const version = execFileSync(chromiumBin, ['--version'], {
  env: { ...process.env, LD_LIBRARY_PATH: '/tmp/al2023/lib' },
  encoding: 'utf8',
});

console.log('Chromium ready:', version.trim());
