import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    sales: [],
    total: 0,
    revenue: 0,
  })
}
