import { seedPromoCode } from '../src/promo.js';

seedPromoCode('FRIEND100', 100, { label: '100 words for friends' });
seedPromoCode('FRIEND500', 500, { label: '500 words for friends' });

console.log('Seeded promo codes: FRIEND100 (100 words), FRIEND500 (500 words)');
