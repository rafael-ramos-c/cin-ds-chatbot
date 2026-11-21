import { ConfigService } from '@nestjs/config';
import { NestFactory } from '@nestjs/core';
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';
import { cleanupOpenApiDoc } from 'nestjs-zod';
import { AppModule } from './app.module';
import { configureApp } from './configure-app';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);

  const configService = app.get(ConfigService);

  configureApp(app);

  const swaggerBuilder = new DocumentBuilder()
    .setTitle(configService.get('swagger.title', 'SecGrad API'))
    .setDescription(configService.get('swagger.description', 'API documentation'))
    .setVersion(configService.get('swagger.version', '1.0.0'))
    .addBearerAuth();

  const authServerUrl = configService.get<string>('keycloak.authServerUrl');
  const realm = configService.get<string>('keycloak.realm');
  if (authServerUrl && realm) {
    const issuer = `${authServerUrl.replace(/\/$/, '')}/realms/${realm}`;
    swaggerBuilder.addOAuth2({
      type: 'oauth2',
      flows: {
        password: {
          tokenUrl: `${issuer}/protocol/openid-connect/token`,
          authorizationUrl: `${issuer}/protocol/openid-connect/auth`,
          scopes: {},
        },
      },
    });
  }

  const document = cleanupOpenApiDoc(SwaggerModule.createDocument(app, swaggerBuilder.build()));
  SwaggerModule.setup(configService.get('swagger.path', 'api/docs'), app, document);

  const port = configService.get<number>('PORT', 3000);
  await app.listen(port);
}

bootstrap().catch((error) => {
  console.error('Não foi possível iniciar a API.', error);
  process.exitCode = 1;
});
