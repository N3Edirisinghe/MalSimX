import fs from 'fs';
import path from 'path';

export interface AgentData {
  id: string;
  hostname: string;
  os: string;
  ip: string;
  status: string;
  lastSeen: string;
  pendingCommand?: string;
  logs?: string[];
}

const DB_PATH = path.join(process.cwd(), 'data.json');

export function getAgents(): AgentData[] {
  if (!fs.existsSync(DB_PATH)) {
    return [];
  }
  const data = fs.readFileSync(DB_PATH, 'utf-8');
  return JSON.parse(data);
}

export function saveAgent(agent: AgentData) {
  const agents = getAgents();
  const index = agents.findIndex((a) => a.id === agent.id);

  if (index >= 0) {
    agents[index] = { ...agents[index], ...agent, lastSeen: new Date().toISOString() };
  } else {
    agent.lastSeen = new Date().toISOString();
    agents.push(agent);
  }

  fs.writeFileSync(DB_PATH, JSON.stringify(agents, null, 2));
}

export function queueCommand(agentId: string, command: string) {
  const agents = getAgents();
  const index = agents.findIndex((a) => a.id === agentId);
  if (index >= 0) {
    agents[index].pendingCommand = command;
    fs.writeFileSync(DB_PATH, JSON.stringify(agents, null, 2));
  }
}

export function popCommand(agentId: string): string | undefined {
  const agents = getAgents();
  const index = agents.findIndex((a) => a.id === agentId);

  if (index >= 0 && agents[index].pendingCommand) {
    const cmd = agents[index].pendingCommand;
    agents[index].pendingCommand = undefined;
    fs.writeFileSync(DB_PATH, JSON.stringify(agents, null, 2));
    return cmd;
  }
  return undefined;
}

export function deleteAgent(agentId: string): boolean {
  const agents = getAgents();
  const filtered = agents.filter((a) => a.id !== agentId);
  if (filtered.length === agents.length) return false;
  fs.writeFileSync(DB_PATH, JSON.stringify(filtered, null, 2));
  return true;
}

export function addLogs(agentId: string, newLogs: string[]) {
  const agents = getAgents();
  const index = agents.findIndex((a) => a.id === agentId);

  if (index >= 0) {
    if (!agents[index].logs) {
      agents[index].logs = [];
    }
    // Keep only last 100 logs to prevent file bloat
    const combined = [...agents[index].logs, ...newLogs];
    agents[index].logs = combined.slice(-100);
    fs.writeFileSync(DB_PATH, JSON.stringify(agents, null, 2));
  }
}
