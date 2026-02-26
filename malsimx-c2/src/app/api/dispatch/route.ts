import { NextResponse } from 'next/server';
import { queueCommand } from '../db';

export async function POST(request: Request) {
    try {
        const { id, command } = await request.json();

        if (!id || !command) {
            return NextResponse.json({ error: 'Missing id or command' }, { status: 400 });
        }

        queueCommand(id, command);

        return NextResponse.json({ status: 'ok', queued: true }, { status: 200 });
    } catch (error) {
        return NextResponse.json({ error: 'Invalid request' }, { status: 400 });
    }
}
