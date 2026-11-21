import { Body, Controller, Inject, Post } from '@nestjs/common';
import { ApiBearerAuth, ApiOperation, ApiTags } from '@nestjs/swagger';
import { ConversationDto } from './conversation.dto';
import { ConversationService } from './conversation.service';

@ApiTags('Conversa')
@ApiBearerAuth()
@Controller({ path: 'conversa', version: '1' })
export class ConversationController {
  constructor(@Inject(ConversationService) private readonly conversation: ConversationService) {}
  @Post()
  @ApiOperation({ summary: 'Consulta documentos acadêmicos; retorna resposta, fontes ou fallback' })
  converse(@Body() input: ConversationDto) {
    return this.conversation.converse(input);
  }
}
