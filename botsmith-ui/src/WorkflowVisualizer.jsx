import { motion } from 'framer-motion';
import { Download, Play, Sparkles } from 'lucide-react';
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
                // Handle different event types
                switch (event.type) {
                    case 'step_start':
                        setCurrentStep(event.data.step);
                        setStepsStatus(prev => ({ ...prev, [event.data.step]: 'running' }));
                        break;

                    case 'step_complete':
                        setStepsStatus(prev => ({
                            ...prev,
                            [event.data.step]: event.data.status // 'success' or 'failed'
                        }));
                        break;

                    case 'log':
                        setLogs(prev => [...prev, event.data]);
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

    return (
        <div className="min-h-screen bg-background text-white font-sans selection:bg-glow selection:text-black">
            {/* HEADER */}
            <header className="border-b border-gray-800 p-6 flex justify-between items-center bg-gray-900/50 backdrop-blur sticky top-0 z-50">
                <div className="flex items-center gap-3">
                    <div className="w-8 h-8 rounded bg-gradient-to-br from-glow to-secondaryGlow flex items-center justify-center">
                        <Sparkles className="text-black w-5 h-5" />
                    </div>
                    <h1 className="text-xl font-bold tracking-tight">BotSmith <span className="text-glow">Studio</span></h1>
                </div>
                <div className="text-sm text-gray-500 font-mono">v1.0.0</div>
            </header>

            {/* INPUT HERO */}
            <div className="max-w-7xl mx-auto p-6 space-y-8">
                {!isBuilding && !isDone && (
                    <motion.div
                        initial={{ opacity: 0, y: 20 }}
                        animate={{ opacity: 1, y: 0 }}
                        className="flex flex-col gap-4 max-w-2xl mx-auto mt-10 p-8 border border-gray-800 rounded-2xl bg-gray-900/30 box-glow"
                    >
                        <h2 className="text-2xl font-bold text-center">What are we building today?</h2>
                        <textarea
                            value={prompt}
                            onChange={(e) => setPrompt(e.target.value)}
                            placeholder="Describe your bot (e.g., 'A research agent that summarizes tech news from RSS feeds')"
                            className="w-full h-32 bg-black/50 border border-gray-700 rounded-xl p-4 focus:border-glow focus:ring-1 focus:ring-glow outline-none transition-all resize-none font-mono text-sm"
                        />
                        <div className="flex gap-4">
                            <input
                                type="text"
                                value={projectName}
                                onChange={(e) => setProjectName(e.target.value)}
                                placeholder="Project Name"
                                className="flex-1 bg-black/50 border border-gray-700 rounded-lg p-3 focus:border-glow outline-none font-mono text-sm"
                            />
                            <button
                                onClick={handleGenerate}
                                disabled={!prompt}
                                className="bg-glow text-black font-bold px-8 py-3 rounded-lg hover:bg-white transition-colors flex items-center gap-2 disabled:opacity-50 disabled:cursor-not-allowed"
                            >
                                <Play size={18} fill="currentColor" />
                                Generate
                            </button>
                        </div>
                    </motion.div>
                )}

                {/* PIPELINE VISUALIZATION - Show if building or if we have any steps status (failed/success) */}
                {(isBuilding || isDone || Object.keys(stepsStatus).length > 0) && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="space-y-6"
                    >
                        <PipelineVisualizer currentStep={currentStep} stepsStatus={stepsStatus} />

                        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[600px]">
                            {/* LEFT: LOGS */}
                            <div className="lg:col-span-2 border border-gray-800 rounded-xl bg-black/40 overflow-hidden">
                                <AnimatedLogList logs={logs} />
                            </div>

                            {/* RIGHT: FILES */}
                            <div className="border border-gray-800 rounded-xl bg-black/40 overflow-hidden">
                                <FileTree files={files} />
                            </div>
                        </div>
                    </motion.div>
                )}

                {/* SUCCESS STATE */}
                {isDone && (
                    <motion.div
                        initial={{ opacity: 0, scale: 0.9 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="flex justify-center mt-8 pb-10"
                    >
                        <button
                            onClick={() => window.open(`http://localhost:8000/bot/download/${projectName}`, '_blank')}
                            className="bg-success text-black font-bold px-10 py-4 rounded-full flex items-center gap-3 hover:bg-white box-glow transition-all transform hover:scale-105"
                        >
                            <Download size={20} />
                            Download Bot Package
                        </button>
                    </motion.div>
                )}
                {/* DEBUG FOOTER */}
                <div className="fixed bottom-0 left-0 right-0 bg-red-900/80 text-white text-xs p-2 font-mono flex justify-between">
                    <span>STATUS: {isBuilding ? 'BUILDING' : 'IDLE'} | DONE: {isDone ? 'YES' : 'NO'} | STEPS: {Object.keys(stepsStatus).length} | LOGS: {logs.length} | PROMPT: {prompt.substring(0, 20)}</span>
                </div>
            </div>
        </div>
    );
};
