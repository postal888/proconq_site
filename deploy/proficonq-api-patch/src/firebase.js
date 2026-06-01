import admin from 'firebase-admin';
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const here = path.dirname(fileURLToPath(import.meta.url));
let initialized = false;

export function initFirebase() {
  if (initialized) return;
  const keyPath =
    process.env.FIREBASE_SERVICE_ACCOUNT_PATH ||
    path.join(here, '..', 'serviceAccountKey.json');
  if (!fs.existsSync(keyPath)) {
    throw new Error(`Firebase service account not found: ${keyPath}`);
  }
  const serviceAccount = JSON.parse(fs.readFileSync(keyPath, 'utf8'));
  admin.initializeApp({ credential: admin.credential.cert(serviceAccount) });
  initialized = true;
}

export async function verifyFirebaseIdToken(idToken) {
  initFirebase();
  return admin.auth().verifyIdToken(idToken);
}

/** Firebase JWT (xxx.yyy.zzz) vs hex session token from pq_session */
export function looksLikeFirebaseJwt(token) {
  if (!token || typeof token !== 'string') return false;
  const parts = token.split('.');
  return parts.length === 3 && token.length > 80;
}
