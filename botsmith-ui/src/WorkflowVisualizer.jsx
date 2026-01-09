import { AnimatePresence, motion } from 'framer-motion';
import { Download, FileCode, Play, Sparkles, Terminal } from 'lucide-react';
import { useState } from 'react';
import { createEventSource } from './api/botsmithClient';
import { AnimatedLogList } from './components/AnimatedLogList';
import { FileTree } from './components/FileTree';
import { PipelineVisualizer } from './components/PipelineVisualizer';

export const WorkflowVisualizer = () => {
    const [prompt, setPrompt] = useState('');
    const [projectName, setProjectName] = useState('MyAgent');
    const [isBuilding, setIsBuilding] = useState(false);
    const [currentStep, setCurrentStep] = useState(null);
    const [stepsStatus, setStepsStatus] = useState({});
    const [logs, setLogs] = useState([]);
    const [files, setFiles] = useState([]);
    const [isDone, setIsDone] = useState(false);

    const handleGenerate = () => {
        if (!prompt) return;

        setIsBuilding(true);
        setIsDone(false);
        setLogs([]);
        setFiles([]);
        setStepsStatus({});
        setCurrentStep('scaffold_project');

        try {
            console.log("Generating with prompt:", prompt);
            createEventSource(prompt, projectName, (event) => {
                switch (event.type) {
                    case 'step_start':
                        setCurrentStep(event.data.step);
                        setStepsStatus(prev => ({ ...prev, [event.data.step]: 'running' }));
                        break;
                    case 'step_complete':
                        setStepsStatus(prev => ({ ...prev, [event.data.step]: event.data.status }));
                        break;
                    case 'log':
                        setLogs(prev => [...prev, event.data]);
                        break;
                    case 'file_start':
                        setLogs(prev => [...prev, { level: 'info', message: `Generating ${event.data.filename}...` }]);
                        break;
                    case 'file_complete':
                        setFiles(prev => [...prev, event.data]);
                        break;
                    case 'done':
                        setIsBuilding(false);
                        setIsDone(event.data.status === 'success');
                        setCurrentStep(null);
                        break;
                    case 'error':
                        console.error("Stream Error:", event.data);
                        setLogs(prev => [...prev, { level: 'error', message: event.data.message }]);
                        break;
                }
            });
        } catch (e) {
            console.error("handleGenerate Error:", e);
            setLogs(prev => [...prev, { level: 'error', message: "Failed to start generation: " + e.message }]);
        }
    };

    const showLanding = !isBuilding && !isDone;

    return (
        <div className="min-h-screen bg-[#0B0F19] text-gray-200 font-sans selection:bg-cyan-500/30 selection:text-cyan-200 relative overflow-hidden flex flex-col">

            {/* Ambient Background Effect */}
            <div className="fixed inset-0 pointer-events-none bg-[radial-gradient(circle_at_50%_0%,_rgba(56,189,248,0.05),_transparent_50%)] z-0" />

            {/* HEADER */}
            <header className="border-b border-gray-800/50 p-6 flex justify-between items-center bg-[#0B0F19]/80 backdrop-blur sticky top-0 z-50">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded bg-gradient-to-br from-cyan-400 to-blue-500 flex items-center justify-center shadow-lg shadow-cyan-500/20">
                        <Sparkles className="text-white w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight text-white">BotSmith <span className="text-cyan-400 font-light">Studio</span></h1>
                </div>
                <div className="flex items-center gap-4 text-xs font-mono text-gray-500">
                    <span className="flex items-center gap-1.5"><div className="w-2 h-2 rounded-full bg-green-500/50 animate-pulse" /> System Online</span>
                    <span className="opacity-50">v1.0.0</span>
                </div>
            </header>

            <main className="flex-1 relative z-10 w-full max-w-7xl mx-auto p-6 flex flex-col">
                <AnimatePresence mode="wait">

                    {/* LANDING STATE */}
                    {showLanding && (
                        <motion.div
                            key="landing"
                            initial={{ opacity: 0, y: 10 }}
                            animate={{ opacity: 1, y: 0 }}
                            exit={{ opacity: 0, y: -20, filter: "blur(10px)" }}
                            transition={{ duration: 0.5 }}
                            className="flex-1 flex flex-col justify-center items-center min-h-[60vh] max-w-3xl mx-auto w-full"
                        >
                            <div className="text-center space-y-6 mb-12">
                                <h2 className="text-5xl font-bold tracking-tighter text-transparent bg-clip-text bg-gradient-to-br from-white via-gray-200 to-gray-500">
                                    What are we building today?
                                </h2>
                                <p className="text-lg text-gray-400 max-w-lg mx-auto leading-relaxed">
                                    Describe your autonomous agent in plain English. BotSmith will plan, architect, and deploy it for you.
                                </p>
                            </div>

                            <div className="w-full space-y-4 bg-gray-900/40 p-1.5 rounded-2xl border border-gray-800 ring-1 ring-white/5 shadow-2xl backdrop-blur-sm">
                                <textarea
                                    value={prompt}
                                    onChange={(e) => setPrompt(e.target.value)}
                                    placeholder="e.g., 'Create a research agent that monitors Hacker News and summarizes trending AI topics to a markdown file...'"
                                    className="w-full h-32 bg-[#0F1420] rounded-xl p-5 text-gray-100 placeholder-gray-600 outline-none resize-none font-mono text-sm leading-relaxed focus:bg-[#131926] transition-colors"
                                    autoFocus
                                />
                                <div className="flex gap-2 p-1">
                                    <div className="flex-1 bg-[#0F1420] rounded-lg border border-gray-800/50 group focus-within:border-cyan-500/50 transition-colors">
                                        <input
                                            type="text"
                                            value={projectName}
                                            onChange={(e) => setProjectName(e.target.value)}
                                            placeholder="Project Name"
                                            className="w-full h-full bg-transparent px-4 py-3 outline-none font-mono text-sm text-cyan-100 placeholder-gray-600"
                                        />
                                    </div>
                                    <button
                                        onClick={handleGenerate}
                                        disabled={!prompt}
                                        className="bg-cyan-500 hover:bg-cyan-400 text-black font-semibold px-8 py-3 rounded-lg transition-all flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed shadow-[0_0_20px_rgba(34,211,238,0.3)] hover:shadow-[0_0_30px_rgba(34,211,238,0.5)]"
                                    >
                                        <Play size={16} fill="currentColor" />
                                        <span>Initialize</span>
                                    </button>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* DASHBOARD STATE */}
                    {!showLanding && (
                        <motion.div
                            key="dashboard"
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            transition={{ duration: 0.6, delay: 0.2 }}
                            className="space-y-8 w-full mt-4"
                        >
                            {/* Pipeline Section */}
                            <div className="space-y-4">
                                <div className="flex items-center gap-2 text-sm text-gray-400 font-mono uppercase tracking-widest pl-1">
                                    <Terminal size={14} className="text-cyan-500" />
                                    Execution Pipeline
                                </div>
                                <PipelineVisualizer currentStep={currentStep} stepsStatus={stepsStatus} />
                            </div>

                            {/* Main Grid */}
                            <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">

                                {/* LOGS */}
                                <div className="lg:col-span-2 border border-gray-800 rounded-xl bg-[#0F1420]/80 overflow-hidden flex flex-col shadow-xl">
                                    <div className="p-4 border-b border-gray-800 bg-[#0F1420] flex items-center justify-between">
                                        <div className="text-xs font-mono text-gray-400 uppercase tracking-wider flex items-center gap-2">
                                            <Terminal size={12} /> System Logs
                                        </div>
                                        <div className="flex gap-1.5">
                                            <div className="w-2.5 h-2.5 rounded-full bg-red-500/20 text-red-500 flex items-center justify-center text-[8px]">•</div>
                                            <div className="w-2.5 h-2.5 rounded-full bg-yellow-500/20 text-yellow-500 flex items-center justify-center text-[8px]">•</div>
                                            <div className="w-2.5 h-2.5 rounded-full bg-green-500/20 text-green-500 flex items-center justify-center text-[8px]">•</div>
                                        </div>
                                    </div>
                                    <div className="flex-1 overflow-hidden relative font-mono text-sm">
                                        <AnimatedLogList logs={logs} />
                                    </div>
                                </div>

                                {/* FILES */}
                                <div className="border border-gray-800 rounded-xl bg-[#0F1420]/80 overflow-hidden flex flex-col shadow-xl">
                                    <div className="p-4 border-b border-gray-800 bg-[#0F1420] text-xs font-mono text-gray-400 uppercase tracking-wider flex items-center gap-2">
                                        <FileCode size={12} /> Workspace Artifacts
                                    </div>
                                    <div className="flex-1 overflow-hidden relative">
                                        <FileTree files={files} />
                                        {files.length === 0 && (
                                            <div className="absolute inset-0 flex flex-col items-center justify-center text-gray-700 font-mono text-sm space-y-2">
                                                <div className="w-8 h-8 rounded-full border border-gray-800 flex items-center justify-center">
                                                    <div className="w-1 h-1 bg-gray-600 rounded-full animate-ping" />
                                                </div>
                                                <span>Waiting for filesystem events...</span>
                                            </div>
                                        )}
                                    </div>
                                </div>
                            </div>
                        </motion.div>
                    )}

                    {/* SUCCESS FOOTER */}
                    {isDone && (
                        <motion.div
                            initial={{ opacity: 0, y: 20 }}
                            animate={{ opacity: 1, y: 0 }}
                            className="fixed bottom-8 left-1/2 -translate-x-1/2 z-50"
                        >
                            <button
                                onClick={() => window.open(`http://localhost:8000/bot/download/${projectName}`, '_blank')}
                                className="bg-green-500 text-black font-bold px-8 py-4 rounded-full flex items-center gap-3 hover:bg-white hover:scale-105 transition-all shadow-[0_0_40px_rgba(34,197,94,0.4)]"
                            >
                                <Download size={20} />
                                Download {projectName} Package
                            </button>
                        </motion.div>
                    )}
                </AnimatePresence>
            </main>
        </div>
    );
};
