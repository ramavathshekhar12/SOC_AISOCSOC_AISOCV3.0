import React, { useEffect, useState } from 'react'
import { createRoot } from 'react-dom/client'
import api from './http'
import { login, logout, handleRedirect, getUser } from './auth'
import './index.css'

function Header({user}){
  return (
    <div className="flex items-center justify-between mb-6">
      <div className="flex items-center gap-3">
        <img src="/logo.svg" className="h-8 w-auto" alt="logo"/>
        <div className="text-xl font-semibold">OneStopSec • AI‑SOC</div>
      </div>
      <div className="flex items-center gap-3">
        {user ? (<>
          <span className="badge">{user.profile?.name || user.profile?.preferred_username}</span>
          <button className="btn" onClick={logout}>Logout</button>
        </>) : (<button className="btn" onClick={login}>Login with Entra ID</button>)}
      </div>
    </div>
  )
}

function Alerts(){
  const [alerts, setAlerts] = useState([])
  useEffect(() => { api.get('/alerts?limit=200').then(r => setAlerts(r.data)).catch(console.error) }, [])
  return (
    <div className="card">
      <div className="text-lg font-semibold mb-3">Latest Alerts</div>
      <table className="table">
        <thead><tr><th>Time</th><th>Rule</th><th>Level</th><th>Tags</th><th>Host</th><th>Msg</th></tr></thead>
        <tbody>
          {alerts.map((a,i)=>(
            <tr key={i}>
              <td>{a.ts}</td><td>{a.rule_name}</td><td><span className="badge">{a.level}</span></td>
              <td>{(a.tags||[]).join(', ')}</td><td>{a.event?.host}</td>
              <td className="max-w-[600px] truncate">{a.event?.message || a.event?.['@raw']}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

function Admin(){
  const reload = async () => {
    await api.post('/admin/reload-rules', {})
    alert('Rules reloaded')
  }
  return (
    <div className="card">
      <div className="text-lg font-semibold mb-3">Admin</div>
      <button className="btn" onClick={reload}>Reload Rules</button>
    </div>
  )
}

function App(){
  const [user, setUser] = useState(null)
  useEffect(() => { handleRedirect().then(()=>getUser().then(setUser)) }, [])
  useEffect(() => { getUser().then(setUser) }, [])
  return (
    <div className="max-w-7xl mx-auto p-6">
      <Header user={user}/>
      <div className="grid gap-6 md:grid-cols-1">
        <Alerts/>
        <Admin/>
      </div>
    </div>
  )
}

createRoot(document.getElementById('root')).render(<App/>)
