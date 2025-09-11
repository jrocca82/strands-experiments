/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/require-await */
// src/circuit/circuit.service.ts
import { Injectable } from '@nestjs/common';

@Injectable()
export class CircuitService {
  private circuitToken: string | null = 'demo-admin-token'; // fake cached token

  // demo method to mimic header logic
  private async getChatbotToken(): Promise<string> {
    // in real service, would fetch if expired
    return this.circuitToken!;
  }

  // demo callByContract that mimics header behavior
  async callByContract({
    operationId,
    params,
    circuitToken,
  }: {
    operationId: string;
    params: any;
    circuitToken?: { issuer: string; jwt: string };
  }) {
    const extraHeaders: Record<string, string> = {};

    // mock authContracts logic
    const authContracts = { someAuthOp: true }; // pretend some ops require special auth

    if (!(operationId in authContracts)) {
      extraHeaders['Authorization'] = `Bearer ${await this.getChatbotToken()}`;
    } else if (circuitToken?.issuer === 'circuit') {
      extraHeaders['Authorization'] = `Bearer ${circuitToken.jwt}`;
    } else {
      extraHeaders['Authorization'] = `Bearer ${await this.getChatbotToken()}`;
      if (circuitToken) extraHeaders['x-on-behalf-of'] = circuitToken.jwt;
    }

    // return mock response including headers for demo/testing
    return {
      operationId,
      params,
      circuitToken,
      extraHeaders,
      message: 'This is a mock response from Circuit with header logic',
    };
  }
}
