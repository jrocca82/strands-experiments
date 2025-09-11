// src/app.module.ts
import { Module } from '@nestjs/common';
import { CircuitModule } from './circuit/circuit.module';
import { McpModule } from './mcp/mcp.module';
import { AppService } from './app.service';
import { AppController } from './app.controller';

@Module({
  imports: [CircuitModule, McpModule],
  controllers: [AppController],
  providers: [AppService],
})
export class AppModule {}
