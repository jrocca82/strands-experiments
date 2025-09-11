// src/circuit/circuit.module.ts
import { Module } from '@nestjs/common';
import { CircuitService } from './circuit.service';

@Module({
  providers: [CircuitService],
  exports: [CircuitService],
})
export class CircuitModule {}
