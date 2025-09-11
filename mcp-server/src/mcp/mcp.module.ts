// src/mcp/mcp.module.ts
import { Module } from '@nestjs/common';
import { CircuitModule } from '../circuit/circuit.module';
import { CircuitMcpService } from './mcp.service';
import { McpController } from './mcp.controller';

@Module({
  imports: [CircuitModule],
  providers: [CircuitMcpService],
  controllers: [McpController],
  exports: [CircuitMcpService],
})
export class McpModule {}
