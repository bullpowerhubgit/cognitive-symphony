import { NextResponse } from 'next/server'

export async function POST(request: Request) {
  try {
    const body = await request.json()

    console.log('Digistore24 Webhook received:', body)

    // TODO: Webhook verarbeiten
    // - Signatur verifizieren
    // - Event-Typ prüfen
    // - Daten speichern

    return NextResponse.json({
      success: true,
      received: true
    })
  } catch (error) {
    console.error('Webhook error:', error)
    return NextResponse.json(
      { success: false, error: 'Invalid payload' },
      { status: 400 }
    )
  }
}
