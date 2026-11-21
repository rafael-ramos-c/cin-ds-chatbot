import { Module } from '@nestjs/common';
import { OrchestrationModule } from '../../orchestration/orchestration.module';
import { ConversationController } from './conversation.controller';
import { ConversationService } from './conversation.service';

@Module({
  imports: [OrchestrationModule],
  controllers: [ConversationController],
  providers: [ConversationService],
})
export class ConversationModule {}
