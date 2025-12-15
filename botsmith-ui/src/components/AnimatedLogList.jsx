import { AnimatePresence, motion } from 'framer-motion';
import { Terminal } from 'lucide-react';
import { useEffect, useRef } from 'react';

export const AnimatedLogList = ({ logs }) => {
    const bottomRef = useRef(null);

    useEffect(() => {
        bottomRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [logs]);

    return (
        <div className="h-full flex flex-col bg-opacity-50">
            <div className="flex items-center gap-2 px-4 py-2 border-b border-gray-800 bg-gray-900/50 backdrop-blur">
                <Terminal size={16} className="text-secondaryGlow" />
                <span className="text-sm font-mono font-bold text-gray-400">SYSTEM LOGS</span>
            </div>

            <div className="flex-1 overflow-y-auto p-4 font-mono text-sm space-y-2">
                <AnimatePresence>
                    {logs.map((log, i) => (
                        <motion.div
                            key={i}
                            initial={{ opacity: 0, x: -20 }}
                            animate={{ opacity: 1, x: 0 }}
                            transition={{ duration: 0.2 }}
                            className="flex gap-2"
                        >
                            <span className="text-gray-600">[{new Date().toLocaleTimeString()}]</span>
                            <span className={log.level === 'error' ? 'text-failure' : 'text-glow'}>
                                {log.message}
                            </span>
                        </motion.div>
                    ))}
                </AnimatePresence>
                <div ref={bottomRef} />
            </div>
        </div>
    );
};
