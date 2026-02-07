export default function DashboardPage() {
  return (
    <div className="flex min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      {/* Sidebar */}
      <aside className="w-64 bg-slate-900/50 backdrop-blur-xl border-r border-white/10">
        <div className="p-6">
          <h1 className="text-2xl font-bold text-white mb-8">
            🚀 Digistore24
          </h1>

          <nav className="space-y-2">
            <NavItem icon="📊" label="Dashboard" active />
            <NavItem icon="💰" label="Verkäufe" />
            <NavItem icon="📦" label="Produkte" />
            <NavItem icon="🤝" label="Affiliates" />
            <NavItem icon="👥" label="Kunden" />
            <NavItem icon="📧" label="Automation" />
            <NavItem icon="📈" label="Analytics" />
            <NavItem icon="⚙️" label="Einstellungen" />
          </nav>
        </div>

        <div className="absolute bottom-0 w-64 p-6 border-t border-white/10">
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-full bg-gradient-to-r from-purple-500 to-pink-500" />
            <div>
              <p className="text-white text-sm font-medium">Admin</p>
              <p className="text-gray-400 text-xs">admin@example.com</p>
            </div>
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 p-8 overflow-y-auto">
        {/* Header */}
        <div className="mb-8">
          <h2 className="text-3xl font-bold text-white mb-2">Willkommen zurück! 👋</h2>
          <p className="text-gray-400">Hier ist eine Übersicht deiner Performance</p>
        </div>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            title="Gesamtumsatz"
            value="€24,582"
            change="+12.5%"
            icon="💰"
            color="from-green-500 to-emerald-600"
            positive={true}
          />
          <StatCard
            title="Verkäufe (Heute)"
            value="143"
            change="+8.2%"
            icon="📊"
            color="from-blue-500 to-cyan-600"
            positive={true}
          />
          <StatCard
            title="Aktive Affiliates"
            value="28"
            change="+4"
            icon="🤝"
            color="from-purple-500 to-pink-600"
            positive={true}
          />
          <StatCard
            title="Kunden (Gesamt)"
            value="1,247"
            change="+23"
            icon="👥"
            color="from-orange-500 to-red-600"
            positive={true}
          />
        </div>

        {/* Charts Row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Revenue Chart */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Umsatz-Entwicklung</h3>
            <div className="h-64 flex items-center justify-center">
              <div className="text-center">
                <div className="text-6xl mb-4">📈</div>
                <p className="text-gray-400">Chart wird hier angezeigt</p>
              </div>
            </div>
          </div>

          {/* Top Products */}
          <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Top Produkte</h3>
            <div className="space-y-3">
              <ProductItem name="Premium Package" sales={245} revenue="€12,250" />
              <ProductItem name="Starter Bundle" sales={189} revenue="€5,670" />
              <ProductItem name="Pro Membership" sales={156} revenue="€4,680" />
              <ProductItem name="Basic Course" sales={98} revenue="€1,960" />
            </div>
          </div>
        </div>

        {/* Quick Actions & Activity */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Quick Actions */}
          <div className="lg:col-span-1 bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Schnellzugriff</h3>
            <div className="space-y-3">
              <QuickAction icon="➕" label="Neues Produkt" color="bg-blue-500" />
              <QuickAction icon="📧" label="E-Mail senden" color="bg-purple-500" />
              <QuickAction icon="📊" label="Report erstellen" color="bg-green-500" />
              <QuickAction icon="⚙️" label="Einstellungen" color="bg-orange-500" />
            </div>
          </div>

          {/* Recent Activity */}
          <div className="lg:col-span-2 bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10">
            <h3 className="text-xl font-bold text-white mb-4">Letzte Aktivitäten</h3>
            <div className="space-y-4">
              <Activity
                icon="💰"
                title="Neuer Verkauf"
                description="Premium Package von Max M."
                time="Vor 5 Min"
                color="text-green-400"
              />
              <Activity
                icon="🤝"
                title="Neuer Affiliate"
                description="Anna S. ist beigetreten"
                time="Vor 23 Min"
                color="text-purple-400"
              />
              <Activity
                icon="📧"
                title="E-Mail Kampagne"
                description="Newsletter versendet (1,247 Empfänger)"
                time="Vor 1 Std"
                color="text-blue-400"
              />
              <Activity
                icon="👥"
                title="Neuer Kunde"
                description="5 neue Registrierungen"
                time="Vor 2 Std"
                color="text-orange-400"
              />
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}

function NavItem({ icon, label, active = false }: any) {
  return (
    <a
      href="#"
      className={`flex items-center space-x-3 px-4 py-3 rounded-lg transition ${
        active
          ? 'bg-white/10 text-white'
          : 'text-gray-400 hover:bg-white/5 hover:text-white'
      }`}
    >
      <span className="text-xl">{icon}</span>
      <span className="font-medium">{label}</span>
    </a>
  )
}

function StatCard({ title, value, change, icon, color, positive }: any) {
  return (
    <div className="bg-slate-800/50 backdrop-blur-xl rounded-2xl p-6 border border-white/10 hover:border-white/20 transition">
      <div className="flex items-center justify-between mb-4">
        <div className={`w-12 h-12 rounded-xl bg-gradient-to-r ${color} flex items-center justify-center text-2xl`}>
          {icon}
        </div>
        <span className={`text-sm font-medium ${positive ? 'text-green-400' : 'text-red-400'}`}>
          {change}
        </span>
      </div>
      <p className="text-gray-400 text-sm mb-1">{title}</p>
      <p className="text-3xl font-bold text-white">{value}</p>
    </div>
  )
}

function ProductItem({ name, sales, revenue }: any) {
  return (
    <div className="flex items-center justify-between p-3 bg-slate-700/30 rounded-lg hover:bg-slate-700/50 transition">
      <div>
        <p className="text-white font-medium">{name}</p>
        <p className="text-gray-400 text-sm">{sales} Verkäufe</p>
      </div>
      <p className="text-green-400 font-bold">{revenue}</p>
    </div>
  )
}

function QuickAction({ icon, label, color }: any) {
  return (
    <button className="w-full flex items-center space-x-3 p-3 bg-slate-700/30 hover:bg-slate-700/50 rounded-lg transition">
      <div className={`w-10 h-10 ${color} rounded-lg flex items-center justify-center text-xl`}>
        {icon}
      </div>
      <span className="text-white font-medium">{label}</span>
    </button>
  )
}

function Activity({ icon, title, description, time, color }: any) {
  return (
    <div className="flex items-start space-x-4">
      <div className={`text-2xl ${color}`}>{icon}</div>
      <div className="flex-1">
        <p className="text-white font-medium">{title}</p>
        <p className="text-gray-400 text-sm">{description}</p>
      </div>
      <p className="text-gray-500 text-sm">{time}</p>
    </div>
  )
}
