import { Body, Controller, Get, Inject, Post } from '@nestjs/common';
import { AppService } from './app.service.js';
import { OrchestrationService } from './orchestration/orchestration.service.js';
import type {
  OrchestrationRequest,
  OrchestrationResult,
} from './orchestration/orchestration.types.js';

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
  async conversar(
    @Body() request: OrchestrationRequest,
  ): Promise<OrchestrationResult> {
    return this.orchestrationService.processar(request);
  }
}