import { registerAs } from '@nestjs/config';

export default registerAs('swagger', () => ({
  title: process.env.SWAGGER_TITLE ?? 'SecGrad API',
  description: process.env.SWAGGER_DESCRIPTION ?? 'Conversa acadêmica com fontes e fallback',
  version: process.env.SWAGGER_VERSION ?? '1.0.0',
  path: process.env.SWAGGER_PATH ?? 'api/docs',
}));
