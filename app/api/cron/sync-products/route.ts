import { NextResponse } from 'next/server'

export async function GET() {
  console.log('Cron: Syncing products...')

  return NextResponse.json({
    success: true,
    synced: 0,
    timestamp: new Date().toISOString(),
  })
}
