# Digistore24 Pro Automation Suite v3.0

Das ultimative All-in-One Automation Tool für Digistore24 mit KI-Integration.

## Features

- Vollständige Digistore24 Integration
- 30+ Automatische Cron-Jobs
- KI-gestützte Analytics
- Advanced Dashboard
- E-Mail Automation
- Affiliate Management
- Real-Time Webhooks
- Production-Ready

## Quick Start

### Installation

```bash
# Dependencies installieren
npm install

# .env.local erstellen
cp .env.example .env.local

# Secrets generieren
openssl rand -base64 32  # Für NEXTAUTH_SECRET
openssl rand -base64 32  # Für JWT_SECRET

# Development Server
npm run dev
```

Öffne: http://localhost:3000

### Datenbank Setup

```bash
# Prisma generieren
npx prisma generate

# Datenbank pushen (Development)
npx prisma db push

# Prisma Studio (optional)
npx prisma studio
```

## Deployment auf Vercel

1. **Repository auf GitHub pushen**
```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/USERNAME/digistore24-automation.git
git push -u origin main
```

2. **Auf Vercel deployen**
- Gehe zu https://vercel.com/new
- Importiere dein Repository
- Setze Environment Variables (siehe .env.example)
- Deploy!

## Environment Variables

Benötigte Variablen für Vercel:

```env
NEXTAUTH_SECRET=...
JWT_SECRET=...
DATABASE_URL=... (von Vercel Postgres)
DIGISTORE_API_KEY=...
DIGISTORE_API_SECRET=...
```

## API Endpunkte

### Health Check
```bash
GET /api/health
```

### Products
```bash
GET /api/products
POST /api/products
```

### Sales
```bash
GET /api/sales
```

### Analytics
```bash
GET /api/analytics
```

### Webhooks
```bash
POST /api/webhooks/digistore
```

### Cron Jobs
```bash
GET /api/cron/sync-sales
GET /api/cron/sync-products
GET /api/cron/daily-report
GET /api/cron/backup
```

## Seiten

- `/` - Homepage
- `/dashboard` - Haupt-Dashboard
- `/dashboard/analytics` - Erweiterte Analytics
- `/dashboard/settings` - Einstellungen

## Development

```bash
# Development Server
npm run dev

# Build
npm run build

# Production Server
npm start

# Type Check
npm run type-check

# Linting
npm run lint
```

## Sicherheit

- HTTPS/SSL (via Vercel)
- CORS Protection
- XSS Protection
- CSRF Protection
- Rate Limiting
- Webhook Signature Verification

## Lizenz

MIT

## Credits

Erstellt mit Next.js 14, TypeScript, Tailwind CSS & Prisma
