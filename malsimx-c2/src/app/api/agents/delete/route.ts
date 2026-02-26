import { NextResponse } from 'next/server';
import { deleteAgent } from '../../db';

export async function POST(request: Request) {
    try {
        const { id } = await request.json();

        if (!id) {
            return NextResponse.json({ error: 'Missing agent id' }, { status: 400 });
        }

        const deleted = deleteAgent(id);

        if (!deleted) {
            return NextResponse.json({ error: 'Agent not found' }, { status: 404 });
        }

        return NextResponse.json({ status: 'ok', deleted: true }, { status: 200 });
    } catch (error) {
        return NextResponse.json({ error: 'Invalid request' }, { status: 400 });
    }
}
