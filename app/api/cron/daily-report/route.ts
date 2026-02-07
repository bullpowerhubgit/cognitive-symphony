import { NextResponse } from 'next/server'

export async function GET() {
  console.log('Cron: Generating daily report...')

  return NextResponse.json({
    success: true,
    sent: false,
    timestamp: new Date().toISOString(),
  })
}
