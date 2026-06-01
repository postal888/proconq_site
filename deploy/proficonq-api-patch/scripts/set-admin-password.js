import { hashPassword } from '../src/auth.js';
import { readFileSync, writeFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';
import { randomBytes } from 'node:crypto';

const here = dirname(fileURLToPath(import.meta.url));
const envPath = process.env.ENV_PATH || join(here, '..', '.env');

function upsertEnv(key, value) {
  let lines = [];
  if (existsSync(envPath)) {
    lines = readFileSync(envPath, 'utf8').split(/\r?\n/);
  }
  const prefix = `${key}=`;
  let found = false;
  lines = lines.map((line) => {
    if (line.startsWith(prefix)) {
      found = true;
      return `${key}=${value}`;
    }
    return line;
  });
  if (!found) lines.push(`${key}=${value}`);
  writeFileSync(envPath, lines.filter((l, i, arr) => l.length || i < arr.length - 1).join('\n') + '\n', 'utf8');
}

function readPasswordArg(argv) {
  const fileArg = argv.find((a) => a.startsWith('--file='));
  if (fileArg) return readFileSync(fileArg.slice('--file='.length), 'utf8').trim();
  if (argv[2] && !argv[2].startsWith('--')) return argv[2];
  if (process.env.ADMIN_PASSWORD_PLAIN) return String(process.env.ADMIN_PASSWORD_PLAIN);
  return randomBytes(9).toString('base64url');
}

const password = readPasswordArg(process.argv);
const username = process.argv[3] && !process.argv[3].startsWith('--')
  ? process.argv[3]
  : (process.env.ADMIN_USERNAME || 'admin');
const { hash, salt } = hashPassword(password);

upsertEnv('ADMIN_USERNAME', username);
upsertEnv('ADMIN_PASSWORD_HASH', hash);
upsertEnv('ADMIN_PASSWORD_SALT', salt);

console.log(`Admin username: ${username}`);
console.log('Admin password updated.');
console.log(`Updated ${envPath}`);
