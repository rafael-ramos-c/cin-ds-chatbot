// Fixture do contrato HTTP anterior à migração; não é importada na aplicação real.
import { Module } from '@nestjs/common';
import { AiServiceModule } from '../../src/ai-service/ai-service.module';
import { OrchestrationModule } from '../../src/orchestration/orchestration.module';
import { AppController } from './app.controller';
import { AppService } from './app.service';
@Module({
  imports: [AiServiceModule, OrchestrationModule],
  controllers: [AppController],
  providers: [AppService],
})
export class LegacyContractModule {}
