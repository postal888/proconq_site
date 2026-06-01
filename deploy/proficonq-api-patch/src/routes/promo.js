import { getRequestUser, getUserById } from '../auth.js';
import { redeemPromoCode } from '../promo.js';
import { publicUserWithLimits } from '../wordLimit.js';

const ERROR_STATUS = {
  missing_code: 400,
  invalid_code: 404,
  already_redeemed: 409,
  code_exhausted: 410,
  already_premium: 400,
  invalid_user: 400,
};

export default async function promoRoutes(fastify) {
  fastify.post('/api/promo/redeem', async (req, reply) => {
    const user = await getRequestUser(req);
    if (!user) return reply.code(401).send({ error: 'unauthorized' });

    const result = redeemPromoCode(user.id, req.body?.code);
    if (result.error) {
      const status = ERROR_STATUS[result.error] || 400;
      return reply.code(status).send({ error: result.error });
    }

    const updated = getUserById(user.id);
    return reply.send({
      ok: true,
      wordLimit: result.wordLimit,
      code: result.code,
      user: publicUserWithLimits(updated),
    });
  });
}
