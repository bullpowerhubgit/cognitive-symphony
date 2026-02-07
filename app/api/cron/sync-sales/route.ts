import { NextResponse } from 'next/server'

export async function GET() {
  console.log('Cron: Syncing sales...')

  // TODO: Digistore24 API aufrufen
  // TODO: Verkäufe synchronisieren

  return NextResponse.json({
    success: true,
    synced: 0,
    timestamp: new Date().toISOString(),
  })
}
