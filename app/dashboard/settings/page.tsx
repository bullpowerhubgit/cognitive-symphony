export default function SettingsPage() {
  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <h1 className="text-3xl font-bold text-gray-900">Einstellungen</h1>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-4 py-8">
        {/* Digistore24 API */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">Digistore24 API</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Key
              </label>
              <input
                type="text"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="Dein Digistore24 API Key"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                API Secret
              </label>
              <input
                type="password"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg"
                placeholder="Dein API Secret"
              />
            </div>
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Speichern
            </button>
          </div>
        </div>

        {/* E-Mail Integration */}
        <div className="bg-white rounded-lg shadow p-6 mb-6">
          <h2 className="text-xl font-bold mb-4">E-Mail Integration</h2>
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                E-Mail Provider
              </label>
              <select className="w-full px-4 py-2 border border-gray-300 rounded-lg">
                <option>SendGrid</option>
                <option>Mailchimp</option>
                <option>SMTP</option>
              </select>
            </div>
            <button className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Konfigurieren
            </button>
          </div>
        </div>

        {/* Automation */}
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Automation</h2>
          <div className="space-y-3">
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" />
              <span>Automatische Sales-Synchronisation</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" />
              <span>Tägliche Berichte per E-Mail</span>
            </label>
            <label className="flex items-center">
              <input type="checkbox" className="mr-3" />
              <span>Affiliate-Benachrichtigungen</span>
            </label>
          </div>
        </div>
      </main>
    </div>
  )
}
