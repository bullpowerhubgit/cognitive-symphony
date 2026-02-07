export default function AnalyticsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Analytics</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          {/* Revenue Chart Placeholder */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Umsatz-Entwicklung</h2>
            <div className="h-64 flex items-center justify-center bg-gray-50 rounded">
              <p className="text-gray-500">Chart kommt hier hin</p>
            </div>
          </div>

          {/* Sales Chart Placeholder */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Verkäufe pro Tag</h2>
            <div className="h-64 flex items-center justify-center bg-gray-50 rounded">
              <p className="text-gray-500">Chart kommt hier hin</p>
            </div>
          </div>

          {/* Top Products */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Top Produkte</h2>
            <div className="text-center text-gray-500 py-8">
              <p>Keine Daten vorhanden</p>
            </div>
          </div>

          {/* Top Affiliates */}
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-xl font-bold mb-4">Top Affiliates</h2>
            <div className="text-center text-gray-500 py-8">
              <p>Keine Daten vorhanden</p>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
