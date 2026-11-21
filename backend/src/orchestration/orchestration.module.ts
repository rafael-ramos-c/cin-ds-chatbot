import { Module } from '@nestjs/common';
import { AiServiceModule } from '../ai-service/ai-service.module';
import { FALLBACK_DISTANCE_THRESHOLD, readFallbackDistanceThreshold } from './fallback.config';
import { FallbackService } from './fallback.service';
import { OrchestrationService } from './orchestration.service';

@Module({
  imports: [AiServiceModule],
  providers: [
    {
      provide: FALLBACK_DISTANCE_THRESHOLD,
      useFactory: readFallbackDistanceThreshold,
    },
    FallbackService,
    OrchestrationService,
  ],
  exports: [OrchestrationService],
})
export class OrchestrationModule {}
