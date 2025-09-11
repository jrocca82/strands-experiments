// src/mcp/mcp.service.ts
import { Injectable, OnModuleInit } from '@nestjs/common';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { CircuitService } from '../circuit/circuit.service';
import { z } from 'zod';
import { randomUUID } from 'crypto';

@Injectable()
export class CircuitMcpService implements OnModuleInit {
  private server: McpServer;

  constructor(private readonly circuitService: CircuitService) {}

  onModuleInit() {
    this.server = new McpServer({ name: 'demo-server', version: '1.0.0' });
    this.registerTools();
  }

  private registerTools() {
    console.log('[MCP] Registering tools...');
    this.server.registerTool(
      'circuit-call',
      {
        title: 'Circuit API Tool',
        description: 'Call Circuit operations via MCP',
        inputSchema: {
          operationId: z.string(),
          params: z.record(z.any()),
          circuitToken: z
            .object({ issuer: z.string(), jwt: z.string() })
            .optional(),
        },
        outputSchema: {
          content: z.array(z.object({ type: z.string(), text: z.string() })),
        },
      },
      async ({ operationId, params, circuitToken }) => {
        const response = await this.circuitService.callByContract({
          operationId,
          params,
          circuitToken,
        });

        return {
          content: [
            {
              type: 'resource',
              resource: {
                uri:
                  'data:application/json;base64,' +
                  Buffer.from(JSON.stringify(response)).toString('base64'),
                text: JSON.stringify(response),
              },
            },
          ],
        };
      },
    );
    console.log('[MCP] Tools registered.');
  }

  public connect() {
    console.log('[MCP] connect() called');
    const transport = new StreamableHTTPServerTransport({
      allowedOrigins: ['*'],
      sessionIdGenerator: () => randomUUID(),
    });
    const conn = this.server.connect(transport);
    console.log('[MCP] connect() returned', conn);
    return conn;
  }
}
