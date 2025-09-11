// src/mcp/mcp.controller.ts
import { Controller, Get, Res } from '@nestjs/common';
import type { Response } from 'express';
import { CircuitMcpService } from './mcp.service';

@Controller()
export class McpController {
  constructor(private readonly mcpService: CircuitMcpService) {}

  @Get('stream')
  sse(@Res() res: Response) {
    console.log('[MCP Controller] /stream endpoint hit');

    this.mcpService
      .connect()
      .then(() => console.log('[MCP Controller] MCP server connected'))
      .catch((err) => {
        console.error('[MCP Controller] SSE connection failed', err);
        try {
          res.end();
        } catch (e) {
          console.log(e);
        }
      });
  }
}
