import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  const port = 8000;
  await app.listen(port);
  console.log(`NestJS app running on http://localhost:${port}`);
}
bootstrap();
