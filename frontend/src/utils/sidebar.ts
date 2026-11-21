import type { SidebarData } from '@cincoders/cinnamon';
import { MessageSquare } from 'lucide-react';
import { Links } from './enums';
import cinLogo from '../assets/icons/cin-logo.svg';
export const sidebar: SidebarData = {
  appName: 'Assistente SecGrad CIn', appLogoSrc: cinLogo,
  navMain: [{ id: 'chat', title: 'Conversa acadêmica', href: Links.CHAT, IconComponent: MessageSquare }],
};
