import fs from 'fs';
import path from 'path';

export interface AgentData {
  id: string;
  hostname: string;
  os: string;
  ip: string;
  status: string;
  lastSeen: string;
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
