import { Body, Controller, Get, Inject, Post } from '@nestjs/common';
import { OrchestrationService } from '../../src/orchestration/orchestration.service';
import type {
  OrchestrationRequest,
  OrchestrationResult,
} from '../../src/orchestration/orchestration.types';
import { AppService } from './app.service';

@Controller()
export class AppController {
  constructor(
    private readonly appService: AppService,
    @Inject(OrchestrationService)
    private readonly orchestrationService: OrchestrationService,
  ) {}

  @Get()
  getHello(): string {
    return this.appService.getHello();
  }

  @Post('api/v1/conversa')
  async conversar(@Body() request: OrchestrationRequest): Promise<OrchestrationResult> {
    return this.orchestrationService.processar(request);
  }
}
