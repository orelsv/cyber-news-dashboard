import React
import {useState
import useEffect} from 'react';
import {
  Settings,
  Search,
  Globe,
  Activity,
  Users,
  FileText,
  AlertTriangle,
  RefreshCw,
  Eye,
  Clock,
  Filter,
  TrendingUp,
  Database,
  Key,
  Server
} from 'lucide-react';

const AdminPanel = () = > {
  const[activeTab, setActiveTab] = useState('dashboard');
  const[stats, setStats] = useState({
    totalArticles: 1247,
    todayArticles: 23,
    apiCalls: 156,
    uptime: '99.8%',
    avgResponseTime: '245ms',
    activeUsers: 12
  });

  const[searchQueries, setSearchQueries] = useState([
    {query: 'cybersecurity OR malware OR "information security"',
        count: 45, isDefault: true},
    {query: 'data breach', count: 12, isDefault: false},
    {query: 'ransomware', count: 8, isDefault: false},
    {query: 'phishing', count: 15, isDefault: false}
  ]);

  const[recentArticles, setRecentArticles] = useState([
    {
      id: 1,
      title: "New Ransomware Variant Targets Healthcare Systems",
      source: "CyberNews",
      published: "2025-09-20 14:30",
      views: 89
    },
    {
      id: 2,
      title: "Major Data Breach Affects 2M Users",
      source: "TechCrunch",
      published: "2025-09-20 12:15",
      views: 156
    },
    {
      id: 3,
      title: "AI-Powered Security Tools Show Promise",
      source: "SecurityWeek",
      published: "2025-09-20 09:45",
      views: 234
    }
  ]);

  const[settings, setSettings] = useState({
    newsApiKey: '••••••••••••••••',
    defaultQuery: 'cybersecurity OR malware OR "information security"',
    pageSize: 20,
    language: 'en',
    sortBy: 'publishedAt',
    cacheTimeout: 300,
    maxRetries: 3
  });

  const tabContent = {
    dashboard: (
      < div className="space-y-6" >
        < div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-4" >
          < div className="bg-gradient-to-br from-blue-500 to-blue-600 text-white p-4 rounded-xl" >
            < div className="flex items-center justify-between" >
              < div >
                < p className="text-blue-100 text-sm" > Total Articles < /p >
                < p className="text-2xl font-bold" > {stats.totalArticles} < /p >
              < / div >
              < FileText size={24} className="text-blue-200" / >
            < /div >
          < / div >

          < div className="bg-gradient-to-br from-green-500 to-green-600 text-white p-4 rounded-xl" >
            < div className="flex items-center justify-between" >
              < div >
                < p className="text-green-100 text-sm" > Today's Articles</p>
                <p className="text-2xl font-bold">{stats.todayArticles}</p>
              </div>
              <Clock size={24} className="text-green-200" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-purple-500 to-purple-600 text-white p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-purple-100 text-sm">API Calls</p>
                <p className="text-2xl font-bold">{stats.apiCalls}</p>
              </div>
              <Globe size={24} className="text-purple-200" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-orange-500 to-orange-600 text-white p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-orange-100 text-sm">Active Users</p>
                <p className="text-2xl font-bold">{stats.activeUsers}</p>
              </div>
              <Users size={24} className="text-orange-200" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-teal-500 to-teal-600 text-white p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-teal-100 text-sm">Uptime</p>
                <p className="text-2xl font-bold">{stats.uptime}</p>
              </div>
              <Activity size={24} className="text-teal-200" />
            </div>
          </div>

          <div className="bg-gradient-to-br from-red-500 to-red-600 text-white p-4 rounded-xl">
            <div className="flex items-center justify-between">
              <div>
                <p className="text-red-100 text-sm">Avg Response</p>
                <p className="text-2xl font-bold">{stats.avgResponseTime}</p>
              </div>
              <Server size={24} className="text-red-200" />
            </div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <TrendingUp className="mr-2 text-blue-600" size={20} />
              Popular Search Queries
            </h3>
            <div className="space-y-3">
              {searchQueries.map((query, index) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <p className="text-sm font-medium text-gray-800 truncate">{query.query}</p>
                    {query.isDefault && <span className="text-xs text-blue-600 font-medium">Default Query</span>}
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className="text-sm text-gray-600">{query.count} searches</span>
                    <div className="w-12 bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full" 
                        style={{width: `${(query.count / Math.max(...searchQueries.map(q => q.count))) * 100}%`}}
                      ></div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <FileText className="mr-2 text-green-600" size={20} />
              Recent Articles
            </h3>
            <div className="space-y-3">
              {recentArticles.map(article => (
                <div key={article.id} className="border-l-4 border-blue-500 pl-4 py-2">
                  <h4 className="text-sm font-medium text-gray-800 line-clamp-2">{article.title}</h4>
                  <div className="flex items-center justify-between mt-1 text-xs text-gray-600">
                    <span>{article.source}</span>
                    <div className="flex items-center space-x-3">
                      <span>{article.published}</span>
                      <div className="flex items-center">
                        <Eye size={12} className="mr-1" />
                        {article.views}
                      </div>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    ),

    articles: (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3 className="text-lg font-semibold">Article Management</h3>
            <button className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg flex items-center">
              <RefreshCw size={16} className="mr-2" />
              Refresh Articles
            </button>
          </div>
          
          <div className="flex items-center space-x-4 mb-4">
            <div className="flex-1">
              <input 
                type="text" 
                placeholder="Search articles..." 
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <select className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500">
              <option>All Sources</option>
              <option>CyberNews</option>
              <option>TechCrunch</option>
              <option>SecurityWeek</option>
            </select>
            <button className="bg-gray-100 hover:bg-gray-200 px-4 py-2 rounded-lg flex items-center">
              <Filter size={16} className="mr-2" />
              Filter
            </button>
          </div>

          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="border-b border-gray-200">
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Title</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Source</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Published</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Views</th>
                  <th className="text-left py-3 px-4 font-medium text-gray-700">Actions</th>
                </tr>
              </thead>
              <tbody>
                {recentArticles.map(article => (
                  <tr key={article.id} className="border-b border-gray-100 hover:bg-gray-50">
                    <td className="py-3 px-4">
                      <div className="max-w-xs truncate font-medium text-gray-800">{article.title}</div>
                    </td>
                    <td className="py-3 px-4 text-gray-600">{article.source}</td>
                    <td className="py-3 px-4 text-gray-600">{article.published}</td>
                    <td className="py-3 px-4">
                      <div className="flex items-center text-gray-600">
                        <Eye size={14} className="mr-1" />
                        {article.views}
                      </div>
                    </td>
                    <td className="py-3 px-4">
                      <button className="text-blue-600 hover:text-blue-800 text-sm">View</button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    ),

    settings: (
      <div className="space-y-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Settings className="mr-2 text-gray-600" size={20} />
            Application Settings
          </h3>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">News API Key</label>
              <div className="flex items-center space-x-2">
                <input 
                  type="password" 
                  value={settings.newsApiKey}
                  className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  readOnly
                />
                <button className="bg-gray-100 hover:bg-gray-200 px-3 py-2 rounded-lg">
                  <Key size={16} />
                </button>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Default Search Query</label>
              <textarea 
                value={settings.defaultQuery}
                onChange={(e) => setSettings({...settings, defaultQuery: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                rows="2"
              />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Page Size</label>
                <input 
                  type="number" 
                  value={settings.pageSize}
                  onChange={(e) => setSettings({...settings, pageSize: parseInt(e.target.value)})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Language</label>
                <select 
                  value={settings.language}
                  onChange={(e) => setSettings({...settings, language: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="en">English</option>
                  <option value="de">German</option>
                  <option value="fr">French</option>
                  <option value="es">Spanish</option>
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Sort By</label>
                <select 
                  value={settings.sortBy}
                  onChange={(e) => setSettings({...settings, sortBy: e.target.value})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                >
                  <option value="publishedAt">Published Date</option>
                  <option value="relevancy">Relevancy</option>
                  <option value="popularity">Popularity</option>
                </select>
              </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Cache Timeout (seconds)</label>
                <input 
                  type="number" 
                  value={settings.cacheTimeout}
                  onChange={(e) => setSettings({...settings, cacheTimeout: parseInt(e.target.value)})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">Max Retries</label>
                <input 
                  type="number" 
                  value={settings.maxRetries}
                  onChange={(e) => setSettings({...settings, maxRetries: parseInt(e.target.value)})}
                  className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                />
              </div>
            </div>

            <div className="flex items-center justify-end space-x-3 pt-4">
              <button className="px-4 py-2 text-gray-600 border border-gray-300 rounded-lg hover:bg-gray-50">
                Reset
              </button>
              <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
                Save Settings
              </button>
            </div>
          </div>
        </div>
      </div>
    ),

    monitoring: (
      <div className="space-y-6">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <Activity className="mr-2 text-blue-600" size={20} />
              System Health
            </h3>
            <div className="space-y-3">
              <div className="flex items-center justify-between">
                <span className="text-gray-600">API Status</span>
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">Healthy</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Database</span>
                <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full text-xs font-medium">Connected</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">NewsAPI Quota</span>
                <span className="bg-yellow-100 text-yellow-800 px-2 py-1 rounded-full text-xs font-medium">78% Used</span>
              </div>
              <div className="flex items-center justify-between">
                <span className="text-gray-600">Memory Usage</span>
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full text-xs font-medium">245 MB</span>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold mb-4 flex items-center">
              <AlertTriangle className="mr-2 text-orange-600" size={20} />
              Recent Alerts
            </h3>
            <div className="space-y-3">
              <div className="flex items-start space-x-3 p-3 bg-yellow-50 rounded-lg">
                <AlertTriangle size={16} className="text-yellow-600 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">API Rate Limit Warning</p>
                  <p className="text-xs text-gray-600 mt-1">Approaching daily quota limit</p>
                  <p className="text-xs text-gray-500 mt-1">2 minutes ago</p>
                </div>
              </div>
              
              <div className="flex items-start space-x-3 p-3 bg-green-50 rounded-lg">
                <Activity size={16} className="text-green-600 mt-0.5 flex-shrink-0" />
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-800">System Restart Complete</p>
                  <p className="text-xs text-gray-600 mt-1">Application restarted successfully</p>
                  <p className="text-xs text-gray-500 mt-1">1 hour ago</p>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold mb-4 flex items-center">
            <Database className="mr-2 text-purple-600" size={20} />
            Performance Metrics
          </h3>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-blue-600">2.3s</p>
              <p className="text-sm text-gray-600">Avg Load Time</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-green-600">156</p>
              <p className="text-sm text-gray-600">Requests/Hour</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-purple-600">99.8%</p>
              <p className="text-sm text-gray-600">Uptime</p>
            </div>
            <div className="text-center p-4 bg-gray-50 rounded-lg">
              <p className="text-2xl font-bold text-orange-600">0</p>
              <p className="text-sm text-gray-600">Errors Today</p>
            </div>
          </div>
        </div>
      </div>
    )
  };

  const tabs = [
    { id: 'dashboard', label: 'Dashboard', icon: Activity },
    { id: 'articles', label: 'Articles', icon: FileText },
    { id: 'settings', label: 'Settings', icon: Settings },
    { id: 'monitoring', label: 'Monitoring', icon: Globe }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center">
              <div className="bg-blue-600 p-2 rounded-lg">
                <FileText size={24} className="text-white" />
              </div>
              <h1 className="ml-3 text-xl font-semibold text-gray-900">News App Admin</h1>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-gray-600">Last updated: {new Date().toLocaleTimeString()}</div>
              <div className="w-2 h-2 bg-green-500 rounded-full"></div>
              <span className="text-sm text-green-600 font-medium">Online</span>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation Tabs */}
      <div className="bg-white border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <nav className="flex space-x-8">
            {tabs.map(tab => {
              const Icon = tab.icon;
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`py-4 px-1 border-b-2 font-medium text-sm flex items-center space-x-2 ${
                    activeTab === tab.id
                      ? 'border-blue-500 text-blue-600'
                      : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
                  }`}
                >
                  <Icon size={16} />
                  <span>{tab.label}</span>
                </button>
              );
            })}
          </nav>
        </div>
      </div>

      {/* Main Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        {tabContent[activeTab]}
      </div>
    </div>
  );
};

export default AdminPanel;