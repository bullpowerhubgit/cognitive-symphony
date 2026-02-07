import { NextResponse } from 'next/server'

export async function GET() {
  console.log('Cron: Running backup...')

  return NextResponse.json({
    success: true,
    backup_created: false,
    timestamp: new Date().toISOString(),
  })
}
