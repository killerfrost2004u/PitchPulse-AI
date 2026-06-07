"use client";

import { useWebSocket } from '@/hooks/useWebSocket';

export default function Home() {
  const { isConnected, latestFrame, tacticalEvents } = useWebSocket();

  return (
    <main className="min-h-screen bg-neutral-950 text-neutral-100 p-8 font-sans">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header */}
        <header className="flex items-center justify-between border-b border-neutral-800 pb-6">
          <div>
            <h1 className="text-3xl font-bold tracking-tight bg-gradient-to-r from-emerald-400 to-cyan-400 bg-clip-text text-transparent">
              PitchPulse AI
            </h1>
            <p className="text-neutral-400 mt-1">Real-time Multimodal Soccer Tactical Analyst</p>
          </div>
          
          {/* Connection Status Badge */}
          <div className={`px-4 py-1.5 rounded-full text-sm font-medium flex items-center gap-2 transition-colors ${
            isConnected ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20' 
                        : 'bg-red-500/10 text-red-400 border border-red-500/20'
          }`}>
            <span className={`w-2 h-2 rounded-full ${isConnected ? 'bg-emerald-400 animate-pulse' : 'bg-red-400'}`}></span>
            {isConnected ? 'Live Connection' : 'Disconnected'}
          </div>
        </header>

        {/* Dashboard Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Main Radar View */}
          <section className="lg:col-span-2 bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-2xl relative overflow-hidden flex flex-col min-h-[500px]">
            <h2 className="text-lg font-semibold text-neutral-200 mb-4 flex items-center gap-2">
              <span className="text-emerald-400">●</span> 2D Pitch Radar
            </h2>
            <div className="flex-1 bg-neutral-950 rounded-xl border border-neutral-800/50 flex flex-col items-center justify-center relative overflow-hidden">
                <div className="absolute inset-0 bg-[linear-gradient(to_right,#80808012_1px,transparent_1px),linear-gradient(to_bottom,#80808012_1px,transparent_1px)] bg-[size:24px_24px]"></div>
                {latestFrame ? (
                    <div className="z-10 bg-neutral-900/80 backdrop-blur border border-neutral-800 p-6 rounded-xl max-w-md w-full font-mono text-sm shadow-xl">
                        <div className="text-emerald-400 mb-2">Raw Frame Data Received:</div>
                        <pre className="text-neutral-300 overflow-x-auto">
                            {JSON.stringify(latestFrame, null, 2)}
                        </pre>
                    </div>
                ) : (
                    <div className="z-10 flex flex-col items-center text-neutral-500">
                        <div className="w-8 h-8 border-4 border-neutral-700 border-t-emerald-500 rounded-full animate-spin mb-4"></div>
                        <p>Waiting for Edge Vision pipeline data...</p>
                    </div>
                )}
            </div>
          </section>

          {/* Side Panel: Tactical Events & AI Insights */}
          <section className="flex flex-col gap-6">
            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-xl flex-1">
                <h2 className="text-lg font-semibold text-neutral-200 mb-4 flex items-center gap-2">
                  <span className="text-cyan-400">⚡</span> Tactical Events
                </h2>
                <div className="space-y-3">
                  {tacticalEvents.length === 0 ? (
                      <p className="text-sm text-neutral-500 italic">No events recorded yet.</p>
                  ) : (
                      tacticalEvents.map((event, idx) => (
                          <div key={idx} className="p-3 bg-neutral-950 border border-neutral-800 rounded-lg text-sm">
                              <div className="text-cyan-400 font-medium mb-1">{event.event_type.toUpperCase()}</div>
                              <div className="text-neutral-300">{event.description}</div>
                          </div>
                      ))
                  )}
                </div>
            </div>

            <div className="bg-neutral-900 border border-neutral-800 rounded-2xl p-6 shadow-xl">
                <h2 className="text-lg font-semibold text-neutral-200 mb-4 flex items-center gap-2">
                  <span className="text-purple-400">🧠</span> Gemini AI Analyst
                </h2>
                <div className="p-4 bg-purple-500/5 border border-purple-500/20 rounded-xl text-sm text-purple-200/80 italic">
                    Waiting for enough tactical events to generate insights...
                </div>
            </div>
          </section>

        </div>
      </div>
    </main>
  );
}
