import { NextResponse } from 'next/server';
import { getAgents } from '../db';

export const dynamic = 'force-dynamic';

export async function GET() {
    const agents = getAgents();
    return NextResponse.json({ agents });
}
