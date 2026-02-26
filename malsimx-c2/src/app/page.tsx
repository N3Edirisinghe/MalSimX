"use client";

import { useEffect, useState } from "react";
import { Terminal, ShieldAlert, Cpu, Activity, Clock, Server, MonitorSmartphone, Skull } from "lucide-react";
import { formatDistanceToNow } from "date-fns";
import type { AgentData } from "./api/db";

export default function Dashboard() {
  const [agents, setAgents] = useState<AgentData[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchAgents = async () => {
      try {
        const res = await fetch("/api/agents");
        const data = await res.json();
        setAgents(data.agents || []);
      } catch (err) {
        console.error("Failed to fetch agents", err);
      } finally {
        setLoading(false);
      }
    };

    fetchAgents();
    const interval = setInterval(fetchAgents, 3000);
    return () => clearInterval(interval);
  }, []);

  const getStatusColor = (status: string, lastSeen: string) => {
    const isDead = new Date().getTime() - new Date(lastSeen).getTime() > 30000;
    if (isDead) return "text-red-500 border-red-500/30 bg-red-500/10";
    if (status.includes("active")) return "text-emerald-400 border-emerald-500/30 bg-emerald-500/10 text-glow";
    return "text-yellow-400 border-yellow-500/30 bg-yellow-500/10";
  };

  return (
    <div className="min-h-screen bg-[#050505] text-slate-300 p-6 sm:p-10 font-mono selection:bg-emerald-500/30 selection:text-emerald-100">

      {/* Header section */}
      <header className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-12 border-b border-white/5 pb-6">
        <div>
          <h1 className="text-3xl font-bold text-emerald-400 tracking-tighter flex items-center gap-3 text-glow">
            <Skull className="w-8 h-8" />
            MalSimX Command & Control
          </h1>
          <p className="text-slate-500 mt-2 text-sm max-w-lg">
            Adversary execution node network. Tracking active implants and dispatching simulation playbooks.
          </p>
        </div>

        <div className="mt-6 sm:mt-0 flex gap-4">
          <div className="glass-panel px-4 py-2 rounded-lg flex items-center gap-3">
            <Activity className="w-5 h-5 text-emerald-400 animate-pulse" />
            <div className="flex flex-col">
              <span className="text-xs text-slate-500 uppercase tracking-widest">Active Implants</span>
              <span className="text-xl font-bold text-white leading-none">
                {agents.filter(a => new Date().getTime() - new Date(a.lastSeen).getTime() <= 30000).length}
              </span>
            </div>
          </div>
          <div className="glass-panel px-4 py-2 rounded-lg flex items-center gap-3">
            <Server className="w-5 h-5 text-indigo-400" />
            <div className="flex flex-col">
              <span className="text-xs text-slate-500 uppercase tracking-widest">Total Dropped</span>
              <span className="text-xl font-bold text-white leading-none">{agents.length}</span>
            </div>
          </div>
        </div>
      </header>

      {/* Main content */}
      <main>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-semibold text-white tracking-tight flex items-center gap-2">
            <Terminal className="w-5 h-5 text-emerald-500" />
            Infected Endpoints
          </h2>
          <div className="text-xs text-slate-500 animate-pulse flex items-center gap-2">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            AUTO-REFRESHING...
          </div>
        </div>

        {loading ? (
          <div className="glass-panel h-64 rounded-xl flex items-center justify-center border-dashed border-slate-800">
            <div className="flex flex-col items-center gap-4">
              <Activity className="w-8 h-8 text-emerald-500 animate-spin" />
              <p className="text-emerald-500/50 uppercase tracking-widest text-sm text-glow">Establishing uplink...</p>
            </div>
          </div>
        ) : agents.length === 0 ? (
          <div className="glass-panel h-64 rounded-xl flex flex-col items-center justify-center border-dashed border-slate-800 text-center px-4">
            <ShieldAlert className="w-12 h-12 text-slate-700 mb-4" />
            <h3 className="text-lg text-slate-300 font-medium mb-1">No Active Agents</h3>
            <p className="text-sm text-slate-500 max-w-sm">
              The C2 server is listening, but no endpoints have executed the payload or checked in recently.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {agents.map((agent) => (
              <div
                key={agent.id}
                className="glass-panel rounded-xl p-6 transition-all duration-300 hover:border-emerald-500/40 hover:-translate-y-1"
              >
                <div className="flex justify-between items-start mb-4">
                  <div className="flex items-center gap-3">
                    <div className="h-10 w-10 rounded-lg bg-slate-900 flex items-center justify-center border border-slate-800 shadow-inner">
                      <MonitorSmartphone className="text-slate-400 w-5 h-5" />
                    </div>
                    <div>
                      <h3 className="text-white font-bold tracking-tight">{agent.hostname}</h3>
                      <p className="text-xs text-slate-500 flex items-center gap-1">
                        <Cpu className="w-3 h-3" /> {agent.os}
                      </p>
                    </div>
                  </div>
                  <span className={`px-2.5 py-1 rounded-full text-[10px] font-bold uppercase tracking-wider border ${getStatusColor(agent.status, agent.lastSeen)}`}>
                    {new Date().getTime() - new Date(agent.lastSeen).getTime() > 30000 ? "OFFLINE" : agent.status}
                  </span>
                </div>

                <div className="space-y-3 mt-6">
                  <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                    <span className="text-slate-500">Implant ID</span>
                    <span className="text-slate-300 opacity-70 truncate max-w-[150px]">{agent.id}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm border-b border-white/5 pb-2">
                    <span className="text-slate-500">Network IP</span>
                    <span className="text-slate-300 font-medium">{agent.ip}</span>
                  </div>
                  <div className="flex justify-between items-center text-sm">
                    <span className="text-slate-500 flex items-center gap-1.5 hover:text-slate-300 transition-colors">
                      <Clock className="w-3.5 h-3.5" /> Last check-in
                    </span>
                    <span className="text-slate-300 text-right">
                      {formatDistanceToNow(new Date(agent.lastSeen), { addSuffix: true })}
                    </span>
                  </div>
                </div>

                <div className="mt-6 pt-4 border-t border-white/5 flex grid grid-cols-2 gap-3">
                  <button className="w-full py-2 bg-emerald-500/10 hover:bg-emerald-500/20 text-emerald-400 text-xs font-bold tracking-widest uppercase rounded border border-emerald-500/30 transition-colors">
                    Deploy Block
                  </button>
                  <button className="w-full py-2 bg-slate-800 hover:bg-slate-700 text-slate-300 text-xs font-bold tracking-widest uppercase rounded border border-slate-700 transition-colors">
                    View Logs
                  </button>
                </div>
              </div>
            ))}
          </div>
        )}
      </main>
    </div>
  );
}
