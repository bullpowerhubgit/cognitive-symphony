import { NextResponse } from 'next/server'

export async function GET() {
  // TODO: Datenbank-Abfrage
  return NextResponse.json({
    products: [],
    total: 0,
  })
}

export async function POST(request: Request) {
  const body = await request.json()

  // TODO: Produkt erstellen
  return NextResponse.json({
    success: true,
    product: body,
  })
}
