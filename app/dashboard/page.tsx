export default function DashboardPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 py-8">
        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Gesamtumsatz"
            value="&euro;0,00"
            change="+0%"
            positive={true}
          />
          <StatCard
            title="Verk&auml;ufe (Heute)"
            value="0"
            change="0 neue"
          />
          <StatCard
            title="Aktive Affiliates"
            value="0"
            change="0 Partner"
          />
          <StatCard
            title="Kunden (Gesamt)"
            value="0"
            change="0 heute"
          />
        </div>

        {/* Quick Actions */}
        <div className="bg-white rounded-lg shadow p-6 mb-8">
          <h2 className="text-xl font-bold mb-4">Schnellzugriff</h2>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <QuickAction
              icon="📊"
              title="Analytics"
              description="Detaillierte Statistiken"
              href="/dashboard/analytics"
            />
            <QuickAction
              icon="📧"
              title="E-Mail Automation"
              description="Kampagnen verwalten"
              href="/dashboard/automation"
            />
            <QuickAction
              icon="🤝"
              title="Affiliates"
              description="Partner-Übersicht"
              href="/dashboard/affiliates"
            />
          </div>
        </div>

        {/* Recent Activity */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Letzte Aktivitäten</h2>
          <div className="text-center text-gray-500 py-8">
            <p>Keine Aktivitäten vorhanden</p>
            <p className="text-sm mt-2">Verbinde dein Digistore24-Konto um loszulegen</p>
          </div>
        </div>
      </main>
    </div>
  )
}

function StatCard({ title, value, change, positive }: any) {
  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h3 className="text-gray-500 text-sm font-medium">{title}</h3>
      <p className="text-3xl font-bold text-gray-900 mt-2">{value}</p>
      <p className={`text-sm mt-2 ${positive ? 'text-green-600' : 'text-gray-500'}`}>
        {change}
      </p>
    </div>
  )
}

function QuickAction({ icon, title, description, href }: any) {
  return (
    <a
      href={href}
      className="block p-4 bg-gray-50 hover:bg-gray-100 rounded-lg transition"
    >
      <div className="text-3xl mb-2">{icon}</div>
      <h3 className="font-bold text-gray-900">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </a>
  )
}
