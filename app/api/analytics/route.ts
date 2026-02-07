import { NextResponse } from 'next/server'

export async function GET() {
  return NextResponse.json({
    today: {
      sales: 0,
      revenue: 0,
      customers: 0,
    },
    week: {
      sales: 0,
      revenue: 0,
      customers: 0,
    },
    month: {
      sales: 0,
      revenue: 0,
      customers: 0,
    },
  })
}
